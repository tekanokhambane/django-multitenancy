from rest_framework import serializers
from .models import Plan, ProductFeature

class  ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ["id", "name"]

class PlanSerialiser(serializers.ModelSerializer):
    features = ProductFeatureSerializer(many=True)
    class Meta:
        model = Plan
        fields = ["id","name", "description", "price", "price_weekly", "price_quartely", "price_annually", "features"]

    # def get_feature(self, feature):
