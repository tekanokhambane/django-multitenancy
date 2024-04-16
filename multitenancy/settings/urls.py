from django.urls import path
from . import views

urlpatterns = [
    path("settings/", views.SettingsIndexView.as_view(), name="settings_index"),
    path("settings/general/", views.SettingsView.as_view(), name="generalsettings_index"),
    path("settings/general/logo/", views.UpdateLogoView.as_view(), name="update_logo"),
    path("settings/general/info/", views.GeneralInfoView.as_view(), name="update_info"),
    path("settings/general/address/", views.AddressView.as_view(), name="update_address"),
    path("settings/general/adminsettings/", views.AdminSettingsView.as_view(), name="update_adminsettings"),
]