import os
import re
import uuid
from django.db import models
from django.db.models import Q
from tenant_users.tenants.models import UserProfile, UserProfileManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import Group
from tenant_users.permissions.models import UserTenantPermissions
from multitenancy.profiles.models import Profile


def upload_avatar_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return os.path.join(
        "avatar_images",
        "avatar_{uuid}_{filename}{ext}".format(
            uuid=uuid.uuid4(), filename=filename, ext=ext
        ),
    )


class TenantUserQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.all()
        lookups = (
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(username__icontains=query)
        )
        return self.filter(lookups)

    def filter_by_id(self, query=None):
        if query is None or query == "":
            return self.all()
        return self.filter(id__exact=query)


class TenantUserManager(UserProfileManager):

    def create_user(self, email=None, password=None, is_staff=False, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        if email:
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                raise ValueError("Invalid email address")

        if not password:
            user.set_unusable_password()
        user = self.model(
            email=self.normalize_email(email),
        )
        return super().create_user(email, password, is_staff, **extra_fields)

    def get_queryset(self):
        return TenantUserQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

    def filter_by_id(self, query=None):
        return self.get_queryset().filter_by_id(query=query)


class TenantUser(UserProfile):
    class Types(models.TextChoices):
        ADMIN = "Admin", "Admin"
        STAFF = "Staff", "Staff"
        CUSTOMER = "Customer", "Customer"

    avatar = models.ImageField(
        verbose_name=_("profile picture"),
        upload_to=upload_avatar_to,
        blank=True,
    )

    type = models.CharField(
        _("Type"), max_length=255, choices=Types.choices, default=Types.CUSTOMER
    )
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True)
    # note = models.CharField(max_length=300, blank=True, null=True)
    signup_confirmation = models.BooleanField(default=False)

    objects = TenantUserManager()

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

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    @property
    def is_superuser(self):
        if self.usertenantpermissions.is_superuser:
            return True
        else:
            return False


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=TenantUser.Types.ADMIN)


class StaffManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=TenantUser.Types.STAFF)


class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(type=TenantUser.Types.CUSTOMER)
        )


class Admin(TenantUser):
    objects = AdminManager()

    def create_public_superuser(self, *args, **kwargs):
        UserTenantPermissions.objects.create(
            profile_id=self.pk, is_staff=True, is_superuser=True
        )

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = TenantUser.Types.ADMIN
            self.create_public_superuser()
        if not self.username:
            self.username = self.email

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
        if not self.username:
            self.username = self.email
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


@receiver(post_save, sender=TenantUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == TenantUser.Types.ADMIN:
            Profile.objects.create(user=instance)
        elif instance.type == TenantUser.Types.STAFF:
            Profile.objects.create(user=instance)
            # UserTenantPermissions.objects.create(
            #     profile_id=instance.pk, is_staff=True, is_superuser=False
            # )


post_save.connect(create_user_profile, sender=TenantUser)
