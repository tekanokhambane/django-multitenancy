from django.db import models

#from tenant_users.tenants.models import TenantUserProfile
from tenant_users.tenants.models import UserProfile
from django.utils.translation import ugettext_lazy as _


class TenantUser(UserProfile):
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
