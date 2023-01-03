from django.db import models
from multitenancy.users.models import Customer
from django_tenants.utils import get_tenant_type_choices


def get_plans():
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


class Subscription(models.Model):
    status = models.IntegerField()
    duration = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    reference = models.TextField(max_length=100, help_text="Free text field for user references")
    last_updated = models.DateTimeField(
        auto_now=True, help_text="Keeps track of when a record was last updated"
    )
    reason = models.TextField(help_text="Reason for state change, if applicable.")


class UserSubcriptions(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(Subscription)
