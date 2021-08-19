from django_tenants_portal.core.models.admin_models import CompanyDetails
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_company_details(context):
    return  CompanyDetails.objects.get(id=1)
    