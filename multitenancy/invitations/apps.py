import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "multitenancy.invitations"
    label = "multitenancy_invitations"
    verbose_name = _("Multitenancy Invitations")

    def ready(self):
        importlib.import_module("multitenancy.invitations.receivers")
