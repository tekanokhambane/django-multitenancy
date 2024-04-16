from django import template
from multitenancy.utils import get_gravatar_url
from multitenancy.settings.models import Logo, GeneralInfo, Address

register = template.Library()


@register.simple_tag(takes_context=True)
def get_company_details(context):
    logo = Logo.load()
    info = GeneralInfo .load()
    address = Address.load()
    company_details = {"logo": logo, "info": info, "address": address}
    return company_details


@register.simple_tag
def avatar_url(user, size=50):
    """
    A template tag that receives a user and size and return
    the appropiate avatar url for that user.
    Example usage: {% avatar_url request.user 50 %}
    """

    if hasattr(user, 'profile') and user.avatar:
        return user.avatar.url

    if hasattr(user, 'email'):
        gravatar_url = get_gravatar_url(user.email, size=size)
        if gravatar_url is not None:
            return gravatar_url

    return 'multitenancy/static/admin/img/default-user-avatar.png'
