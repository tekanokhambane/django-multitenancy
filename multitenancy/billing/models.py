from decimal import Decimal
from django.db import models
from multitenancy.subscriptions.models import Subscription

from django.conf import settings

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


class Refund(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()


class Credit(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

