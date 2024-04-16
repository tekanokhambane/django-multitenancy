from django.test import TestCase
from multitenancy.users.models import Admin, Customer, Staff, TenantUser
from tenant_users.permissions.models import UserTenantPermissions


class StaffTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Staff.objects.all().delete()
        password = "password123"
        cls.staff = Staff.objects.create(
            username="teststaff",
            first_name="Test",
            last_name="Staff",
            email="test@example.com",
        )
        cls.staff.set_password(password)
        cls.staff.save()

    def test_staff_exists(self):
        staff = Staff.objects.get(username=self.staff.username)
        self.assertEqual(staff, self.staff)
        self.assertTrue(staff.pk)  # staff has a primary key set

    def test_staff_password(self):
        staff = Staff.objects.get(username=self.staff.username)
        staff.check_password("password123")
        self.assertTrue(staff.check_password("password123"))

    def test_role(self):
        self.assertEqual(self.staff.type, "Staff")


class AdminTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Admin.objects.all().delete()
        password = "password123"
        cls.admin = Admin.objects.create(
            username="testadmin",
            first_name="Test",
            last_name="Admin",
            email="admin1@example.com",
            password=password,
        )
        cls.admin.set_password(password)
        cls.admin.save()
        cls.admin.create_public_superuser()

    def test_admin_exists(self):
        admin = Admin.objects.get(username=self.admin.username)
        self.assertEqual(admin, self.admin)
        self.assertTrue(admin.pk)

    def test_superuser(self):
        self.assertTrue(self.admin.is_superuser)
        self.assertTrue(self.admin.is_staff)

    def test_admin_password(self):
        admin = Admin.objects.get(username=self.admin.username)
        admin.check_password("password123")
        self.assertTrue(admin.check_password("password123"))

    def test_role(self):
        self.assertEqual(self.admin.type, "Admin")


class CustomerTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Customer.objects.all().delete()
        password = "password123"
        cls.customer = Customer.objects.create(
            username="testcustomer",
            first_name="Test",
            last_name="Customer",
            email="customer1@example.com",
            password=password,
        )
        cls.customer.set_password(password)
        cls.customer.save()

    def test_customer_exists(self):
        customer = Customer.objects.get(username=self.customer.username)
        self.assertEqual(customer, self.customer)
        self.assertTrue(customer.pk)

    def test_customer_password(self):
        customer = Customer.objects.get(username=self.customer.username)
        customer.check_password("password123")
        self.assertTrue(customer.password, customer.check_password("password123"))

    def test_role(self):
        self.assertEqual(self.customer.type, "Customer")
