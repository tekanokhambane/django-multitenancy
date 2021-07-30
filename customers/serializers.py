from rest_framework import serializers
from .models import Domain, Client
from rest_framework.fields import TimeField


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'schema_name', 'domain_url', 'name', 'owner_id'
             ]


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain', 'tenant']
