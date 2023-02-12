import unittest
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse, reverse_lazy
from tenant_users.permissions.models import UserTenantPermissions
from multitenancy.admin.views.adminViews import (
    AdminIndexView, 
    )
from multitenancy.apps.models import Tenant

from multitenancy.apps.views import (
    TenantListView, 
    UpdateTemplateView,
    CustomerTenantListView,
    CreateTemplateView,
    TemplateListView,
    DeleteTemplateView
    )
from multitenancy.subscriptions.views import (
    CreatePlanView, 
    PlanDetailView,
    PlanListView,
)
from multitenancy.users.models import TenantUser


class TenantTemplateViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.tenant_data = {
            'name': 'tenant1',
            'slug': 'tenant1',
            'type': 'premium',
        }
        self.new_tenant_data = {
            'type': 'business',
        }
        
    def test__templatelist_view(self):
        self.user = TenantUser.objects.get(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc123@email.com', 
            type='Admin',
            is_active=True
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/templates/')
        request.user = self.user
        response = TemplateListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_get_create_template_view(self):
        self.user = TenantUser.objects.get(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc123@email.com', 
            type='Admin',
            is_active=True
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/templates/create/')
        request.user = self.user
        response = CreateTemplateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertIn('_auth_user_id', self.client.session)

    
    def test_post_create_temaple_view(self):
        self.user = TenantUser.objects.get(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc123@email.com', 
            type='Admin',
            is_active=True
            )
        self.client.force_login(user=self.user)
        request = self.factory.post('/admin/template/create/', data=self.tenant_data)
        request.user = self.user
        response = CreateTemplateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_create_template_view_authenticated(self):
        self.user = TenantUser.objects.get(
            email='AnonymousUser', 
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/templates/create/')
        request.user = self.user
        response = AdminIndexView.as_view()(request)
        
        self.assertEqual(response.status_code, 404)

    def test_update_template_view(self):
        self.user = TenantUser.objects.get(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc123@email.com', 
            type='Admin',
            is_active=True
            )
        
        self.client.force_login(user=self.user)
        self.tenant = Tenant.objects.get(
            name='tenant1', 
        )
        request = self.factory.post(f'/admin/templates/{self.tenant.id}/update', data=self.new_tenant_data)
        request.user = self.user
        response = UpdateTemplateView.as_view()(request, pk=self.tenant.id)
        self.assertEqual(response.status_code, 200)


    def test_update_template_unauthenticateduser_view(self):
        self.user = TenantUser.objects.get(
            email='AnonymousUser', 
            )
        self.client.force_login(user=self.user)
        self.tenant = Tenant.objects.get(
            name='tenant1', 
        )
        request = self.factory.post(f'/admin/templates/{self.tenant.id}/update', data=self.new_tenant_data)
        request.user = self.user
        response = AdminIndexView.as_view()(request, pk=self.tenant.id)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_template_view(self):
        self.user = TenantUser.objects.get(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc123@email.com', 
            type='Admin',
            is_active=True
            )
        
        self.client.force_login(user=self.user)
        self.tenant = Tenant.objects.get(
            name='tenant1', 
        )
        request = self.factory.delete(f'/admin/templates/{self.tenant.id}/delete')
        request.user = self.user
        response = DeleteTemplateView.as_view()(request, pk=self.tenant.id)
        self.assertEqual(response.status_code, 302)

    def test_delete_template_unauthenticateduser_view(self):
        self.user = TenantUser.objects.get(
            email='AnonymousUser', 
            )
        self.client.force_login(user=self.user)
        self.tenant = Tenant.objects.get(
            name='tenant1', 
        )
        request = self.factory.delete(f'/admin/templates/{self.tenant.id}/delete')
        request.user = self.user
        response = DeleteTemplateView.as_view()(request, pk=self.tenant.id)
        self.assertEqual(response.status_code, 302)
