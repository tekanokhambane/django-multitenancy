import logging
import datetime
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.db.models import F, Sum
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
import uuid
from django.conf import settings
from django.db import models
from multitenancy.settings.models import Currency
from multitenancy.subscriptions.models import Subscription
from django_countries.fields import CountryField
from django.conf import settings
from django.db.models import Q
from djmoney.models.fields import MoneyField


class CurrencyAmount(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.currency.code} {self.amount}"


class InvoiceQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.all()
        lookups = (
            Q(subscription__product_type__name__icontains=query)
            | Q(id__exact=query)
            | Q(invoice_number__exact=query)
        )
        return self.filter(lookups)

    def filter_by_id(self, id=None):
        if id is None or id == "":
            return self.all()
        return self.filter(id__exact=id)

    def get_due_date(self, date=None):
        if date is None or date == "":
            return self.all()
        return self.filter(due_date__exact=date)

    def filter_date_range(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
            return self.all()
        return self.filter(date_created__range=(start_date, end_date))

    def get_status(self, status):
        if status is None or status == "":
            return self.all()
        return self.filter(status__exact=status)


class InvoiceManager(models.Manager):
    def get_queryset(self):
        return InvoiceQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def filter_by_id(self, id=None):
        return self.get_queryset().filter_by_id(id=id)

    def get_due_date(self, date=None):
        return self.get_queryset().get_due_date(date=date)

    def filter_date_range(self, start_date, end_date):
        return self.get_queryset().filter_date_range(
            start_date=start_date, end_date=end_date
        )

    def get_status(self, status):
        return self.get_queryset().get_status(status=status)


def invoice_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/invoices/<invoice_number>/<filename>
    return f"invoices/{instance.invoice_number}/{filename}"


class Invoice(models.Model):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="invoices"
    )
    date_created = models.DateField(auto_now_add=True, db_index=True)
    due_date = models.DateField(db_index=True)
    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_used = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.0")
    )
    payment_method = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("paid", "Paid"),
            ("unpaid", "Unpaid"),
            ("pending", "Pending"),
            ("cancelled", "Cancelled"),
            ("refunded", "Refunded"),
        ],
        db_index=True,
    )
    notes = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to=invoice_directory_path)
    objects = InvoiceManager()

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.invoice_number

    def create_pdf(self):
        pass


class RefundQuerySet(models.QuerySet):
    def get_invoice(self, invoice_id=None):
        if invoice_id is None or invoice_id == "":
            return self.all()
        return self.filter(invoice_id__exact=invoice_id)


class RefundManager(models.Manager):
    def get_queryset(self):
        return RefundQuerySet(self.model, using=self._db)

    def get_invoice(self, invoice_id=None):
        return self.get_queryset().get_invoice(invoice_id=invoice_id)


class Refund(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="refunds"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    objects = RefundManager()

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return (
            f"Invoice -{self.invoice.pk}, Amount: {self.amount}, Status: {self.status}"
        )

    def clean(self):
        if self.amount > self.invoice.amount:
            raise ValidationError(
                "Refund amount cannot be greater than invoice amount."
            )
        super().clean()

    def update_invoice_status(self):
        self.invoice.status = F("refunded")
        self.invoice.save()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.update_invoice_status()
            super().save(*args, **kwargs)


def update_invoice_status(sender, instance, **kwargs):
    instance.invoice.status = "refunded"
    instance.invoice.save()


post_save.connect(update_invoice_status, sender=Refund)


class CreditQuesrySet(models.QuerySet):
    def get_customer_credit(self, customer_id=None):
        if customer_id is None or customer_id == "":
            return self.all()
        return self.filter(customer_id__exact=customer_id)


class CreditManager(models.Manager):
    def get_queryset(self):
        return CreditQuesrySet(self.model, using=self._db)

    def get_customer_credit(self, customer_id=None):
        return self.get_queryset().get_customer_credit(customer_id=customer_id)


class Credit(models.Model):
    customer = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="credits"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CreditManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["customer"], name="unique_customer_credit")
        ]
        indexes = [models.Index(fields=["customer"])]

    def __str__(self) -> str:
        return f"{self.customer}, {self.amount}"


class PaymentGateWay(models.Model):
    name = models.CharField(
        max_length=250, unique=True, help_text="The name of the payment gateway."
    )
    description = models.TextField(help_text="A description of the payment gateway.")
    status = models.CharField(
        max_length=10,
        choices=[("active", "Active"), ("inactive", "Inactive")],
        help_text="The status of the payment gateway.",
    )
    default = models.BooleanField(
        default=False, help_text="Whether this payment gateway is the default gateway."
    )

    class Meta:
        verbose_name = "Payment Gateway"
        verbose_name_plural = "Payment Gateways"

    def __str__(self) -> str:
        """
        Returns the name of the payment gateway as a string.
        """
        return f"{self.name}-{self.status}"


class Payment(models.Model):
    subscriber = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        help_text="The user who made the payment.",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="The amount of the payment."
    )
    gateway = models.ForeignKey(
        PaymentGateWay,
        on_delete=models.PROTECT,
        help_text="The payment gateway used for the payment.",
    )
    status = models.CharField(
        max_length=10,
        choices=[("success", "Success"), ("failed", "Failed"), ("pending", "Pending")],
        help_text="The status of the payment.",
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the payment was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The date and time the payment was last updated."
    )
    transaction_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="The ID of the payment transaction.",
    )
    details = models.TextField(
        blank=True, null=True, help_text="Additional details about the payment."
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        help_text="The currency used for the payment.",
    )
    failed_reason = models.TextField(
        blank=True, null=True, help_text="The reason for a failed payment."
    )


class PaymentHandler:
    class PaymentHandler:
        def __init__(self, payment_gateway):
            if payment_gateway is None:
                raise ValueError("Payment gateway is not available.")
            self.payment_gateway = payment_gateway
            self.logger = logging.getLogger(__name__)

        def process_payment(self, payment, amount):
            """
            Process a payment through the payment gateway.
            :param payment: The Payment object representing the payment.
            :param amount: The amount of the payment.
            :return: The result of the payment processing.
            """
            if payment is None:
                return {"success": False, "message": "Payment object is None"}
            if amount <= 0:
                return {
                    "success": False,
                    "message": "Payment amount must be greater than zero.",
                }
            try:
                # Code to communicate with the payment gateway API and process the payment goes here
                result = {"success": True, "message": "Payment processed successfully."}
            except Exception as e:
                result = {"success": False, "message": str(e)}
            self.logger.info(
                f"Payment processed successfully for payment {payment.id} with amount {amount}"
            )
            return result

        def refund_payment(self, payment, amount):
            """
            Refund a payment through the payment gateway.
            :param payment: The Payment object representing the payment.
            :param amount: The amount of the refund.
            :return: The result of the refund processing.
            """
            if payment is None:
                return {"success": False, "message": "Payment object is None"}
            if amount <= 0:
                return {
                    "success": False,
                    "message": "Refund amount must be greater than zero.",
                }
            try:
                # Code to communicate with the payment gateway API and process the refund goes here
                result = {"success": True, "message": "Refund processed successfully."}
            except Exception as e:
                result = {"success": False, "message": str(e)}
            self.logger.info(
                f"Refund processed successfully for payment {payment.id} with amount {amount}"
            )
            return result
