from rest_framework import serializers

from multitenancy.users.models import TenantUser
from .models import Invoice, Credit, Refund
from multitenancy.subscriptions.serializers import SubscriptionSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(many=False)
    class Meta:
        model = Invoice
        fields = ["id", "subscription", "date_created", "due_date", "invoice_number", "amount", "credit_used", "payment_method", "status", "notes", "pdf"]



class RefundSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(many=False)
    class Meta:
        model = Credit
        fields = "__all__"


class UserDropdownField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [(user.id, user) for user in TenantUser.objects.filter().exclude(type="Admin").exclude(type="Staff").exclude(email="AnonymousUser")]
        super().__init__(*args, **kwargs)


class CreditSerializer(serializers.ModelSerializer):
    customer = UserDropdownField()
    class Meta:
        model = Credit
        fields = "__all__"