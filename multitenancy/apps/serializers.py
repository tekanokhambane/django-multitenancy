from rest_framework import serializers
from multitenancy.subscriptions.serializers import  SubscriptionSerializer
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(many=False)
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'type', 'is_template', 'plan', 'description', 'subscription', 'trail_duration', 'on_trial', 'created', 'modified']