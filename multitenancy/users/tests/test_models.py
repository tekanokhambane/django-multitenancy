import unittest
from multitenancy.users.models import Admin, Customer, Staff, TenantUser
from tenant_users.permissions.models import UserTenantPermissions


class StaffTestCase(unittest.TestCase):

    def setUp(self) -> None:
        staff_a = Staff(username='staff1', first_name='abc', last_name='kham', email='abc@email.com',)
        staff_a_pass = 'somepasswaord'
        staff_a.set_password(staff_a_pass)
        self.staff_a_pass = staff_a_pass
        staff_a.save()
        staff_a.add_user_perms()
        self.staff_a = staff_a

    def test_staff_exists(self):
        staff_count = Staff.objects.all().count()
        self.assertEqual(staff_count, 1)
        self.assertNotEqual(staff_count, 0)

    def test_staff_password(self):
        staff_qs = Staff.objects.filter(username__iexact="staff1")
        staff_exist = staff_qs.exists() and staff_qs.count() == 1
        self.assertTrue(staff_exist)
        self.assertTrue(self.staff_a.check_password(self.staff_a_pass))

class AdminTestCase(unittest.TestCase):

    def setUp(self) -> None:
        admin_a = Admin(username='admin', first_name='abc123', last_name='khamban', email='abc123@email.com',)
        admin_a_pass = 'somepasswaord'
        self.admin_a_pass = admin_a_pass
        admin_a.set_password(admin_a_pass)
        #admin_a.is_superuser = True
        admin_a.save()
        self.admin_a = admin_a
        admin_a.create_public_superuser()
        

    def test_admin_exists(self):
        admin_count = TenantUser.objects.filter(username__iexact="admin").count()
        self.assertEqual(admin_count, 1)
        self.assertNotEqual(admin_count, 0)
    
    def test_superuser(self):
        superuser = UserTenantPermissions.objects.filter(is_superuser=True, profile_id=1)
        is_super = TenantUser.objects.filter(usertenantpermissions__is_superuser=True)
        super_exists = is_super.exists()
        #self.assertEqual(superuser, True)              
        self.assertTrue(super_exists, True)
        

    def test_admin_password(self):
        admin_qs = Admin.objects.filter(username__iexact="admin")
        admin_exist = admin_qs.exists() and admin_qs.count() == 1
        self.assertTrue(admin_exist)
        self.assertTrue(self.admin_a.check_password(self.admin_a_pass))
    

class CustomerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        customer_a = Customer(username='customer1', first_name='abc', last_name='kham', email='abc@email.com',)
        customer_a_pass = 'somepasswaord'
        customer_a.set_password(customer_a_pass)
        self.customer_a_pass = customer_a_pass
        customer_a.save()
        self.customer_a = customer_a

    def test_customer_exists(self):
        customer_count = Customer.objects.all().count()
        self.assertEqual(customer_count, 1)
        self.assertNotEqual(customer_count, 0)

    def test_customer_password(self):
        customer_qs = Customer.objects.filter(username__iexact="customer1")
        customer_exist = customer_qs.exists() and customer_qs.count() == 1
        self.assertTrue(customer_exist)
        self.assertTrue(self.customer_a.check_password(self.customer_a_pass))