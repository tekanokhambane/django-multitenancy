from django.conf import settings
from django.db import models
from django.db.models import Q
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase
from django_tenants.utils import get_tenant_type_choices

from multitenancy.subscriptions.models import Plan, Subscription


DEFAULT_TYPE = "personal"

def get_types():
    #remove the plublic tenant type from list
    items = get_tenant_type_choices()
    items.pop(0) 
    return items

class TenantManager(models.Manager):
    def search(self, query):
        lookups = Q(name__icontains=query ) | Q(id__exact=query) | Q(type__iexact=query)
        return Tenant.objects.filter(lookups)
    
    def filter_by_plan(self):
        pass

    

class Tenant(TenantBase):
    id = models.AutoField(primary_key=True, auto_created=True)
    type = models.CharField(max_length=200, default=DEFAULT_TYPE, choices=get_types())
    name = models.CharField(max_length=100)
    is_template = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.PROTECT, related_name="tenants")
    description = models.TextField(max_length=200)
    subscription = models.OneToOneField(Subscription, null=True, blank=True,on_delete=models.CASCADE, related_name="tenants")
    # paid_until = models.DateField()
    trail_duration = models.IntegerField(null=True, blank=True)
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
        """
        if the user has no active or inactive tenants than start trail
        """
        if self.owner.tenants == None:
            self.on_trial = True
            self.save()

    def end_trail(self):
        """
        End trail when the trail duration is reached
        """
        pass

    def upgrade(self):
        """
        Upgrade plan
        """
        pass

    def downgrade(self):
        """
        Downgrade plan
        """
        pass
    
    def add_subscription(self):
        """
        if user upgrades service from trail create a subscription
        """
        if self.on_trial == True:
            subscription = self.subscription.objects.create()
            self.subscription.get_product_type("tenant")
            self.save()
        

    def get_features(self):
        pass


class DomainManager(models.Manager):
    pass

class Domain(DomainMixin):
    is_custom = models.BooleanField(default=False)
    objects = DomainManager()

    def __str__(self):
        return self.domain