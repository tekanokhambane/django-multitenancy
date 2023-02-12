from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from multitenancy.subscriptions.models import Subscription
from ..models import Tenant
from multitenancy.users.models import TenantUser


class TenantTemplateViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = TenantUser.objects.create_user(
            username='johndoe',
            email='johndoe@eexample.com',
            password='password123'
        )
        self.admin = TenantUser.objects.create_superuser(
            username='admin',
            email='admin@gexample.com',
            password='password123',
            type='Admin'
        )

    def test_template_list_with_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/templates/')
        self.assertEqual(response.status_code, 403)

    def test_templates_list_with_admin_user(self):
        self.client.force_login(user=self.admin)
        response = self.client.get('/api/templates/')
        self.assertEqual(response.status_code, 200)

    def test_template_update_with_admin_user(self):
        subscription = Subscription.objects.create()
        self.template = Tenant.objects.create(
            name='tenantSerializer', 
            type="personal",
            slug="tenantSerializer", 
            is_template=False, 
            subscription=subscription, 
            trail_duration=30,
            on_trial=False, 
        )
        self.client.force_login(user=self.admin)
        response = self.client.put(f'/api/templates/{self.template.pk}',data={"name":"tenantTemplate"})
        self.assertEqual(response.status_code, 200)

    def test_temlate_update_with_authenticated_user(self):
        subscription = Subscription.objects.create()
        self.template = Tenant.objects.create(
            name='tenantSerializer2', 
            type="personal",
            slug="tenantSerializer2", 
            is_template=False, 
            subscription=subscription, 
            trail_duration=30,
            on_trial=False, 
        )
        self.client.force_login(user=self.user)
        response = self.client.put(f'/api/templates/{self.template.pk}', data={"name":"tenantfail"})
        self.assertEqual(response.status_code, 403)

    def test_tenant_detail_with_admin_user(self):
        self.template = Tenant.objects.get(
            type="personal",
            slug="tenantSerializer2", 
            is_template=False, 
            trail_duration=30,
            on_trial=False, 
        )
        self.client.force_login(user=self.admin)
        response = self.client.get(f'/api/templates/{self.template.pk}')
        self.assertEqual(response.status_code, 200)

    def test_template_detail_with_authenticated_user(self):
        self.template = Tenant.objects.get(
            type="personal",
            slug="tenantSerializer2", 
            is_template=False, 
            trail_duration=30,
            on_trial=False, 
        )
        self.client.force_login(user=self.user)
        response = self.client.get(f'/api/customers/{self.template.pk}')
        self.assertEqual(response.status_code, 403)