from django.conf import settings
from django.db import models
from django.db.models import Q
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase
from django_tenants.utils import get_tenant_type_choices

from multitenancy.subscriptions.models import Plan


DEFAULT_TYPE = "personal"

def get_types():
    items = get_tenant_type_choices()
    items.pop(0) 
    return items

class TenantManager(models.Manager):
    def search(self, query):
        lookups = Q(name__icontains=query ) | Q(id__exact=query) | Q(type__iexact=query)
        return Tenant.objects.filter(lookups)

    def upgrade(self):
        pass

    def downgrade(self):
        pass

class Tenant(TenantBase):
    id = models.AutoField(primary_key=True, auto_created=True)
    type = models.CharField(max_length=200, default=DEFAULT_TYPE, choices=get_types())
    name = models.CharField(max_length=100)
    is_template = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.PROTECT)
    description = models.TextField(max_length=200)
    # paid_until = models.DateField()
    on_trial = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    objects = TenantManager()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['id', 'name']
        verbose_name = settings.TENANT_DISPLAY_NAME
        verbose_name_plural = settings.TENANT_DISPLAY_NAME_PLURAL

    def start_trail(self):
        pass

    def end_trail(self):
        pass

class Domain(DomainMixin):
    has_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.domain
