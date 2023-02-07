import django_filters
from multitenancy.apps.models import Tenant


class TenantFilter(django_filters.FilterSet):
    class Meta:
        model = Tenant
        fields = ['id']
