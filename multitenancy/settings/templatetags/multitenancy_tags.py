from multitenancy.settings.models import Logo, GeneralInfo, Address
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_company_details(context):
    logo = Logo.load()
    info = GeneralInfo .load()
    address = Address.load()
    company_details = {"logo": logo, "info": info, "address": address}
    return company_details
