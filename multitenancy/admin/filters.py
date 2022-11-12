import  django_filters 
from multitenancy.apps.models import Tenant, Package
from multitenancy.users.models import Customer

class TenantFilter(django_filters.FilterSet):
    class Meta:
        model = Tenant
        fields = ['id']

class PackageFilter(django_filters.FilterSet):
    class Meta:
        model = Package
        fields = ['id']


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['id']