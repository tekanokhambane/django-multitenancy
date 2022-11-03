from django.apps import AppConfig


class MultiTenancyAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'multitenancy.admin'
    verbose_name = 'multitenancy_admin'
    default = True
    app_label = 'multitenancy_admin'
    
