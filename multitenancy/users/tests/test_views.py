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


class CustomerViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.customer_data = {
            "first_name": "customer",
            "last_name": "test",
            "username": "tcustomer",
            "password": "password1234",
            "email": "customer2@example.com",
        }
        self.new_customer_data = {
            "first_name": "customernew",
            "username": "testcustomer",
        }
        self.customer_obj = Customer.objects.first()

        self.staff_data = {
            "first_name": "staff",
            "last_name": "test",
            "username": "tstaff",
            "password": "password1234",
            "email": "staff2@example.com",
        }
        self.staff_obj = Staff.objects.first()

    def test_create_customer_view(self):
        # create a new admin
        admin = Admin.objects.create(
            first_name="admin",
            last_name="test",
            username="tadmin",
            password="password1234",
            email="admin2@example.com",
        )
        self.client.force_login(admin)
        response = self.client.post(
            "/admin/customers/create/", self.customer_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "multitenancy/users/created_customer.html")
