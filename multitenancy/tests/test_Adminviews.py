import unittest
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse, reverse_lazy
from tenant_users.permissions.models import UserTenantPermissions
from multitenancy.admin.views.adminViews import (
    AdminIndexView, 
    )
from multitenancy.settings.views import SettingsIndexView
from multitenancy.apps.views import TenantListView
from multitenancy.subscriptions.views import (
    CreatePlanView, 
    PlanDetailView,
    PlanListView,
)
from multitenancy.users.views import(
    CreateCustomerView,
    DeleteCustomerView,
    CustomerListView,
    UpdateCustomerView,
)
from multitenancy.subscriptions.models import Plan
from multitenancy.users.models import Admin, Customer, TenantUser
from  multitenancy.admin.decorators import allowed_users
from multitenancy.users.forms import CustomerForm, CustomerUpdateForm
from multitenancy.subscriptions.forms import PlanForm
from multitenancy.admin import urls



class AdminViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.customer_data = {
            'first_name': 'customer',
            'last_name': 'test',
            'username': 'tcustomer',
            'password': 'password1234',
            'email': 'customer@example.com',
        }
        self.new_customer_data = {
            'first_name': 'customer1',
            'username': 'testcustomer',
        }
        self.customer_obj = Customer.objects.first()


    
    def test_admin_index_view(self):
        self.user = TenantUser.objects.create(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='abc123@email.com', 
            type='Admin',
            is_active=True
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/')
        request.user = self.user
        response = AdminIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_admin_index_view_authenticated(self):
        self.user = TenantUser.objects.get(
            
            email='AnonymousUser', 
            
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/')
        request.user = self.user
        response = AdminIndexView.as_view()(request)
        
        self.assertEqual(response.status_code, 404)
    

    

     
    

    def test_subscriptionlist_index_view(self):
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
        request = self.factory.get('/admin/tenants/')
        request.user = self.user
        response = TenantListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_subscriptionlist_index_view_authenticated(self):
        self.user = TenantUser.objects.get(
            
            email='AnonymousUser', 
            
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/tenants/')
        request.user = self.user
        response = TenantListView.as_view()(request)
        
        self.assertEqual(response.status_code, 404)



    def test_customerlist_index_view(self):
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
        request = self.factory.get('/admin/customers/')
        request.user = self.user
        response = CustomerListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_customerlist_index_view_authenticated(self):
        self.user = TenantUser.objects.get(
            
            email='AnonymousUser', 
            
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/customers/')
        request.user = self.user
        response = CustomerListView.as_view()(request)
        
        self.assertEqual(response.status_code, 404)


    def test_settings_index_view(self):
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
        request = self.factory.get('/admin/settings/')
        request.user = self.user
        response = SettingsIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_settings_index_view_authenticated(self):
        self.user = TenantUser.objects.get(
            
            email='AnonymousUser', 
            
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/settings/')
        request.user = self.user
        response = SettingsIndexView.as_view()(request)
        
        self.assertEqual(response.status_code, 404)


    def test_planlist_index_view(self):
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
        request = self.factory.get('/admin/settings/plans/')
        request.user = self.user
        response = PlanListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_planlist_view_authenticated(self):
        self.user = TenantUser.objects.get(
            
            email='AnonymousUser', 
            
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/settings/plans/')
        request.user = self.user
        response = PlanListView.as_view()(request)
        
        self.assertEqual(response.status_code, 404)


    