from rest_framework import serializers
from .models import Plan, ProductFeature, Subscription, ProductType

class  ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ["id", "name"]

class PlanSerialiser(serializers.ModelSerializer):
    features = ProductFeatureSerializer(many=True)
    class Meta:
        model = Plan
        fields = ["id","name", "description", "price", "price_weekly", "price_quartely", "price_annually", "features", "slug"]


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "name"]

class SubscriptionSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer(many=False)
    class Meta:
        model = Subscription
        fields = ['id', 'cycle', 'subscription_duration', 'start_date', 'end_date', 'created_date', 'renewal_date', 'reference', 'last_updated', 'product_type', 'reason', 'status',]