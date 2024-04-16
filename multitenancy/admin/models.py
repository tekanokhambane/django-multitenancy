class SettingsConfig:
    def __init__(self, model_class, position, label, icon):
        self.model_class = model_class
        self.position = position
        self.label = label
        self.icon = icon

class Settings:
    app_configs = []

    @classmethod
    def register_settings(cls, model_class, position=0, label=None, icon=None):
        if not label:
            label = model_class._meta.verbose_name
        cls.app_configs.append(SettingsConfig(model_class, position, label, icon))
        return model_class

def add_to_settings(position=0, label=None, icon=None):
    def decorator(cls):
        Settings.register_settings(cls, position, label, icon)
        return cls
    return decorator


class ModelAdminGroup:
    menu_icon = ''
    menu_label = ''
    menu_order = 0
    items = []

    def __init__(self, menu_icon, menu_label, menu_order):
        self.menu_icon = menu_icon
        self.menu_label = menu_label
        self.menu_order = menu_order

    def register(self, model_admin):
        self.items.append(model_admin)



class AppConfig:
    def __init__(self, model_class, menu_label, menu_order, menu_icon, list_display):
        self.model_class = model_class
        self.menu_label = menu_label
        self.menu_order = menu_order
        self.menu_icon = menu_icon
        self.list_display = list_display


class Admin:
    app_configs = []

    def __init__(self, model, menu_label, menu_order, menu_icon, list_display, group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.menu_label = menu_label
        self.menu_order = menu_order
        self.menu_icon = menu_icon
        self.list_display = list_display
        group.register(self)
        self.app_configs.append(AppConfig(model, menu_label, menu_order, menu_icon, list_display))


def register_admin(admin_class):
    admin_class.app_configs.append(AppConfig(admin_class.model, admin_class.menu_label, admin_class.menu_order, admin_class.menu_icon, admin_class.list_display))
    return admin_class



