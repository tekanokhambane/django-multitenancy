from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django_tenants.models import DomainMixin
from datetime import datetime, timedelta
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
    
    def filter_by_plan(self, plan):
        filter = Tenant.objects.filter(type=plan)
        return filter

    def active(self):
        return Tenant.objects.filter(subscription__is_active=True)

    

class Tenant(TenantBase):
    id = models.AutoField(primary_key=True, auto_created=True)
    type = models.CharField(max_length=200, default=DEFAULT_TYPE, choices=get_types())
    name = models.CharField(max_length=100)
    is_template = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.PROTECT, related_name="tenants")
    description = models.TextField(max_length=200)
    subscription = models.OneToOneField(Subscription,  blank=True,on_delete=models.CASCADE, related_name="tenants")
    # paid_until = models.DateField()
    trail_duration = models.IntegerField(default=0)
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
    

    @classmethod
    def create_tenant(cls, name, type, is_template, description, trail_duration, owner, subscription_plan):
        subscription = Subscription.objects.create(plan=subscription_plan, owner=owner)
        tenant = cls.objects.create(name=name, type=type, is_template=is_template, description=description, trail_duration=trail_duration, subscription=subscription, owner=owner)
        return tenant
    
    @transaction.atomic
    def create_tenant_with_subscription(self, plan, **kwargs):
        subscription = Subscription.objects.create(plan=plan)
        kwargs['subscription'] = subscription
        tenant = Tenant.objects.create(**kwargs)
        return tenant

    def start_trail(self):
        """
        if the user has no active or inactive tenants than start trail
        """
        
        if self.owner.tenants.count() > 1:
            raise ValueError("User has no trails available")
        else:
            self.on_trial = True
            self.trail_duration = 30
            self.subscription.start_subscription("monthly")
            self.save()

    def end_trail(self):
        """
        End trail when the trail duration is reached
        """
        if self.on_trial == True:
            self.on_trial = False
            self.trail_duration = None
            self.deactivate()
            self.save()            
    

    
    def trail_days_left(self):
        """
        Calculate the number of days left for the trail to end
        """
        if self.on_trial:
            trail_end_date = self.created + timedelta(days=self.trail_duration)
            days_left = (trail_end_date - datetime.now().date()).days
            # update the duration
            self.trail_duration = days_left
            self.save()
            # update duration and end trail then deactivate service
            if self.trail_duration == 0:
                self.on_trial = False
                self.deactivate()
                self.save()
            return days_left
        else:
            return None

    def upgrade(self, plan):
        """
        Iterate over the plans and then select a plan to upgrade and update the subscription
        """
        self.type = plan
        self.save()

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