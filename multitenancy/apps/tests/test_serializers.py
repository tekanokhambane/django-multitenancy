from rest_framework.test import APITestCase
from ..serializers import TenantSerializer
from multitenancy.subscriptions.models import Plan, Subscription, get_plans

class TenantSerializerTestCase(APITestCase):
    
        

    def test_serializer_with_valid_data(self):
        
        self.subscription = Subscription.objects.create()
        self.data = {
            'name': 'tenant_serialized',
            'type': 'personal',
            'is_template': False,
            # 'plan': 2,
            'subscription':{"product_type":{"name":"tenant"},"reason":"create subscription","reference":"99d8d","status":"active","cycle":"monthly", "subscription_duration":30},
            'slug':"tenant-serialized",
            'schema_name':"tenant-serialized",
            'description': 'Test serializer',
            'on_trail': True,
            'trail_duration': 30,
        }
        serializer = TenantSerializer(data=self.data)# type: ignore      
        
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

    