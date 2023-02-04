import unittest
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse, reverse_lazy
from tenant_users.permissions.models import UserTenantPermissions
from multitenancy.admin.views.adminViews import (
    AdminIndexView, 
    CreateCustomerView,
    CreatePlanView,
    CustomerList,
    PlanDetailView,
    PlanListView,
    SettingsIndexView,
    TenantListView, 
    UpdateCustomerView,
    DeleteCustomerView
    )
from multitenancy.subscriptions.models import Plan
from multitenancy.users.models import Admin, Customer, TenantUser
from  multitenancy.admin.decorators import allowed_users
from multitenancy.admin.forms import CustomerForm, CustomerUpdateForm, PlanForm
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
    

    def test_get_create_customer_view(self):
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
        request = self.factory.get('/admin/customers/create/')
        request.user = self.user
        response = CreateCustomerView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        self.assertIn('_auth_user_id', self.client.session)

                                              
    def test_post_create_customer_view(self):
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
        request = self.factory.post('/admin/customers/create/', data=self.customer_data)
        request.user = self.user
        response = CreateCustomerView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 3)

    def test_get_create_customer_view_authenticated(self):
        self.user = TenantUser.objects.get(
            
            email='AnonymousUser', 
            
            )
        
        self.client.force_login(user=self.user)
        request = self.factory.get('/admin/customers/create/')
        request.user = self.user
        response = AdminIndexView.as_view()(request)
        
        self.assertEqual(response.status_code, 404)
    
    def test_update_customer_view(self):
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
        self.customer = Customer.objects.create(
            username='customer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='customer123@email.com', 
        )
        request = self.factory.post(f'/admin/customers/{self.customer.id}/update', data=self.new_customer_data)
        request.user = self.user
        response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 200)

    
    def test_update_customer_unauthenticateduser_view(self):
        self.user = TenantUser.objects.get(
            email='AnonymousUser', 
            )
        
        self.client.force_login(user=self.user)
        self.customer = Customer.objects.create(
            username='customer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='customer123e@email.com', 
        )
        request = self.factory.post(f'/admin/customers/{self.customer.id}/update', data=self.new_customer_data)
        request.user = self.user
        response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 404)


    def test_update_customer_authenticatednonadminuser_view(self):
        self.user = TenantUser.objects.create(
            username='admin', 
            password="password", 
            first_name='abc123', 
            last_name='staff', 
            email='staff1@email.com', 
            type='Staff',
            is_active=True
            )
        
        self.client.force_login(user=self.user)
        self.customer = Customer.objects.create(
            username='customer', 
            password="password", 
            first_name='abc123', 
            last_name='customer1', 
            email='customer12344@email.com', 
        )
        request = self.factory.post(f'/admin/customers/{self.customer.id}/update', data=self.new_customer_data)
        request.user = self.user
        response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 404)

    def test_delete_customer_view(self):
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
        self.customer = Customer.objects.create(
            username='customer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='customer12345@email.com', 
        )
        request = self.factory.delete(f'/admin/customers/{self.customer.id}/delete')
        request.user = self.user
        response = DeleteCustomerView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 302)

    def test_delete_customer_unauthenticateduser_view(self):
        self.user = TenantUser.objects.get(
            email='AnonymousUser', 
            )
        
        self.client.force_login(user=self.user)
        self.customer = Customer.objects.create(
            username='customer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='customer1234@email.com', 
        )
        request = self.factory.delete(f'/admin/customers/{self.customer.id}/delete')
        request.user = self.user
        response = DeleteCustomerView.as_view()(request, pk=self.customer.id)
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
        response = CustomerList.as_view()(request)
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
        response = CustomerList.as_view()(request)
        
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


    def test_get_create_plan_view(self):
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
        request = self.factory.get('/admin/settings/plans/create/')
        request.user = self.user
        response = CreatePlanView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
                                              
    def test_post_create_plan_view(self):
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
        self.data= {
            "name":"basic",
            "description":"basic plan",
            "price":78,
        }
        request = self.factory.post('/admin/plans/create/', data=self.data)
        request.user = self.user
        response = CreatePlanView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        # self.assertIsInstance(respbonse.context['form'], PlanForm)
        self.assertEqual(Plan.objects.count(), 1)

    
    def test_plan_detail_view(self):
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
        self.plan = Plan.objects.create(
            name='basic',
        )
        self.request = self.factory.get(f'/settings/plans/{self.plan}/')
        self.request.user = self.user
        view = PlanDetailView.as_view()
        response = view(self.request, pk=self.plan.pk)
        self.assertEqual(response.status_code, 200)
        
