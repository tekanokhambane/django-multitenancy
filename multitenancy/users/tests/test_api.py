import unittest

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from multitenancy.users.models import TenantUser

class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = TenantUser.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='password123'
        )

    def test_customer_list_with_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, 403)

    def test_customer_list_with_admin_user(self):
        admin = TenantUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.client.force_login(user=admin)
        response = self.client.get('/api/customer/')
        self.assertEqual(response.status_code, 200)

    def test_staff_list_with_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/staff/')
        self.assertEqual(response.status_code, 403)

    def test_staff_list_with_admin_user(self):
        admin = TenantUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.client.force_login(user=admin)
        response = self.client.get('/api/staff/')
        self.assertEqual(response.status_code, 200)

    def test_customer_detail_with_admin_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/customers/2')
        self.assertEqual(response.status_code, 200)

    def test_customer_detail_with_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/customers/2')
        self.assertEqual(response.status_code, 403)

    def test_staff_detail_with_admin_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/staff/2')
        self.assertEqual(response.status_code, 200)

    def test_staff_detail_with_authenticated_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/staff/2')
        self.assertEqual(response.status_code, 403)
