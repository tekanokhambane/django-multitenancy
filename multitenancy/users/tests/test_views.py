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


# class CustomerViewsTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()
#         self.customer_data = {
#             "first_name": "customer",
#             "last_name": "test",
#             "username": "tcustomer",
#             "password": "password1234",
#             "email": "customer@example.com",
#         }
#         self.new_customer_data = {
#             "first_name": "customer1",
#             "username": "testcustomer",
#         }
#         self.customer_obj = Customer.objects.first()

#     def test_get_create_customer_view(self):
#         self.user = TenantUser.objects.create(
#             username="admin",
#             password="password",
#             first_name="abc123",
#             last_name="khamban",
#             email="abc123@email.com",
#             type="Admin",
#             is_active=True,
#         )

#         self.client.force_login(user=self.user)
#         request = self.factory.get("/admin/customers/create/")
#         request.user = self.user
#         response = CreateCustomerView.as_view()(request)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(self.client.session.get("_auth_user_id"))
#         self.assertIn("_auth_user_id", self.client.session)
#         self.assertTemplateUsed(response, "admin/customers/create.html")

#     def test_post_create_customer_view(self):
#         self.user = TenantUser.objects.get(
#             username="admin",
#             password="password",
#             first_name="abc123",
#             last_name="khamban",
#             email="abc123@email.com",
#             type="Admin",
#             is_active=True,
#         )
#         self.client.force_login(user=self.user)
#         request = self.factory.post("/admin/customers/create/", data=self.customer_data)
#         request.user = self.user
#         response = CreateCustomerView.as_view()(request)
#         self.assertEqual(response.status_code, 200)
