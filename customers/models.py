from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from tenant_users.tenants.models import TenantBase
from django.utils.text import slugify 


class Client(TenantBase):
    id = models.AutoField(primary_key=True, auto_created=True)
    description = models.TextField(max_length=200)

   # objects = models.Manager()


class Domain(DomainMixin):
    pass
