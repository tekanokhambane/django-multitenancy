from django.urls.base import reverse, reverse_lazy
import sweetify
# import environ
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import gettext as _
# import time
from django.conf import settings
from tenant_users.tenants.utils import (get_tenant_model,
                                        get_tenant_domain_model)
from multitenancy.admin.decorators import allowed_users
from multitenancy.profiles.models import Profile
from tenant_users.tenants.models import InactiveError, ExistsError
from django.views.generic import TemplateView, ListView, DeleteView, View, CreateView, UpdateView
from account.mixins import LoginRequiredMixin
from multitenancy.admin.filters import CustomerFilter, PlanFilter, TenantFilter
from multitenancy.admin.forms import (
    AddressForm,
    AdminSettingsForm,
    CustomerForm,
    GeneralInfoForm,
    LogoForm,
    PlanForm,
    TenantForm)
from multitenancy.settings.models import Address, AdminSettings, GeneralInfo, Logo
from multitenancy.subscriptions.models import Plan, UserSubcriptions
from pinax.teams.models import SimpleTeam, Team
from multitenancy.users.models import Customer, TenantUser
from multitenancy.apps.models import Tenant, TenantType

# env = environ.Env()


class BaseCreateView(CreateView):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class BaseUpdateView(UpdateView):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class BaseDeleteView(DeleteView):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class BaseListView(ListView):
        def get(self, request, *args, **kwargs):
            self.object_list = self.get_queryset()
            allow_empty = self.get_allow_empty()

            if not allow_empty:
                # When pagination is enabled and object_list is a queryset,
                # it's better to do a cheap query than to load the unpaginated
                # queryset in memory.
                if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                        'class_name': self.__class__.__name__,
                    })
            context = self.get_context_data()
            return self.render_to_response(context)

class BaseTemplateView(TemplateView):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class AdminIndexView(View, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        tenants = get_tenant_model().objects.all().exclude(schema_name='public').exclude(is_template=True)
        users = TenantUser.objects.all()
        staff = Profile.objects.filter()
        customers = Customer.objects.filter()
        return render(request, 'multitenancy/admin/adminUser/index.html',
                      {
                          'nbar': 'admin',
                          'title': 'Dashboard!',
                          'tenants': tenants,
                          'customers': customers,
                          'staff': staff,
                          'users': users
                      }
                      )


class CreateCustomerView(BaseCreateView, LoginRequiredMixin):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')
    template_name = 'multitenancy/admin/adminUser/create_customer.html'


class UpdateCustomerView(BaseUpdateView, LoginRequiredMixin):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')
    template_name = 'multitenancy/admin/adminUser/update_customer.html'


class DeleteCustomerView(LoginRequiredMixin, BaseDeleteView):
    model = Customer
    template_name = "multitenancy/admin/adminUser/delete_customer.html"
    success_url = reverse_lazy("customer_list")

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs['pk']

        user = Customer.objects.filter(id=customer_id)
        user.delete()
        return HttpResponseRedirect(reverse('customer_list'))


class TeamsIndexView(BaseTemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/teamIndex.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['simple_teams'] = SimpleTeam.objects.all()
        context['teams'] = Team.objects.all()
        return context


class TemplateListView(BaseTemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/template_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryset = TenantFilter(queryset=Tenant.objects.filter(is_template=True))   # type: ignore

        context['filter'] = queryset
        return context


class CreateTemplateView(BaseCreateView, LoginRequiredMixin):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('tenant_list')
    template_name = 'multitenancy/admin/adminUser/create_template.html'

    def post(self, request, is_staff=True, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            name = form.cleaned_data["name"]
            tenant_slug = form.cleaned_data["slug"]
            type = form.cleaned_data['type']
            user = request.user

            if not user.is_active:
                raise InactiveError("Inactive user passed to provision tenant")
            tenant_domain = '{}.{}'.format(
                tenant_slug,  settings.TENANT_USERS_DOMAIN)
            DomainModel = get_tenant_domain_model()
            if DomainModel.objects.filter(domain=tenant_domain).exists():
                raise ExistsError('Tenant URL already exists.')
            # time_string = str(int(time.time()))
            # Must be valid postgres schema characters see:
            # https://www.postgresql.org/docs/9.2/static/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
            # We generate unique schema names each time so we can keep tenants around without
            # taking up url/schema namespace.
            schema_name = '{}'.format(tenant_slug)
            domain = None
            tenant = None
            try:

                tenant = Tenant.objects.create(name=name,
                                               slug=tenant_slug,
                                               schema_name=schema_name,
                                               owner=user,
                                               is_template=True,
                                               type=type)
                domain = get_tenant_domain_model().objects.create(domain=tenant_domain,
                                                                  tenant=tenant,
                                                                  is_primary=True)
                tenant.add_user(user, is_superuser=True, is_staff=is_staff)
                tenant.auto_create_schema = False
                tenant.save()
                # Create cursor
                sweetify.success(request, "Successfully Created Tenant!", icon='success', timer=5000)
                # messages.success(request, "Successfully Added Tenant!")
                return redirect("template_list")
            except Exception:
                if domain is not None:
                    domain.delete()
                if tenant is not None:
                    # Flag is set to auto-drop the schema for the tenant
                    tenant.delete(True)
                raise
                return tenant_domain
        # return super().post(request, *args, **kwargs)


class UpdateTemplateView(BaseUpdateView, LoginRequiredMixin):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('template_list')
    template_name = 'multitenancy/admin/adminUser/update_template.html'


class DeleteTenantView(LoginRequiredMixin, BaseDeleteView):
    model = Tenant
    template_name = "multitenancy/admin/adminUser/delete_tenant.html"
    success_url = reverse_lazy("template_list")

    def delete(self, request, *args, **kwargs):
        tenant_id = self.kwargs['pk']

        tenant = Tenant.objects.filter(id=tenant_id)
        tenant.delete()
        return HttpResponseRedirect(reverse('tenant_list'))


class TenantTypes(BaseListView, LoginRequiredMixin):
    template_name = 'multitenancy/admin/adminUser/tenant_types.html'
    model = TenantType


class CreateType(BaseCreateView, LoginRequiredMixin):
    model = TenantType
    fields = ['name']
    success_url = reverse_lazy('tenant_types')
    template_name = 'multitenancy/admin/adminUser/create_tenant_type.html'


class TenantList(BaseTemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/tenant_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = TenantFilter(self.request.GET, queryset=Tenant.objects.all())
        context['filter'] = f
        return context


class CustomerList(BaseTemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/customer_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = CustomerFilter(self.request.GET, queryset=Customer.objects.all())
        context['filter'] = f
        return context


class SettingsIndexView(BaseTemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/settings_list.html"


class PlanListView(BaseListView, LoginRequiredMixin):
    model = Plan
    template_name = 'multitenancy/admin/adminUser/plan_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = PlanFilter(self.request.GET, queryset=Plan.objects.all())
        context['filter'] = f
        return context


class CreatePlanView(BaseCreateView, LoginRequiredMixin):
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy('plan_list')
    template_name = 'multitenancy/admin/adminUser/create_plan.html'


class UpdatePlanView(BaseUpdateView, LoginRequiredMixin):
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy('plan_list')
    template_name = 'multitenancy/admin/adminUser/update_plan.html'


class DeletePlanView(LoginRequiredMixin, BaseDeleteView):
    model = Plan
    template_name = "multitenancy/admin/adminUser/delete_plan.html"
    success_url = reverse_lazy("plan_list")


class UserSubcriptionsListView(BaseListView, LoginRequiredMixin):
    model = UserSubcriptions
    template_name = 'multitenancy/admin/adminUser/usersubscriptions_list.html'


class SettingsView(BaseTemplateView, LoginRequiredMixin):
    template_name = 'multitenancy/admin/adminUser/generalsettings_index.html'
    model = None
    settings_list = []

    # def get_model(self):
    #     """
    #     Return a list of template names to be used for the request. Must return
    #     a list. May not be called if render_to_response() is overridden.
    #     """
    #     if self.model is None:
    #         raise ImproperlyConfigured(
    #             "TemplateResponseMixin requires either a definition of "
    #             "'template_name' or an implementation of 'get_template_names()'")
    #     else:
    #         return [self.model]
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # item = self.model
        # if item not in self.settings_list:
        #     self.settings_list.append(item)

        context['logo'] = Logo.load()
        context['address'] = Address.load()
        context['admin_settings'] = AdminSettings.load()
        context['info'] = GeneralInfo.load()
        return context


class UpdateLogoView(BaseUpdateView, LoginRequiredMixin):

    model = Logo
    form_class = LogoForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_logo.html'


class GeneralInfoView(BaseUpdateView, LoginRequiredMixin):

    model = GeneralInfo
    form_class = GeneralInfoForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_info.html'


class AddressView(BaseUpdateView, LoginRequiredMixin):

    model = Address
    form_class = AddressForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_address.html'


class AdminSettingsView(BaseUpdateView, LoginRequiredMixin):

    model = AdminSettings
    form_class = AdminSettingsForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_adminsettings.html'
