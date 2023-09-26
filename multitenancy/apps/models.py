from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.db import models, transaction

from django.db.models import Q, Sum
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

class TenantQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query =="":
            return self.all()
        lookups = Q(name__icontains=query ) | Q(id__contains=query) | Q(type__iexact=query)| Q(owner__id__icontains=query)| Q(owner__email__icontains=query)| Q(owner__username__icontains=query)
        return self.filter(lookups)
    
    def filter_by_plan(self, plan):
        filter = self.filter(type=plan)
        return filter

    def active(self):
        return self.filter(subscription__is_active=True)
    
    

class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)
    
    def search(self, query=None):
        return self.get_queryset().search(query=query)
    
    def filter_by_plan(self, plan):
        return self.get_queryset().filter_by_plan(plan=plan)
    
    def active(self):
        return self.get_queryset().active()

DEFAULT_TYPE = 'default'





class Tenant(TenantBase):
    id = models.AutoField(primary_key=True, auto_created=True)
    type = models.CharField(max_length=200, default=DEFAULT_TYPE, choices=get_types())
    name = models.CharField(max_length=100)
    is_template = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.PROTECT, related_name="tenants")
    description = models.TextField(max_length=200)
    subscription = models.OneToOneField(Subscription, blank=True, null=True, on_delete=models.CASCADE, related_name="tenants")
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
        tenant = cls.objects.create(name=name, type=type, is_template=is_template, description=description,
                                    trail_duration=trail_duration, subscription=subscription, owner=owner)
        return tenant

    @transaction.atomic
    def create_tenant_with_subscription(self, plan, **kwargs):
        subscription = Subscription.objects.create(plan=plan)
        kwargs['subscription'] = subscription
        tenant = Tenant.objects.create(**kwargs)
        return tenant


    @classmethod
    def total_revenue(cls):
        revenue = cls.objects.aggregate(total_revenue=Sum('plan__price'))['total_revenue']
        return revenue or 0

    def end_trail(self):
        """
        End trail when the trail duration is reached
        """
        if self.on_trial:
            self.subscription.update(trail_duration=None)
            self.on_trial = False
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
            self.update(trail_duration=days_left)
            # update duration and end trail then deactivate service
            if days_left == 0:
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


@receiver(post_save, sender=Tenant)
def start_trial(sender, instance, created, **kwargs):
    """
    Automatically start a trial when a tenant is created
    """
    if created:
        if instance.owner.tenants.count() > 1:
            instance.on_trial = False
            instance.trail_duration = 0
        else:
            instance.on_trial = True
            instance.trail_duration = 30
        instance.subscription.update(status="active", cycle="monthly", subscription_duration=instance.trail_duration)
        instance.save()
        
    



class DomainManager(models.Manager):
    pass

class Domain(DomainMixin):
    is_custom = models.BooleanField(default=False)
    objects = DomainManager()

    def __str__(self):
        return self.domain