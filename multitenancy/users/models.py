from django.db import models
from tenant_users.tenants.models import UserProfile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from tenant_users.permissions.models import UserTenantPermissions
from multitenancy.profiles.models import Profile


# Create your models here.
class TenantUser(UserProfile):
    class Types(models.TextChoices):
        ADMIN = "Admin", "Admin"
        STAFF = "Staff", "Staff"
        CUSTOMER = "Customer", "Customer"
    type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=Types.ADMIN)
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True)
    # note = models.CharField(max_length=300, blank=True, null=True)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        elif self.username:
            return self.username
        else:
            return self.email


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=TenantUser.Types.ADMIN)


class StaffManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=TenantUser.Types.STAFF)


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=TenantUser.Types.CUSTOMER)


class Admin(TenantUser):
    objects = AdminManager()

    @property
    def get_profile(self):
        profile = Profile.objects.get_or_create(user_id=self.id, name=self.username)  # type: ignore
        return profile

    @property
    def create_public_superuser(self, *args, **kwargs):
        UserTenantPermissions.objects.create(profile_id=self.id, is_staff=True, is_superuser=True)  # type: ignore

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = TenantUser.Types.ADMIN

        return super().save(*args, **kwargs)


class Staff(TenantUser):
    objects = StaffManager()

    @property
    def profiles(self):
        return self.profiles

    @property
    def account(self):
        return self.account

    @property
    def get_profile(self):
        profile = Profile.objects.get_or_create(user_id=self.id, name=self.username)  # type: ignore
        return profile

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = TenantUser.Types.STAFF
        return super().save(*args, **kwargs)


class Customer(TenantUser):
    objects = CustomerManager()

    @property
    def account(self):
        return self.account

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = TenantUser.Types.CUSTOMER
        return super().save(*args, **kwargs)
