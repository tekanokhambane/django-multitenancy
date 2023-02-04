from django.db import models
from django.conf import settings
from multitenancy.subscriptions.models import Subscription
from multitenancy.address.models import Address
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    usage_limit = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    redeem_by = models.DateField()
    usage_count = models.PositiveIntegerField(default=0)
    # the valid_for field will have to be connected to a Product model
    # valid_for = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True) 

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    order_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[("completed", "Completed"), ("failed", "Failed")])
    payment_method = models.CharField(max_length=50)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)


class OrderItem(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)