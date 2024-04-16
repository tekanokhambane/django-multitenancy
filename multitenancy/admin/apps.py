from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MultiTenancyAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'multitenancy'
    verbose_name = _("Multitenancy admin")
    app_label = 'multitenancyadmin'
