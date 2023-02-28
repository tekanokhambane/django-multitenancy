import unittest
from multitenancy.users.models import Admin, Customer, Staff, TenantUser
from tenant_users.permissions.models import UserTenantPermissions


class StaffTestCase(unittest.TestCase):

        

    def test_staff_exists(self):
        staff_a = Staff.objects.create(
            username='staff1', first_name='abc', last_name='kham', email='abcstaff@email.com',
        )
        
        staff_a_pass = 'somepasswaord'
        staff_a.set_password(staff_a_pass)
        self.staff_a_pass = staff_a_pass
        staff_a.save()
        staff_a.add_user_perms()
        self.staff_a = staff_a
        staff_count = Staff.objects.all().count()
        self.assertEqual(staff_count, 1)
        self.assertNotEqual(staff_count, 0)

    def test_staff_password(self):
        staff_a = Staff.objects.get(
            username='staff1', first_name='abc', last_name='kham', email='abcstaff@email.com',
        )
        
        staff_a_pass = 'somepasswaord'
        staff_a.set_password(staff_a_pass)
        self.staff_a_pass = staff_a_pass
        staff_a.save()
        
        self.staff_a = staff_a
        staff_qs = Staff.objects.filter(username__iexact="staff1")
        staff_exist = staff_qs.exists() and staff_qs.count() == 1
        self.assertTrue(staff_exist)
        self.assertTrue(self.staff_a.check_password(self.staff_a_pass))

class AdminTestCase(unittest.TestCase):
    

    def test_admin_exists(self):
        admin_a_pass = 'somepasswaord'
        admin_a = TenantUser.objects.create_superuser(
            username='admin', first_name='abc123', last_name='khamban', email='adminabc123@email.com',
            password=admin_a_pass
            )
        self.admin_a_pass = admin_a_pass
        admin_a.set_password(admin_a_pass)
        #admin_a.is_superuser = True
        admin_a.save()
        self.admin_a = admin_a
        admin_exits = TenantUser.objects.filter(email__iexact="adminabc123@email.com").exists()
        self.assertTrue(admin_exits)
        
    
    def test_superuser(self):

        superuser = UserTenantPermissions.objects.filter(is_superuser=True, profile_id=1)
        is_super = TenantUser.objects.filter(usertenantpermissions__is_superuser=True)
        super_exists = is_super.exists()
        #self.assertEqual(superuser, True)              
        self.assertTrue(super_exists, True)
        

    def test_admin_password(self):
        admin_a_pass = 'somepasswaord'
        admin_qs = TenantUser.objects.get( email='adminabc123@email.com')
        self.assertTrue(admin_qs.check_password(admin_a_pass))
    

class CustomerTestCase(unittest.TestCase):
    

    def test_customer_exists(self):
        customer_a = Customer.objects.create(username='customer1', first_name='abc', last_name='kham', email='abpdpdc@email.com',)
        customer_a_pass = 'somepasswaord'
        customer_a.set_password(customer_a_pass)
        self.customer_a_pass = customer_a_pass
        customer_a.save()
        customer_qs = Customer.objects.filter(email='abpdpdc@email.com',)
        customer_qs.exists()
        customer_count = Customer.objects.all().count()
        self.assertTrue(customer_qs)
        self.assertNotEqual(customer_count, 0)

    def test_customer_password(self):
        customer_a = Customer.objects.create(username='customer1', first_name='abc', last_name='kham', email='abffffc@email.com', password='somepasswaord')
        
        customer_qs = Customer.objects.filter(email='abffffc@email.com')
        customer_exist = customer_qs.exists() and customer_qs.count() == 1
        self.assertTrue(customer_exist)
        