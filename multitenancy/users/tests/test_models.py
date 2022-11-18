from django.test import TestCase
from ..models import Admin, Staff


class StaffTestCase(TestCase):

    def setUp(self) -> None:
        staff_a = Staff(username='staff1', first_name='abc', last_name='kham', email='abc@email.com',)
        staff_a.set_password('somepasswaord')
        staff_a.is_staff = True
        staff_a.save()
        print(staff_a.is_staff)
        print(staff_a.type, staff_a.is_superuser)

    def test_staff_exists(self):
        staff_count = Staff.objects.all().count()
        self.assertEqual(staff_count, 1)
        self.assertNotEqual(staff_count, 0)


class AdminTestCase(TestCase):

    def setUp(self) -> None:
        admin_a = Admin(username='admin', first_name='abc123', last_name='khamban', email='abc123@email.com',)
        admin_a_pass = 'somepasswaord'
        self.admin_a_pass = admin_a_pass
        admin_a.set_password(admin_a_pass)
        admin_a.is_staff = True
        admin_a.is_superuser = True
        admin_a.save()
        self.admin_a = admin_a

    def test_admin_exists(self):
        admin_count = Admin.objects.all().count()
        self.assertEqual(admin_count, 1)
        self.assertNotEqual(admin_count, 0)

    def test_admin_password(self):
        admin_qs = Admin.objects.filter(username__iexact="admin")
        admin_exist = admin_qs.exists() and admin_qs.count() == 1
        self.assertTrue(admin_exist)
        self.assertTrue(self.admin_a.check_password(self.admin_a_pass))
