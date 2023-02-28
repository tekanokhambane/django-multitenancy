import datetime
from django.db import models
from django.db.models import Q
from calendar import monthrange
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
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
    
    class Meta:
        ordering= ('-pk',)


class PlanQueryset(models.QuerySet):

    def search(self, query):
        return self.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    def active_plans(self):
        return self.filter(is_active=True)

    def by_price(self, price):
        return self.filter(price=price)

    def by_features(self, feature):
        return self.filter(features=feature)

class PlanManager(models.Manager):
    def get_queryset(self):
        return PlanQueryset(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

    def active_plans(self):
        return self.get_queryset().active_plans()

    def by_price(self, price):
        return self.get_queryset().by_price(price)

    def by_features(self, feature):
        return self.get_queryset().by_features(feature)

class Plan(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True, null=False, choices=get_plans())
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    features = models.ManyToManyField(ProductFeature)
    price = models.DecimalField(default=75,  # type: ignore
                                max_digits=12, verbose_name="Price", decimal_places=2)
    objects = PlanManager()
    
    class Meta:
        ordering = ('-price',)

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


class SubscriptionQueryset(models.QuerySet):
    def active(self):
        return self.filter(status="active")

    def inactive(self):
        return self.filter(status="inactive")

    def cancelled(self):
        return self.filter(status="cancelled")

    def expired(self):
        return self.filter(status="expired")

    def weekly(self):
        return self.filter(cycle=Subscription.Cycles.WEEKLY)

    def monthly(self):
        return self.filter(cycle=Subscription.Cycles.MONTHLY)

    def quarterly(self):
        return self.filter(cycle=Subscription.Cycles.QUARTERLY)

    def annually(self):
        return self.filter(cycle=Subscription.Cycles.ANNUALLY)

    def started_within_week(self):
        return self.filter(start_date__gte=timezone.now() - timezone.timedelta(days=7))

    def ended_within_week(self):
        return self.filter(end_date__lte=timezone.now() - timezone.timedelta(days=7))

    def renew_within_week(self):
        return self.filter(renewal_date__lte=timezone.now() - timezone.timedelta(days=7))
    def get_product_type(self, name):
        return self.filter(product_type__name__exact=name)

    def get_status(self, query):
        return self.filter(status__exact=query)

    def get_active(self):
        return self.filter(status__contains="active")
    
    def search(self, query=None):
        if query is None or query == "":
            return self.all()
        return self.filter(
            Q(reference__icontains=query) |
            Q(reason__icontains=query) |
            Q(product_type__name__icontains=query)
        )

    


class Subscription(models.Model):
    class Cycles(models.TextChoices):
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        QUARTERLY = "quartely", "quarterly"
        ANNUALLY = "annually", "annually"
    
    cycle = models.CharField(max_length=50, choices=Cycles.choices, default=Cycles.MONTHLY)
    subscription_duration = models.IntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True,null=True)
    end_date = models.DateField(auto_now_add=True)
    renewal_date = models.DateField(null=True)
    reference = models.TextField(max_length=100, help_text="Free text field for user references")
    last_updated = models.DateTimeField(
        auto_now=True, help_text="Keeps track of when a record was last updated"
    )
    product_type = models.ForeignKey(ProductType,null=True, on_delete=models.CASCADE, related_name="subscriptions")
    reason = models.TextField(help_text="Reason for state change, if applicable.")
    status = models.CharField(max_length=10, choices=[('active', 'Active'),('inactive', 'Inactive') ,('cancelled', 'Cancelled'), ('expired', 'Expired')], default="inactive")
    objects = SubscriptionQueryset().as_manager()


    def __str__(self) -> str:
        return f"{self.pk}"

    
    class Meta:
        verbose_name = _("Subscription")
        ordering = ("-last_updated",)

    
    @classmethod
    def get_active_inactive_subscriptions_data(cls):
        """
        Create a dataset for total active and inactive subscriptions, the data is updated daily and the data can be displayed on a dashboard graph
        """
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=monthrange(today.year, today.month)[1])
        data = []
        for i in range((last_day_of_month - first_day_of_month).days + 1):
            date = first_day_of_month + datetime.timedelta(days=i)
            if date <= today:
                active_count = cls.objects.filter(status="active", created_date__lte=date).count()
                inactive_count = cls.objects.filter(status="inactive", created_date__lte=date).count()
                
            else:
                active_count = 0
                inactive_count = 0
            data.append((date.strftime("%Y-%m-%d"), active_count, inactive_count))
            # active_data[date.strftime("%Y-%m-%d")] = active_count
            # inactive_data[date.strftime("%Y-%m-%d")] = inactive_count
        return data

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
