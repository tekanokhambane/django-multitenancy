from django.db import models
from multitenancy.subscriptions.models import Subscription
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
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    order_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[("completed", "Completed"), ("failed", "Failed")])
    payment_method = models.CharField(max_length=50)
    shipping_address = models.TextField()
    billing_address = models.TextField()
    notes = models.TextField(blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)