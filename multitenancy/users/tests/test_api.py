import unittest

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from multitenancy.users.models import Customer, Staff, TenantUser

class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = TenantUser.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='password123'
        )
        self.admin = TenantUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
            type='Admin'
        )

    def test_customer_list_with_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, 403)

    def test_customer_list_with_admin_user(self):
        self.client.force_login(user=self.admin)
        response = self.client.get('/api/customer/')
        self.assertEqual(response.status_code, 200)

    def test_staff_list_with_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/staff/')
        self.assertEqual(response.status_code, 403)

    def test_staff_list_with_admin_user(self):
        self.client.force_login(user=self.admin)
        response = self.client.get('/api/staff/')
        self.assertEqual(response.status_code, 200)

    def test_customer_update_with_admin_user(self):
        self.customer = Customer.objects.create(
            username='customerSerializer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='customeSerializer@email.com', 
        )
        self.client.force_login(user=self.admin)
        response = self.client.put(f'/api/customers/{self.customer.pk}',data={"username":"scustomer"})
        self.assertEqual(response.status_code, 200)

    def test_customer_update_with_authenticated_user(self):
        self.customer = Customer.objects.create(
            username='customerFailSerializer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='customerFailSerializer@email.com', 
        )
        self.client.force_login(user=self.user)
        response = self.client.put(f'/api/customers/{self.customer.pk}', data={"username":"customerfail"})
        self.assertEqual(response.status_code, 403)

    def test_customer_detail_with_admin_user(self):
        self.customer = Customer.objects.create(
            username='customerdetailSerializer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='customerdetailSerializer@email.com', 
        )
        self.client.force_login(user=self.admin)
        response = self.client.get(f'/api/customers/{self.customer.pk}')
        self.assertEqual(response.status_code, 200)

    def test_customer_detail_with_authenticated_user(self):
        self.customer = Customer.objects.get(
            username='customerdetailSerializer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='customerdetailSerializer@email.com', 
        )
        self.client.force_login(user=self.user)
        response = self.client.get(f'/api/customers/{self.customer.pk}')
        self.assertEqual(response.status_code, 403)

    def test_staff_detail_with_admin_user(self):
        self.staff = Staff.objects.get(
            username='staffSerializer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='staffSerializer@email.com', 
        )
        self.client.force_login(user=self.admin)
        response = self.client.get(f'/api/staff/{self.customer.pk}')
        self.assertEqual(response.status_code, 200)

    def test_staff_detail_with_authenticated_user(self):
        self.staff = Staff.objects.create(
            username='staffSerializer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='staffSerializer@email.com', 
        )
        self.client.force_login(user=self.user)
        response = self.client.get(f'/api/staff/{self.staff.pk}')
        self.assertEqual(response.status_code, 403)

    def test_staff_update_with_admin_user(self):
        self.staff = Staff.objects.get(
            username='staffSerializer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='staffSerializer@email.com', 
        )
        self.client.force_login(user=self.user)
        response = self.client.put(f'/api/staff/{self.staff.pk}',data={"username":"sstaff"})
        self.assertEqual(response.status_code, 200)

    def test_staff_update_with_authenticated_user(self):
        self.staff = Staff.objects.create(
            username='staffFailSerializer', 
            password="password", 
            first_name='abc123', 
            last_name='khamban', 
            email='staffFailSerializer@email.com', 
        )
        self.client.force_login(user=self.user)
        response = self.client.put(f'/api/staff/{self.staff.pk}', data={"username":"stafffail"})
        self.assertEqual(response.status_code, 403)
