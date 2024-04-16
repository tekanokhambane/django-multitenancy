import django_filters
from multitenancy.subscriptions.models import Plan

class PlanFilter(django_filters.FilterSet):
    class Meta:
        model = Plan
        fields = ['id']
