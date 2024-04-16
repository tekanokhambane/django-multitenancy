from rest_framework import serializers

from multitenancy.users.models import TenantUser
from multitenancy.users.serializers import UserSerializer
from .models import Invoice, Credit, Payment, Refund, PaymentGateWay
from multitenancy.subscriptions.serializers import SubscriptionSerializer


class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateWay
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    subscriber = UserSerializer(many=False)
    gateway = PaymentGatewaySerializer(many=False)
    class Meta:
        model = Payment
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(many=False)
    class Meta:
        model = Invoice
        fields = ["id", "subscription", "date_created", "due_date", "invoice_number", "amount", "credit_used", "payment_method", "status", "notes", "pdf"]



class RefundSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(many=False)
    class Meta:
        model = Refund
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