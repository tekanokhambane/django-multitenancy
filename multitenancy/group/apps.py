from django.apps import AppConfig


class GroupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'multitenancy.group'
    app_label = 'multitenancy_auth'
