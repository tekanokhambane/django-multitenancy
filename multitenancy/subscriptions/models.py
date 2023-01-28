import datetime
from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from multitenancy.users.models import Customer
from django_tenants.utils import get_tenant_type_choices


def get_plans():
    #remove the plublic tenant type from list
    items = get_tenant_type_choices()
    items.pop(0) 
    return items

class ProductFeature(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True, null=False, choices=get_plans())
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    features = models.ManyToManyField(ProductFeature)
    price = models.DecimalField(default=75,  # type: ignore
                                max_digits=12, verbose_name="Price", decimal_places=2)

    def __str__(self):
        return self.name
    
    def add_feature(self, feature):
        new_feature = ProductFeature.objects.create(name=feature)
        self.features.add(new_feature)
        self.save()

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    @property
    def price_weekly(self):
        price = self.price / 4
        return price
    
    @property
    def price_quartely(self):
        price = self.price * 3
        return price

    @property
    def price_annually(self):
        price = self.price * 12
        return price


class ProductTypeManager(models.Manager):
    def create_defaults(self):
        self.get_or_create(name=ProductType.Types.TENANT_APP)
        self.get_or_create(name=ProductType.Types.DOMAIN)
        self.get_or_create(name=ProductType.Types.THIRD_PARTY_APP)

class ProductType(models.Model):
    class Types(models.TextChoices):
        TENANT_APP = "tenant", "Tenant App"
        DOMAIN = "domain", "Custom Domain"
        THIRD_PARTY_APP = "third_party", "3rd party App"
    name = models.CharField(max_length=115,choices=Types.choices, default=Types.TENANT_APP)
    objects = ProductTypeManager()


class SubscriptionManager(models.Manager):
    pass

class Subscription(models.Model):
    class Cycles(models.TextChoices):
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        QUARTERLY = "quartely", "quarterly"
        ANNUALLY = "annually", "annually"
    
    cycle = models.CharField(max_length=50, choices=Cycles.choices, default=Cycles.MONTHLY)
    subscription_duration = models.IntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    renewal_date = models.DateField(null=True)
    reference = models.TextField(max_length=100, help_text="Free text field for user references")
    last_updated = models.DateTimeField(
        auto_now=True, help_text="Keeps track of when a record was last updated"
    )
    product_type = models.ForeignKey(ProductType,null=True, on_delete=models.CASCADE, related_name="subscriptions")
    reason = models.TextField(help_text="Reason for state change, if applicable.")
    status = models.CharField(max_length=10, choices=[('active', 'Active'),('inactive', 'Inactive') ,('cancelled', 'Cancelled'), ('expired', 'Expired')], default="inactive")
    objects = SubscriptionManager()
    

    def start_subscription(self, cycle):
        
        # calculate the subscription_duration based on the subscription cycle
        self.status = "active"
        self.cycle = cycle
        self.reason =  "Start Subscription"
        self.renewal_date = datetime.date.today()
        self.save()
        if cycle == 'weekly':
            self.subscription_duration =  7
            self.end_date =  self.renewal_date + datetime.timedelta(days=self.subscription_duration)
            self.save()
            return self.subscription_duration
        elif  cycle == 'monthly':
            self.subscription_duration = 30
            self.end_date = self.renewal_date + datetime.timedelta(days=self.subscription_duration)
            self.save()
            return self.subscription_duration
        elif  cycle == 'quartely':
            self.subscription_duration = 90
            self.end_date = self.renewal_date + datetime.timedelta(days=self.subscription_duration)
            self.save()
            return self.subscription_duration
        else:
            self.subscription_duration = 365
            self.end_date = self.renewal_date + datetime.timedelta(days=self.subscription_duration)
            self.save()
            return self.subscription_duration

    def renew(self):
        
        if self.status == 'active':
            # Calculate and update the new end date for the subscription
            self.end_date = self.end_date + datetime.timedelta(days=self.subscription_duration)
            # Set the renewal date to today
            self.renewal_date = datetime.date.today()
            # Update the reason 
            self.reason = "Subscription renewed"
            self.save()
            # Charge the customer here and create invoice
        elif self.status == 'expired':
            # Send a notification to the customer here
            pass
    
    def cancel_subscription(self):
        # set the status to cancelled
        if self.status == 'active':
            self.status = 'cancelled'
            # Set the end date to today
            self.end_date = datetime.date.today()
            # Update the reason 
            self.reason = "Subscription cancelled"
            self.save()

    def activate_subscription(self, duration):
        # In future checks will be done to ensure there are no outstanding invoices
        # update the renewal status
        self.status = 'active'
        # Set the renewal date to today
        self.renewal_date = datetime.date.today()
        # Calculate and update the new end date for the subscription
        self.end_date = self.renewal_date + datetime.timedelta(days=duration)
        # Update the reason 
        self.reason = "Subscription activated"
        self.save()

    def update_duration(self, duration):
        self.subscription_duration = duration
        self.save()

    @property
    def is_active(self):
        # a check to see if the active
        if self.status == "active":
            return True
        else:
            return False

    def get_service(self):
        pass

    def get_product_type(self, type:str):
        # On service creation each subscription must be assigned to a product type
        self.product_type = type
        self.save()
