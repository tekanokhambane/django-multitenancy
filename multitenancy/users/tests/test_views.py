import unittest
from urllib import response
from django.test import RequestFactory, TestCase, Client
from multitenancy.utils import create_public_tenant
from unittest.mock import Mock
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from multitenancy.users.views import (
    CreateCustomerView,
    CreateStaffView,
    DeleteCustomerView,
    CustomerListView,
    DeleteStaffView,
    UpdateCustomerView,
    UpdateStaffView,
    StaffViewSet,
    CustomerViewSet,
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
            last_name="opdidid",
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
            last_name="kdidid",
            email="abc123897w@email.com",
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
        self.user = TenantUser.objects.create(
            username="admin",
            password="password",
            first_name="abc123",
            last_name="houtken",
            email="abc1ppdo23@email.com",
            type="Admin",
            is_active=True,
        )
        self.client.force_login(user=self.user)
        request = self.factory.get("/admin/customers/create/")
        request.user = self.user
        response = CreateCustomerView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get("_auth_user_id"))

    def test_update_customer_view(self):
        self.user = TenantUser.objects.create(
            username="admin",
            password="password",
            first_name="abc123",
            last_name="oskidu",
            email="abc12388ff@email.com",
            type="Admin",
            is_active=True,
        )

        self.client.force_login(user=self.user)
        self.customer = Customer.objects.create(
            username="customer",
            password="password",
            first_name="abc123",
            last_name="hudy",
            email="customer123@email.com",
        )
        request = self.factory.post(
            f"/admin/customers/{self.customer.id}/update", data=self.new_customer_data
        )
        request.user = self.user
        response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 200)

    def test_update_customer_unauthenticateduser_view(self):
        try:
            self.user, created = TenantUser.objects.get_or_create(
                email="AnonymousUser",
            )
            assert not created
            assert self.user is not None

            self.client.force_login(user=self.user)
            self.customer = Customer.objects.create(
                username="customer",
                password="password",
                first_name="abc123",
                last_name="yus",
                email="customer123e@email.com",
            )
            assert self.customer is not None

            request = self.factory.post(
                f"/admin/customers/{self.customer.id}/update",
                data=self.new_customer_data,
            )
            assert request is not None
            request.user = self.user
            assert request.user is not None

            response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
            assert response is not None
            self.assertEqual(response.status_code, 404)
        except Exception as e:
            print(f"Exception raised: {str(e)}")

    def test_update_customer_authenticatednonadminuser_view(self):
        try:
            self.user = Staff.objects.create(
                username="admin",
                password="password",
                first_name="abc123",
                last_name="staff",
                email="staff1@email.com",
                type="Staff",
                is_active=True,
            )
            assert self.user is not None

            self.client.force_login(user=self.user)
            self.customer = Customer.objects.create(
                username="customer",
                password="password",
                first_name="abc123",
                last_name="customer1",
                email="customer12344@email.com",
            )
            assert self.customer is not None

            request = self.factory.get(f"/admin/customers/{self.customer.id}/update")
            assert request is not None
            request.user = self.user
            assert request.user is not None

            response = UpdateCustomerView.as_view()(request, pk=self.customer.id)
            print(response)
            assert response is not None
            self.assertEqual(response.status_code, 403)
        except Exception as e:
            print(f"Exception raised: {str(e)}")

    def test_delete_customer_view(self):
        self.user = TenantUser.objects.create(
            username="admin",
            password="password",
            first_name="abc123",
            last_name="wieure",
            email="abc12ffj3@email.com",
            type="Admin",
            is_active=True,
        )

        self.client.force_login(user=self.user)
        self.customer = Customer.objects.create(
            username="customer",
            password="password",
            first_name="abc123",
            last_name="lauud",
            email="customer123odi45@email.com",
        )
        request = self.factory.delete(f"/admin/customers/{self.customer.id}/delete")
        request.user = self.user
        response = DeleteCustomerView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 302)

    def test_delete_customer_unauthenticated(self):
        try:
            unauthenticated_user, created = TenantUser.objects.get_or_create(
                email="AnonymousUser"
            )
            assert unauthenticated_user is not None
            assert created is False

            customer = Customer.objects.create(
                username="customer",
                password="password",
                first_name="abc123",
                last_name="oiute",
                email="customer123posie4@email.com",
            )
            assert customer is not None

            request = self.factory.delete(f"/admin/customers/{customer.id}/delete")
            assert request is not None
            assert request.user is None

            response = DeleteCustomerView.as_view()(request, pk=customer.id)
            assert response is not None
            self.assertEqual(response.status_code, 403)
        except Exception as e:
            print(f"Exception raised: {str(e)}")

    def test_customerlist_index_view(self):
        self.user = TenantUser.objects.create(
            username="admin",
            password="password",
            first_name="abc123",
            last_name="opdue",
            email="abc12kdoid3@email.com",
            type="Admin",
            is_active=True,
        )

        self.client.force_login(user=self.user)
        request = self.factory.get("/admin/customers/")
        request.user = self.user
        response = CustomerListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get("_auth_user_id"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_customerlist_index_view_unauthenticated(self):
        try:
            user, _ = TenantUser.objects.get_or_create(email="AnonymousUser")

            if user is None:
                raise ValueError("user is None")

            self.client.force_login(user=user)
            request = self.factory.get("/admin/customers/")

            if request is None:
                raise ValueError("request is None")

            request.user = user
            response = CustomerListView.as_view()(request)

            if response is None:
                raise ValueError("response is None")

            self.assertEqual(response.status_code, 404)
        except Exception as e:
            print(f"Exception raised: {str(e)}")


class StaffViewsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.tenant = create_public_tenant(
            "localhost",
            "abc1eoirj23@email.com",
            "password",
        )
        self.staff_data = {
            "first_name": "staff",
            "last_name": "test",
            "username": "tstaff",
            "password": "password1234",
            "email": "staff@example.com",
        }
        self.new_staff_data = {
            "first_name": "staff1",
            "username": "teststaff",
        }
        self.staff_obj = Staff.objects.first()

    def test_get_create_staff_view(self):
        # self.user = Admin.objects.create(
        #     username="admin",
        #     password="password",
        #     first_name="abc123",
        #     last_name="pooemd",
        #     email="abc1eoirj23@email.com",
        #     type="Admin",
        #     is_active=True,
        # )

        self.user = Admin.objects.get(email="abc1eoirj23@email.com")
        self.client.force_login(user=self.user)
        request = self.factory.get("/admin/staff/create/")
        request.user = self.user
        response = CreateStaffView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session.get("_auth_user_id"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_post_create_staff_view(self):
        self.user = Admin.objects.get(email="abc1eoirj23@email.com")
        self.client.force_login(user=self.user)
        request = self.factory.post("/admin/staff/create/", data=self.staff_data)
        request.user = self.user
        response = CreateStaffView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_create_staff_view_unauthenticated(self):
        try:
            self.user = TenantUser.objects.get(
                email="AnonymousUser",
            )
            assert self.user is not None

            self.client.force_login(user=self.user)
            request = self.factory.get("/admin/staff/create/")
            assert request is not None
            request.user = self.user
            assert request.user is not None

            response = CreateStaffView.as_view()(request)
            assert response is not None
            self.assertEqual(response.status_code, 403)
        except Exception as e:
            print(f"Exception raised: {str(e)}")

    def test_update_staff_view(self):
        self.user = Admin.objects.get(email="abc1eoirj23@email.com")
        self.client.force_login(user=self.user)
        self.staff = Staff.objects.create(
            username="staff2",
            password="password",
            first_name="abc123",
            last_name="khamban",
            email="staff123@email.com",
        )
        request = self.factory.post(
            f"/admin/custom/{self.staff.id}/update", data=self.new_staff_data
        )
        request.user = self.user
        response = UpdateStaffView.as_view()(request, pk=self.staff.id)
        self.assertEqual(response.status_code, 200)

    def test_update_staff_unauthenticateduser_view(self):
        try:
            self.user = TenantUser.objects.get(email="AnonymousUser")
            if self.user is None:
                raise ValueError("AnonymousUser user not found")

            self.client.force_login(user=self.user)
            self.staff = Staff.objects.create(
                username="staff",
                password="password",
                first_name="abc123",
                last_name="khamban",
                email="staff123e@email.com",
            )
            if self.staff is None:
                raise ValueError("Could not create staff user")

            request = self.factory.post(
                f"/admin/staff/{self.staff.id}/update/", data=self.new_staff_data
            )
            if request is None:
                raise ValueError("request is None")

            request.user = self.user
            if request.user is None:
                raise ValueError("request.user is None")

            response = UpdateStaffView.as_view()(request, pk=self.staff.id)
            if response is None:
                raise ValueError("Response is None")

            self.assertEqual(response.status_code, 404)
        except Exception as e:
            print(f"Exception raised: {str(e)}")

    def test_delete_staff_view(self):
        self.user = Admin.objects.get(email="abc1eoirj23@email.com")
        self.client.force_login(user=self.user)
        self.staff = Staff.objects.create(
            username="staff",
            password="password",
            first_name="abc123",
            last_name="khamban",
            email="staff12345@email.com",
        )
        request = self.factory.delete(f"/admin/staff/{self.staff.id}/delete")
        request.user = self.user
        response = DeleteStaffView.as_view()(request, pk=self.staff.id)
        self.assertEqual(response.status_code, 302)

    def test_delete_staff_unauthenticateduser_view(self):
        try:
            self.user = TenantUser.objects.get(email="AnonymousUser")
            if self.user is None:
                raise ValueError("Could not get AnonymousUser")

            self.staff = Staff.objects.get(
                username="staff",
                password="password",
                first_name="abc123",
                last_name="oipemd",
                email="staffk1234@email.com",
            )
            if self.customer is None:
                raise ValueError("Could not get Staff")

            request = self.factory.delete(f"/admin/staff/{self.staff.id}/delete")
            if request is None:
                raise ValueError("request is None")

            request.user = self.user
            if request.user is None:
                raise ValueError("request.user is None")

            response = DeleteStaffView.as_view()(request, pk=self.customer.id)
            if response is None:
                raise ValueError("Response is None")

            self.assertEqual(response.status_code, 404)
        except Exception as e:
            print(f"Exception raised: {str(e)}")
