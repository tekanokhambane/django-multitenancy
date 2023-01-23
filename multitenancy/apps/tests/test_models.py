from django.test import TestCase, Client
from multitenancy.apps.models import Tenant, Domain
from multitenancy.users.models import Admin, Customer, TenantUser
class TestTenant(TestCase):
    def  setUp(self) -> None:
        self.client = Client()
    
    def test_start_trail(self):
        # Create a tenant
        user = TenantUser.objects.create(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc@email.com', 
            type='Customer',
            is_active=True
            )
        tenant = Tenant.objects.create(name="Test Tenant", type="personal", is_template=False, description="Test tenant for testing purposes", owner=user, schema_name='tenant1')
        domain = Domain.objects.create(domain="domain1.com", tenant=tenant, is_primary=True)
        self.assertEqual(tenant.name, "Test Tenant")
        self.assertEqual(tenant.type, "personal")
        self.assertFalse(tenant.is_template)
        self.assertEqual(tenant.description, "Test tenant for testing purposes")
        self.assertFalse(tenant.on_trial)

        # Start the trail for the tenant
        tenant.start_trail()
        self.assertTrue(tenant.on_trial)
        self.assertIsNotNone(tenant.trail_duration)

        # Try to start the trail again
        tenant.start_trail()
        self.assertTrue(tenant.on_trial)
        self.assertIsNotNone(tenant.trail_duration)

        # Create another tenant for the same user
        tenant2 = Tenant.objects.create(name="Test Tenant 2", type="premium", is_template=True, description="Test tenant for testing purposes", owner=user, schema_name="tenant2")
        domain2 = Domain.objects.create(domain="domain2.com", tenant=tenant2, is_primary=True)
        self.assertEqual(tenant2.name, "Test Tenant 2")
        self.assertEqual(tenant2.type, "premium")
        self.assertTrue(tenant2.is_template)
        self.assertEqual(tenant2.description, "Test tenant for testing purposes")
        self.assertFalse(tenant2.on_trial)

        # Check the trail for the second tenant
        
        self.assertFalse(tenant2.on_trial)
        self.assertIsNone(tenant2.trail_duration)

        # Clean up
        # tenant.delete_tenant()
        # tenant2.delete_tenant()
