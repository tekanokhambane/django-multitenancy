from multitenancy.settings.models  import Logo, GeneralInfo, Address, AdminSettings
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_company_details(context):
    logo = Logo.load()
    info = GeneralInfo .load()
    company_details = {"logo":logo, "info":info}
    print(company_details)
    return  company_details
    