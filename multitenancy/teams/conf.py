import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1 :]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured(f"Error importing {module}: '{e}'")
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(f"Module '{module}' does not define a '{attr}'")
    return attr


class TeamAppConf(AppConf):

    PROFILE_MODEL = ""
    HOOKSET = "multitenancy.teams.hooks.TeamDefaultHookset"
    NAME_BLACKLIST = []

    def configure_profile_model(self, value):
        if value:
            return load_path_attr(value)

    def configure_hookset(self, value):
        return load_path_attr(value)()

    class Meta:
        prefix = "multitenancy_teams"
