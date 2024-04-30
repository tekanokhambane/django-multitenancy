import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "multitenancy.teams"
    label = "multitenancy_teams"
    verbose_name = _("Multitenancy Teams")

    def ready(self):
        importlib.import_module("multitenancy.teams.receivers")
