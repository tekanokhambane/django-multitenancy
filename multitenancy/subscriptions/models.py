import datetime
from django.db import models
from multitenancy.users.models import Customer
from django_tenants.utils import get_tenant_type_choices


def get_plans():
    #remove the plublic tenant type from list
    items = get_tenant_type_choices()
    items.pop(0) 
    return items

class Plan(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True, null=False, choices=get_plans())
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(default=75,  # type: ignore
                                max_digits=12, verbose_name="Price", decimal_places=2)

    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class ProductTypeManager(models.Manager):
    pass

class ProductType(models.Model):
    class Types(models.TextChoices):
        TENANT_APP = "tenant", "Tenant App"
        DOMAIN = "domain"
        THIRD_PARTY_APP = "third_party", "3rd party App"
    name = models.CharField(max_length=115,choices=Types.choices, default=Types.TENANT_APP)
    features = models.ManyToManyField(ProductFeature)
    objects = ProductTypeManager()


class SubscriptionManager(models.Manager):
    pass

class Subscription(models.Model):
    class Cycles(models.TextChoices):
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        QUARTERLY = "quartely", "quarterly"
        ANNUALLY = "annually", "annually"
    status = models.IntegerField()
    cycle = models.CharField(max_length=50, choices=Cycles.choices, default=Cycles.MONTHLY)
    subscription_duration = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    renewal_date = models.DateField(null=True)
    reference = models.TextField(max_length=100, help_text="Free text field for user references")
    last_updated = models.DateTimeField(
        auto_now=True, help_text="Keeps track of when a record was last updated"
    )
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.CASCADE, related_name="subscriptions")
    reason = models.TextField(help_text="Reason for state change, if applicable.")
    renewal_status = models.CharField(max_length=10, choices=[('active', 'Active'), ('cancelled', 'Cancelled'), ('expired', 'Expired')], default="active")
    objects = SubscriptionManager()

    def get_cycle(self):
        # calculate the subscription_duration based on the subscription cycle
        cycle = self.cycle
        if cycle == 'weekly':
            self.subscription_duration = 7
            self.save()
            return self.subscription_duration
        elif  cycle == 'monthly':
            self.subscription_duration = 30
            self.save()
            return self.subscription_duration
        elif  cycle == 'quartely':
            self.subscription_duration = 90
            self.save()
            return self.subscription_duration
        else:
            self.subscription_duration = 365
            self.save()
            return self.subscription_duration

    def renew(self):
        
        if self.renewal_status == 'active':
            # Calculate and update the new end date for the subscription
            self.end_date = self.end_date + datetime.timedelta(days=self.subscription_duration)
            # Set the renewal date to today
            self.renewal_date = datetime.date.today()
            # Update the reason 
            self.reason = "Subscription renewal"
            self.save()
            # Charge the customer here
        elif self.renewal_status == 'expired':
            # Send a notification to the customer here
            pass
    
    def cancel_subscription(self):
        # set the status to cancelled
        self.renewal_status = 'cancelled'
        # Set the end date to today
        self.end_date = datetime.date.today()
        self.save()

    def activate_subscription(self):
        pass

    def update_duration(self):
        pass

    def is_active(self):
        pass

    def get_service(self):
        pass

    def get_product_type(self, type):
        self.product_type = type
        self.save()
