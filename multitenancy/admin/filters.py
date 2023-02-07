import django_filters
from multitenancy.apps.models import Tenant

from multitenancy.users.models import Customer



class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['id']
