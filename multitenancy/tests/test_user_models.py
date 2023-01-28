from django.conf import settings
from django.urls import reverse_lazy
from django.test import TestCase
from multitenancy.users.models import Admin, Staff, TenantUser
from tenant_users.permissions.models import UserTenantPermissions


class StaffTestCase(TestCase):

    def setUp(self) -> None:
        staff_a = Staff(username='staff1', first_name='abc', last_name='kham', email='abc@email.com',)
        staff_a_pass = 'somepasswaord'
        staff_a.set_password(staff_a_pass)
        self.staff_a_pass = staff_a_pass
        staff_a.is_staff = True
        staff_a.save()
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

class AdminTestCase(TestCase):

    def setUp(self) -> None:
        admin_a = Admin(username='admin', first_name='abc123', last_name='khamban', email='abc123@email.com',)
        admin_a_pass = 'somepasswaord'
        self.admin_a_pass = admin_a_pass
        admin_a.set_password(admin_a_pass)
        admin_a.is_staff = True
        #admin_a.is_superuser = True
        admin_a.save()
        self.admin_a = admin_a
        add_user_perms = UserTenantPermissions.objects.create(profile_id=admin_a.id, is_staff=True, is_superuser=True)
        add_user_perms.save()

    def test_admin_exists(self):
        admin_count = TenantUser.objects.filter(username__iexact="admin").count()
        print(admin_count)
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
    
    # def test_admin_login_url(self):
    #     # login_url = 'admin/accounts/login/'
    #     login_url = settings.LOGIN_URL
    #     data = {"email":"abc123@email.com", "password":self.admin_a_pass}
    #     response = self.client.post(login_url, data, follow=True)
    #     # print(dir(response))
    #     status_code = response.status_code
    #     redirect_path = response.request.get('PATH_INFO')
    #     print(redirect_path)
    #     # self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
    #     # self.assertEqual(status_code, 200)
