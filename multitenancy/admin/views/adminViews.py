from django.urls.base import reverse, reverse_lazy
import sweetify
# import environ
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
# import time
from django.forms.models import modelform_factory
from django.conf import settings
from tenant_users.tenants.utils import (get_tenant_model,
                                        get_tenant_domain_model)
from multitenancy.admin.decorators import allowed_users
from multitenancy.profiles.models import Profile
from tenant_users.tenants.models import InactiveError, ExistsError
from django.views.generic import View
from account.mixins import LoginRequiredMixin
from helpdesk.models import Ticket
from multitenancy.admin.filters import CustomerFilter, PlanFilter, TenantFilter
from multitenancy.admin.forms import (
    AddressForm,
    AdminSettingsForm,
    CustomerForm,
    CustomerUpdateForm,
    GeneralInfoForm,
    LogoForm,
    PlanForm,
    ProductFeatureForm,
    TenantForm)
from django.views.generic import TemplateView, ListView, DeleteView, View, CreateView, UpdateView, DetailView
from multitenancy.settings.models import Address, AdminSettings, GeneralInfo, Logo
from multitenancy.subscriptions.models import Plan, ProductFeature, ProductType, Subscription
from pinax.teams.models import SimpleTeam, Team
from account.mixins import LoginRequiredMixin
from multitenancy.users.models import Customer, TenantUser
from multitenancy.apps.models import Tenant
from .baseViews import(
    AdminListView,
    AdminDeleteView,
    AdminCreateView,
    AdminUpdateView,
    AdminTemplateView,
    AdminView,
    AdminDetailView
    )
# env = environ.Env()





class AdminIndexView(LoginRequiredMixin ,AdminTemplateView):
    template_name = 'multitenancy/admin/adminUser/index.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['subscriptions'] = get_tenant_model().objects.all().exclude(schema_name='public').exclude(is_template=True)
        context['users'] = TenantUser.objects.all()
        ProductType.objects.create_defaults()
        context['staff'] = Profile.objects.filter()
        context['customers'] = Customer.objects.filter()
        context['users'] = TenantUser.objects.all()
        context['active_tickets'] = Ticket.objects.select_related('queue').exclude(
        status__in=[Ticket.CLOSED_STATUS, Ticket.RESOLVED_STATUS],
        )
        return context
    


class CreateCustomerView(LoginRequiredMixin ,AdminCreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')
    template_name = 'multitenancy/admin/adminUser/create_customer.html'


class UpdateCustomerView(LoginRequiredMixin ,AdminUpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    success_url = reverse_lazy('customer_list')
    template_name = 'multitenancy/admin/adminUser/update_customer.html'


class DeleteCustomerView(LoginRequiredMixin ,AdminDeleteView):
    model = Customer
    template_name = "multitenancy/admin/adminUser/delete_customer.html"
    success_url = reverse_lazy("customer_list")

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs['pk']

        user = Customer.objects.filter(id=customer_id)
        user.delete()
        return HttpResponseRedirect(reverse('customer_list'))


class TeamsIndexView(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/teamIndex.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['simple_teams'] = SimpleTeam.objects.all()
        context['teams'] = Team.objects.all()
        return context


class TemplateListView(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/template_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryset = TenantFilter(queryset=Tenant.objects.filter(is_template=True))   # type: ignore

        context['filter'] = queryset
        
        return context


class CreateTemplateView(LoginRequiredMixin ,AdminCreateView):
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
                    raise Exception('Tenant already exists')
                return tenant_domain
        # return super().post(request, *args, **kwargs)


class UpdateTemplateView(LoginRequiredMixin ,AdminUpdateView):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('template_list')
    template_name = 'multitenancy/admin/adminUser/update_template.html'


class DeleteTenantView(LoginRequiredMixin ,AdminDeleteView):
    model = Tenant
    template_name = "multitenancy/admin/adminUser/delete_tenant.html"
    success_url = reverse_lazy("template_list")

    def delete(self, request, *args, **kwargs):
        tenant_id = self.kwargs['pk']

        tenant = Tenant.objects.filter(id=tenant_id)
        tenant.delete()
        return HttpResponseRedirect(reverse('tenant_list'))



class SubscriptionList(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/subscription_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = TenantFilter(self.request.GET, queryset=Tenant.objects.filter().exclude(is_template=True))
        context['filter'] = f
        return context


class CustomerList(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/customer_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = CustomerFilter(self.request.GET, queryset=Customer.objects.all())
        context['filter'] = f
        return context


class SettingsIndexView(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/settings_list.html"


class PlanListView(LoginRequiredMixin ,AdminListView):
    
    model = Plan
    template_name = 'multitenancy/admin/adminUser/plan_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = PlanFilter(self.request.GET, queryset=Plan.objects.all())
        context['filter'] = f
        return context


class CreatePlanView(LoginRequiredMixin ,AdminCreateView):
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy('plan_list')
    template_name = 'multitenancy/admin/adminUser/create_plan.html'


class PlanDetailView(LoginRequiredMixin ,AdminDetailView):
    template_name = "multitenancy/admin/adminUser/plan_detail.html"
    model = Plan
    # context_object_name = "plan"
    #slug_field = "slug"
    # def get_context_data(self, slug,*args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     plan = Plan.objects.get(slug=slug)
    #     print(plan.features)
    #     context['plan'] = plan
    #     context['form'] =  ProductFeatureForm()
    #     return context

class FeatureCreateView(LoginRequiredMixin, AdminView):

    
    def post(self, request, *args: str, **kwargs):
        if request.method != "POST":
            return HttpResponseRedirect("Method Not Allowed")
        else:
            form = ProductFeatureForm(request.POST)
            print(request.content_params)
            if form.is_valid():
                name = form.cleaned_data["name"]
                description = form.cleaned_data["description"]
                
                plan_name = form.cleaned_data["plan_name"]
                plan = form.cleaned_data["plan"]
                feature = None
                
                try:
                    feature = ProductFeature.objects.create(name=name, description=description)
                    feature.save()
                    print(feature.pk)
                    feature_plan = Plan.objects.get(id=plan)
                    feature_plan.features.add(feature)
                    print(feature_plan.pk)
                    feature_plan.add_feature(feature.pk)
                    
                    sweetify.success(request, "Successfully Added Feature!", icon='success', timer=5000)
                    return HttpResponseRedirect(f"/admin/settings/plans/{plan_name}/")
                except:                               
                    sweetify.error(request, "Failed to Add Feature!")
                    return HttpResponseRedirect(f"/admin/settings/plans/{plan_name}/")
            else:
                form=ProductFeatureForm(request.POST)
                return render(request, 'multitenancy/admin/adminUser/plan_detail.html', {"feature_form":form})



class UpdatePlanView(LoginRequiredMixin, AdminUpdateView):
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy('plan_list')
    template_name = 'multitenancy/admin/adminUser/update_plan.html'


class DeletePlanView(LoginRequiredMixin, AdminDeleteView):
    model = Plan
    template_name = "multitenancy/admin/adminUser/delete_plan.html"
    success_url = reverse_lazy("plan_list")


class UserSubscriptionsListView(LoginRequiredMixin, AdminListView):
    model = Subscription
    template_name = 'multitenancy/admin/adminUser/usersubscriptions_list.html'


class SettingsView(LoginRequiredMixin, AdminTemplateView):
    template_name = 'multitenancy/admin/adminUser/generalsettings_index.html'
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
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_logo.html'

    def get_object(self):
        return self.model.objects.first()


class GeneralInfoView(LoginRequiredMixin, AdminUpdateView):

    model = GeneralInfo
    form_class = GeneralInfoForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_info.html'

    def get_object(self):
        return self.model.objects.first()


class AddressView(LoginRequiredMixin, AdminUpdateView):

    model = Address
    form_class = AddressForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_address.html'

    def get_object(self):
        return self.model.objects.first()

class AdminSettingsView(LoginRequiredMixin, AdminUpdateView):

    model = AdminSettings
    form_class = AdminSettingsForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_adminsettings.html'

    def get_object(self):
        return self.model.objects.first()

class ProductTypeListView(LoginRequiredMixin, AdminListView):
    model = ProductType

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        
        context['object_list'] = ProductType.objects.all()
        return context

    template_name = 'multitenancy/admin/adminUser/product_type_list.html'