import unittest
from django.test import TestCase, Client
from multitenancy.apps.models import Tenant, Domain
from multitenancy.subscriptions.models import Subscription
from multitenancy.users.models import Admin, Customer, TenantUser
from tenant_users.permissions.models import UserTenantPermissions
from multitenancy.utils import create_public_tenant

class TestTenant(unittest.TestCase):
    def  setUp(self) -> None:
        self.client = Client()
        
    
    def test_start_trail(self):
        public_user = TenantUser.objects.create(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='public@email.com', 
            type='Admin',
            is_active=True
            )
        #Create public tenant
        
        public_tenant = create_public_tenant("localhost", "tkhambane@gmail.com", "publicuser123")
        
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
        subscription = Subscription.objects.create()
        tenant = Tenant.objects.create(name="Test Tenant", type="personal", is_template=False, description="Test tenant for testing purposes", owner=user, schema_name='tenant1', subscription=subscription)
        domain = Domain.objects.create(domain="domain1.com", tenant=tenant, is_primary=True)
        tenant.add_user(user, is_superuser=True, is_staff=True)
        tenant.auto_create_schema = False
        tenant.save()
        
        self.assertFalse(tenant.subscription.is_active)
        self.assertEqual(tenant.name, "Test Tenant")
        self.assertEqual(tenant.type, "personal")
        self.assertFalse(tenant.is_template)
        self.assertEqual(tenant.description, "Test tenant for testing purposes")
        self.assertFalse(tenant.on_trial)

        # Start the trail for the tenant
        tenant.start_trail()
        self.assertTrue(tenant.subscription.is_active)
        self.assertTrue(tenant.on_trial)
        self.assertIsNotNone(tenant.trail_duration)

        # Try to start the trail again
        tenant.start_trail()
        self.assertTrue(tenant.on_trial)
        self.assertEquals(30,tenant.trail_duration)


    def test_end_trail(self):
        
        user = TenantUser.objects.create(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc2@email.com', 
            type='Customer',
            is_active=True
            )
        subscription = Subscription.objects.create()
        tenant = Tenant.objects.create(name="Test Tenant", type="personal", is_template=False,
                                        description="Test tenant for testing purposes",
                                          owner=user, schema_name='tenant2', subscription=subscription)
        domain = Domain.objects.create(domain="domain2.com", tenant=tenant, is_primary=True)
        tenant.add_user(user, is_superuser=True, is_staff=True)
        tenant.auto_create_schema = False
        tenant.save()
        # End the trail
        tenant.end_trail()
        self.assertFalse(tenant.on_trial)
        self.assertEqual(0,tenant.trail_duration)
        
    def test_trail_days_start(self):
        user = TenantUser.objects.create(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc3@email.com', 
            type='Customer',
            is_active=True
            )
        subscription = Subscription.objects.create()
        tenant = Tenant.objects.create(name="Test Tenant", type="personal", is_template=False,
                                        description="Test tenant for testing purposes", 
                                        owner=user, schema_name='tenant3', on_trial=True, 
                                        trail_duration=30, subscription=subscription)
        domain = Domain.objects.create(domain="domain3.com", tenant=tenant, is_primary=True)
        tenant.add_user(user, is_superuser=True, is_staff=True)
        tenant.auto_create_schema = False
        tenant.save()
        # Check trail days
        tenant.trail_days_left()
        self.assertTrue(tenant.on_trial)
        self.assertEqual(30,tenant.trail_duration)
        

    def test_trail_days_end(self):
        user = TenantUser.objects.create(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc4@email.com', 
            type='Customer',
            is_active=True
            )
        subscription = Subscription.objects.create()
        tenant = Tenant.objects.create(name="Test Tenant", type="personal", 
                                       is_template=False, description="Test tenant for testing purposes", 
                                       owner=user, schema_name='tenant4', 
                                       on_trial=True, trail_duration=30, subscription=subscription)
        domain = Domain.objects.create(domain="domain4.com", tenant=tenant, is_primary=True)
        tenant.add_user(user, is_superuser=True, is_staff=True)
        tenant.auto_create_schema = False
        tenant.save()
        tenant.trail_duration = 0
        tenant.save()
        # Check trail days
        tenant.trail_days_left()
        self.assertFalse(tenant.on_trial)
        self.assertEqual(0,tenant.trail_duration)
    
    