from django.core.validators import MinValueValidator
import datetime
from django.db import models
from django.conf import settings
from multitenancy.subscriptions.models import Subscription
from multitenancy.address.models import Address
class Coupon(models.Model):
    """
    Represents a model for a coupon in a Django application.

    Fields:
    - code (CharField): Coupon code (max length: 15, unique).
    - discount (DecimalField): Discount amount (max digits: 10, decimal places: 2, minimum value: 0).
    - start_date (DateField): Start date of coupon validity (default: current date).
    - end_date (DateField): End date of coupon validity (default: current date).
    - usage_limit (PositiveIntegerField): Maximum number of times the coupon can be used (minimum value: 0).
    - is_active (BooleanField): Activation status of the coupon (default: True).
    - minimum_order_amount (DecimalField): Minimum order amount required to use the coupon (max digits: 10, decimal places: 2, minimum value: 0).
    """

    code = models.CharField(max_length=15, unique=True, help_text="Coupon code")
    discount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Discount amount")
    start_date = models.DateField(default=datetime.date.today, help_text="Start date of coupon validity")
    end_date = models.DateField(default=datetime.date.today, help_text="End date of coupon validity")
    usage_limit = models.PositiveIntegerField(validators=[MinValueValidator(0)], help_text="Maximum number of times coupon can be used")
    is_active = models.BooleanField(default=True, help_text="Whether the coupon is currently active")
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Minimum order amount required to use the coupon")
    redeem_by = models.DateField(default=datetime.date.today, help_text="Date by which the coupon must be redeemed")
    usage_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], help_text="Number of times the coupon has been used")
    # the valid_for field will have to be connected to a Product model
    # valid_for = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True) 

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    order_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[("completed", "Completed"), ("failed", "Failed")])
    payment_method = models.CharField(max_length=50)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.order_number


    def get_total_amount(self):
        """
        Calculate and return the total amount of the order.
        """
        return self.amount

    def get_status_display(self):
        """
        Return the display value of the order status.
        """
        return dict(self.status.choices).get(self.status)

    def get_payment_method_display(self):
        """
        Return the display value of the payment method.
        """
        return self.payment_method

    def get_billing_address(self):
        """
        Return the billing address associated with the order.
        """
        return self.billing_address

    def get_notes(self):
        """
        Return any additional notes or instructions for the order.
        """
        return self.notes

    def get_coupon(self):
        """
        Return the coupon associated with the order.
        """
        return self.coupon

    def set_coupon(self, coupon):
        """
        Set the coupon associated with the order.
        """
        self.coupon = coupon

    def remove_coupon(self):
        """
        Remove the coupon associated with the order.
        """
        self.coupon = None

    def is_completed(self):
        """
        Check if the order is completed.
        """
        return self.status == "completed"

    def is_failed(self):
        """
        Check if the order is failed.
        """
        return self.status == "failed"


class OrderItem(models.Model):
    """
    Represents an item in an order, associating a subscription with an order.
    """

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)