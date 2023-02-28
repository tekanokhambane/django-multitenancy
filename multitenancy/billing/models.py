from decimal import Decimal
from django.conf import settings
from django.db import models
from multitenancy.subscriptions.models import Subscription

from django.conf import settings
from django.db.models import Q

class InvoiceQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query =="":
                return self.all()
        lookups = Q(subscription__product_type__name__icontains=query) | Q(id__exact=query) | Q(invoice_number__exact=query)
        return self.filter(lookups)
    
    def filter_by_id(self, id=None):
            if id is None or id =="":
                return self.all()
            return self.filter(id__exact=id)
    
    def get_due_date(self, date=None):
        if date is None or date =="":
                return self.all()
        return self.filter(due_date__exact=date)
    
    def filter_date_range(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
              return self.all()
        return self.filter(date_created__range=(start_date, end_date))
        
    def get_status(self, status):
        if status is None or status =="":
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
         return self.get_queryset().filter_date_range(start_date=start_date, end_date=end_date)
    
    def get_status(self, status):
        return self.get_queryset().get_status(status=status)

class Invoice(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    invoice_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_used = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=[("paid", "Paid"), ("unpaid", "Unpaid"),("pending", "Pending"),("cancelled", "Cancelled"),("refunded", "Refunded")])
    notes = models.TextField(blank=True)
    pdf = models.FileField(upload_to='invoices/')
    objects = InvoiceManager()

    class Meta:
        ordering = ['-date_created']

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
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    objects = RefundManager()

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"Invoice -{self.invoice.pk}, Amount: {self.amount}"

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
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CreditManager()

    def __str__(self) -> str:
        return f"{self.customer}, {self.amount}"


class PaymentGateWay(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[("active", "Active"), ("inactive", "Inactive")])
    default = models.BooleanField(default=False)


class Payment(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway = models.ForeignKey(PaymentGateWay, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=[("success", "Success"), ("failed", "Failed"), ("pending", "Pending")])

class PaymentHandler:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def process_payment(self, payment, amount):
        """
        Process a payment through the payment gateway.
        :param payment: The Payment object representing the payment.
        :param amount: The amount of the payment.
        :return: The result of the payment processing.
        """
        # Code to communicate with the payment gateway API and process the payment goes here
        result = {'success': True, 'message': 'Payment processed successfully.'}
        return result

    def refund_payment(self, payment, amount):
        """
        Refund a payment through the payment gateway.
        :param payment: The Payment object representing the payment.
        :param amount: The amount of the refund.
        :return: The result of the refund processing.
        """
        # Code to communicate with the payment gateway API and process the refund goes here
        result = {'success': True, 'message': 'Refund processed successfully.'}
        return result


