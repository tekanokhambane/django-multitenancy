from django.db import models

#from tenant_users.tenants.models import TenantUserProfile
from tenant_users.tenants.models import UserProfile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    Permission, Group


class TenantUser(UserProfile):
    user_type_data = (('1', 'HOD'), ('2', 'Staff'), ('3', 'Customer'), ('4', 'AppUser'))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True)
    #note = models.CharField(max_length=300, blank=True, null=True)
    
    