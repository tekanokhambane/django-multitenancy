from account.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy
from multitenancy.settings.forms import AddressForm, AdminSettingsForm, GeneralInfoForm, LogoForm
from multitenancy.settings.models import Address, AdminSettings, GeneralInfo, Logo
from multitenancy.admin.views.baseViews import(
    AdminListView,
    AdminDeleteView,
    AdminCreateView,
    AdminUpdateView,
    AdminTemplateView,
    AdminView,
    AdminDetailView
    )

class SettingsIndexView(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/settings_list.html"





class SettingsView(LoginRequiredMixin, AdminTemplateView):
    template_name = 'multitenancy/settings/generalsettings_index.html'
    settings_list = []

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['logo'] = Logo.load()
        context['address'] = Address.load()
        context['admin_settings'] = AdminSettings.load()
        context['info'] = GeneralInfo.load()
        return context


class UpdateLogoView(LoginRequiredMixin, AdminUpdateView):

    model = Logo
    form_class = LogoForm
    success_url = reverse_lazy('generalsettings_index', urlconf="multitenancy.urls")
    template_name = 'multitenancy/settings/update_logo.html'

    def get_object(self):
        return self.model.objects.first()


class GeneralInfoView(LoginRequiredMixin, AdminUpdateView):

    model = GeneralInfo
    form_class = GeneralInfoForm
    success_url = reverse_lazy('generalsettings_index', urlconf="multitenancy.urls")
    template_name = 'multitenancy/settings/update_info.html'

    def get_object(self):
        return self.model.objects.first()


class AddressView(LoginRequiredMixin, AdminUpdateView):

    model = Address
    form_class = AddressForm
    success_url = reverse_lazy('generalsettings_index', urlconf="multitenancy.urls")
    template_name = 'multitenancy/settings/update_address.html'

    def get_object(self):
        return self.model.objects.first()

class AdminSettingsView(LoginRequiredMixin, AdminUpdateView):

    model = AdminSettings
    form_class = AdminSettingsForm
    success_url = reverse_lazy('generalsettings_index', urlconf="multitenancy.urls")
    template_name = 'multitenancy/settings/update_adminsettings.html'

    def get_object(self):
        return self.model.objects.first()