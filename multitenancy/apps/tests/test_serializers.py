from rest_framework.test import APITestCase
from ..serializers import TenantSerializer
from multitenancy.subscriptions.models import Plan, Subscription

class TenantSerializerTestCase(APITestCase):
    def setUp(self):
        self.plan = Plan.objects.create(name="tenant")
        self.subscription = Subscription.objects.create()
        self.data = {
            'name': 'tenant_serialized',
            'type': 'personal',
            'is_template': False,
            'plan': self.plan,
            'subscription':self.subscription,
            'description': 'Test serializer',
            'on_trail': True,
            'trail_duration': 30,
        }

    def test_serializer_with_valid_data(self):
        serializer = TenantSerializer(data=self.data)# type: ignore        
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

    