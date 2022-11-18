import django_filters
from multitenancy.apps.models import Tenant
from multitenancy.subscriptions.models import Plan
from multitenancy.users.models import Customer


class TenantFilter(django_filters.FilterSet):
    class Meta:
        model = Tenant
        fields = ['id']


class PlanFilter(django_filters.FilterSet):
    class Meta:
        model = Plan
        fields = ['id']


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['id']
