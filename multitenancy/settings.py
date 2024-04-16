"""
Default settings for Multitenancy apps
"""

from django.conf import settings

#The default name for your tenants, eg if your saas app is a website you can name it website
#or CRM you can name it CRM etc.



TENANT_DISPLAY_NAME = getattr(settings, "TENANT_DISPLAY_NAME", "Service")
TENANT_DISPLAY_NAME_PLURAL =getattr(settings, "TENANT_DISPLAY_NAME_PLURAL", "Services")
TENANT_CREATION_TEMPLATE = getattr(settings, "TENANT_CREATION_TEMPLATE", "multitenancy/admin/publicUser/create_service.html")