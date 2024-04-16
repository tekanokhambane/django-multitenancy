import unittest
from django.test import RequestFactory, TestCase, Client
from multitenancy.admin.views.adminViews import (
    AdminIndexView,
)
from multitenancy.users.views import (
    CreateCustomerView,
    CreateStaffView,
    DeleteCustomerView,
    CustomerListView,
    UpdateCustomerView,
    UpdateStaffView,
)
from multitenancy.subscriptions.models import Plan
from multitenancy.users.models import Admin, Customer, Staff, TenantUser
from multitenancy.admin.decorators import allowed_users
from multitenancy.users.forms import CustomerForm, CustomerUpdateForm
from multitenancy.subscriptions.forms import PlanForm
from multitenancy.admin import urls


class CustomerViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.customer_data = {
            "first_name": "customer",
            "last_name": "test",
            "username": "tcustomer",
            "password": "password1234",
            "email": "customer@example.com",
        }
        self.new_customer_data = {
            "first_name": "customer1",
            "username": "testcustomer",
        }
        self.customer_obj = Customer.objects.first()

    def test_get_create_customer_view(self):
        self.user = TenantUser.objects.create(
            username="admin",
            password="password",
            first_name="abc123",
            last_name="khamban",
            email="abc123@email.com",
            type="Admin",
            is_active=True,
        )

        self.client.force_login(user=self.user)
        request = self.factory.get("/admin/customers/create/")
        request.user = self.user
        response = CreateCustomerView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get("_auth_user_id"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_post_create_customer_view(self):
        self.user = TenantUser.objects.create(
            username="admin",
            password="password",
            first_name="abc123",
            last_name="khamban",
            email="abc123@email.com",
            type="Admin",
            is_active=True,
        )
        self.client.force_login(user=self.user)
        request = self.factory.post("/admin/customers/create/", data=self.customer_data)
        request.user = self.user
        response = CreateCustomerView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get("_auth_user_id"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_get_create_customer_view_authenticated(self):
        self.user = TenantUser.objects.get(
            email="AnonymousUser",
        )

        self.client.force_login(user=self.user)
        request = self.factory.get("/admin/customers/create/")
        request.user = self.user
        response = AdminIndexView.as_view()(request)

        self.assertEqual(response.status_code, 404)


#     def test_update_customer_view(self):
#         self.user = TenantUser.objects.get(
#             username='admin',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='abc123@email.com',
#             type='Admin',
#             is_active=True
#             )

#         self.client.force_login(user=self.user)
#         self.customer = Customer.objects.create(
#             username='customer',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='customer123@email.com',
#         )
#         request = self.factory.post(f'/admin/customers/{self.customer.id}/update', data=self.new_customer_data)
#         request.user = self.user
#         response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
#         self.assertEqual(response.status_code, 200)


#     def test_update_customer_unauthenticateduser_view(self):
#         self.user = TenantUser.objects.get(
#             email='AnonymousUser',
#             )

#         self.client.force_login(user=self.user)
#         self.customer = Customer.objects.create(
#             username='customer',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='customer123e@email.com',
#         )
#         request = self.factory.post(f'/admin/customers/{self.customer.id}/update', data=self.new_customer_data)
#         request.user = self.user
#         response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
#         self.assertEqual(response.status_code, 404)


#     def test_update_customer_authenticatednonadminuser_view(self):
#         self.user = TenantUser.objects.create(
#             username='admin',
#             password="password",
#             first_name='abc123',
#             last_name='staff',
#             email='staff1@email.com',
#             type='Staff',
#             is_active=True
#             )

#         self.client.force_login(user=self.user)
#         self.customer = Customer.objects.create(
#             username='customer',
#             password="password",
#             first_name='abc123',
#             last_name='customer1',
#             email='customer12344@email.com',
#         )
#         request = self.factory.post(f'/admin/customers/{self.customer.id}/update', data=self.new_customer_data)
#         request.user = self.user
#         response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
#         self.assertEqual(response.status_code, 404)

#     def test_delete_customer_view(self):
#         self.user = TenantUser.objects.get(
#             username='admin',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='abc123@email.com',
#             type='Admin',
#             is_active=True
#             )

#         self.client.force_login(user=self.user)
#         self.customer = Customer.objects.create(
#             username='customer',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='customer12345@email.com',
#         )
#         request = self.factory.delete(f'/admin/customers/{self.customer.id}/delete')
#         request.user = self.user
#         response = DeleteCustomerView.as_view()(request, pk=self.customer.id)
#         self.assertEqual(response.status_code, 302)

#     def test_delete_customer_unauthenticateduser_view(self):
#         self.user = TenantUser.objects.get(
#             email='AnonymousUser',
#             )

#         self.client.force_login(user=self.user)
#         self.customer = Customer.objects.create(
#             username='customer',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='customer1234@email.com',
#         )
#         request = self.factory.delete(f'/admin/customers/{self.customer.id}/delete')
#         request.user = self.user
#         response = DeleteCustomerView.as_view()(request, pk=self.customer.id)
#         self.assertEqual(response.status_code, 404)


#     def test_customerlist_index_view(self):
#         self.user = TenantUser.objects.get(
#             username='admin',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='abc123@email.com',
#             type='Admin',
#             is_active=True
#             )

#         self.client.force_login(user=self.user)
#         request = self.factory.get('/admin/customers/')
#         request.user = self.user
#         response = CustomerListView.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(self.client.session.get('_auth_user_id'))
#         self.assertIn('_auth_user_id', self.client.session)

#     def test_customerlist_index_view_authenticated(self):
#         self.user = TenantUser.objects.get(

#             email='AnonymousUser',

#             )

#         self.client.force_login(user=self.user)
#         request = self.factory.get('/admin/customers/')
#         request.user = self.user
#         response = CustomerListView.as_view()(request)

#         self.assertEqual(response.status_code, 404)

# class StaffViewsTestCase(unittest.TestCase):

#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()
#         self.staff_data = {
#             'first_name': 'staff',
#             'last_name': 'test',
#             'username': 'tstaff',
#             'password': 'password1234',
#             'email': 'staff@example.com',
#         }
#         self.new_staff_data = {
#             'first_name': 'staff1',
#             'username': 'teststaff',
#         }
#         self.staff_obj = Staff.objects.first()

#     def test_get_create_staff_view(self):
#         self.user = TenantUser.objects.get(
#             username='admin',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='abc123@email.com',
#             type='Admin',
#             is_active=True
#             )

#         self.client.force_login(user=self.user)
#         request = self.factory.get('/admin/staff/create/')
#         request.user = self.user
#         response = CreateCustomerView.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(self.client.session.get('_auth_user_id'))
#         self.assertIn('_auth_user_id', self.client.session)


#     def test_post_create_staff_view(self):
#         self.user = TenantUser.objects.get(
#             username='admin',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='abc123@email.com',
#             type='Admin',
#             is_active=True
#             )
#         self.client.force_login(user=self.user)
#         request = self.factory.post('/admin/staff/create/', data=self.staff_data)
#         request.user = self.user
#         response = CreateStaffView.as_view()(request)
#         self.assertEqual(response.status_code, 200)


#     def test_get_create_staff_view_authenticated(self):
#         self.user = TenantUser.objects.get(
#             email='AnonymousUser',
#             )

#         self.client.force_login(user=self.user)
#         request = self.factory.get('/admin/staff/create/')
#         request.user = self.user
#         response = AdminIndexView.as_view()(request)

#         self.assertEqual(response.status_code, 404)

#     def test_update_staff_view(self):
#         self.user = TenantUser.objects.get(
#             username='admin',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='abc123@email.com',
#             type='Admin',
#             is_active=True
#             )

#         self.client.force_login(user=self.user)
#         self.staff = Staff.objects.create(
#             username='staff2',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='staff123@email.com',
#         )
#         request = self.factory.post(f'/admin/custom/{self.staff.id}/update', data=self.new_staff_data)
#         request.user = self.user
#         response = UpdateStaffView.as_view()(request, pk=self.staff.id)
#         self.assertEqual(response.status_code, 200)


#     def test_update_customer_unauthenticateduser_view(self):
#         self.user = TenantUser.objects.get(
#             email='AnonymousUser',
#             )

#         self.client.force_login(user=self.user)
#         self.staff = Staff.objects.create(
#             username='staff',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='staff123e@email.com',
#         )
#         request = self.factory.post(f'/admin/staff/{self.staff.id}/update/', data=self.new_staff_data)
#         request.user = self.user
#         response = UpdateStaffView.as_view()(request, pk=self.staff.id)
#         self.assertEqual(response.status_code, 404)


#     def test_delete_customer_view(self):
#         self.user = TenantUser.objects.get(
#             username='admin',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='abc123@email.com',
#             type='Admin',
#             is_active=True
#             )

#         self.client.force_login(user=self.user)
#         self.customer = Customer.objects.create(
#             username='customer',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='customer12345@email.com',
#         )
#         request = self.factory.delete(f'/admin/customers/{self.customer.id}/delete')
#         request.user = self.user
#         response = DeleteCustomerView.as_view()(request, pk=self.customer.id)
#         self.assertEqual(response.status_code, 302)

#     def test_delete_customer_unauthenticateduser_view(self):
#         self.user = TenantUser.objects.get(
#             email='AnonymousUser',
#             )

#         self.client.force_login(user=self.user)
#         self.customer = Customer.objects.get(
#             username='customer',
#             password="password",
#             first_name='abc123',
#             last_name='khamban',
#             email='customer1234@email.com',
#         )
#         request = self.factory.delete(f'/admin/customers/{self.customer.id}/delete')
#         request.user = self.user
#         response = DeleteCustomerView.as_view()(request, pk=self.customer.id)
#         self.assertEqual(response.status_code, 404)
