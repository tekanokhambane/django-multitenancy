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
from multitenancy.settings.models import Address, AdminSettings, GeneralInfo, Logo
from multitenancy.subscriptions.models import Plan, ProductFeature, Subscription
from pinax.teams.models import SimpleTeam, Team
from multitenancy.users.models import Customer, TenantUser
from multitenancy.apps.models import Tenant
from .baseViews import(
    AdminListView,
    AdminDeleteView,
    AdminCreateView,
    AdminUpdateView,
    AdminTemplateView
    )
# env = environ.Env()





class AdminIndexView(View, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        subscriptions = get_tenant_model().objects.all().exclude(schema_name='public').exclude(is_template=True)
        users = TenantUser.objects.all()
        staff = Profile.objects.filter()
        customers = Customer.objects.filter()
        active_tickets = Ticket.objects.select_related('queue').exclude(
        status__in=[Ticket.CLOSED_STATUS, Ticket.RESOLVED_STATUS],
        )

        # open & reopened tickets, assigned to current user
        tickets = active_tickets.filter(
            assigned_to=request.user,
        )

        
        return render(request, 'multitenancy/admin/adminUser/index.html',
                      {
                          'nbar': 'admin',
                          'title': 'Dashboard!',
                          'subscriptions': subscriptions,
                          'customers': customers,
                          'staff': staff,
                          'users': users,
                          'user_tickets':tickets
                      }
                      )


class CreateCustomerView(AdminCreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')
    template_name = 'multitenancy/admin/adminUser/create_customer.html'


class UpdateCustomerView(AdminUpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    success_url = reverse_lazy('customer_list')
    template_name = 'multitenancy/admin/adminUser/update_customer.html'


class DeleteCustomerView(AdminDeleteView):
    model = Customer
    template_name = "multitenancy/admin/adminUser/delete_customer.html"
    success_url = reverse_lazy("customer_list")

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs['pk']

        user = Customer.objects.filter(id=customer_id)
        user.delete()
        return HttpResponseRedirect(reverse('customer_list'))


class TeamsIndexView(AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/teamIndex.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['simple_teams'] = SimpleTeam.objects.all()
        context['teams'] = Team.objects.all()
        return context


class TemplateListView(AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/template_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryset = TenantFilter(queryset=Tenant.objects.filter(is_template=True))   # type: ignore

        context['filter'] = queryset
        
        return context


class CreateTemplateView(AdminCreateView):
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


class UpdateTemplateView(AdminUpdateView):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('template_list')
    template_name = 'multitenancy/admin/adminUser/update_template.html'


class DeleteTenantView(AdminDeleteView):
    model = Tenant
    template_name = "multitenancy/admin/adminUser/delete_tenant.html"
    success_url = reverse_lazy("template_list")

    def delete(self, request, *args, **kwargs):
        tenant_id = self.kwargs['pk']

        tenant = Tenant.objects.filter(id=tenant_id)
        tenant.delete()
        return HttpResponseRedirect(reverse('tenant_list'))



class SubscriptionList(AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/subscription_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = TenantFilter(self.request.GET, queryset=Tenant.objects.filter().exclude(is_template=True))
        context['filter'] = f
        return context


class CustomerList(AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/customer_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = CustomerFilter(self.request.GET, queryset=Customer.objects.all())
        context['filter'] = f
        return context


class SettingsIndexView(AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/settings_list.html"


class PlanListView(AdminListView):
    model = Plan
    template_name = 'multitenancy/admin/adminUser/plan_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = PlanFilter(self.request.GET, queryset=Plan.objects.all())
        context['filter'] = f
        return context


class CreatePlanView(AdminCreateView):
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy('plan_list')
    template_name = 'multitenancy/admin/adminUser/create_plan.html'


class PlanDetailView(AdminTemplateView):
    template_name = "multitenancy/admin/adminUser/plan_detail.html"

    def get_context_data(self, slug,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        plan = Plan.objects.get(slug=slug)
        print(plan.features)
        context['plan'] = plan
        context['form'] =  ProductFeatureForm()
        return context

class FeatureCreateView(View, LoginRequiredMixin):

    @allowed_users(allowed_types=["Admin"])
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



class UpdatePlanView(AdminUpdateView):
    model = Plan
    form_class = PlanForm
    success_url = reverse_lazy('plan_list')
    template_name = 'multitenancy/admin/adminUser/update_plan.html'


class DeletePlanView(AdminDeleteView):
    model = Plan
    template_name = "multitenancy/admin/adminUser/delete_plan.html"
    success_url = reverse_lazy("plan_list")


class UserSubscriptionsListView(AdminListView):
    model = Subscription
    template_name = 'multitenancy/admin/adminUser/usersubscriptions_list.html'


class SettingsView(AdminTemplateView):
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


class UpdateLogoView(AdminUpdateView):

    model = Logo
    form_class = LogoForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_logo.html'

    def get_object(self):
        return self.model.objects.first()


class GeneralInfoView(AdminUpdateView):

    model = GeneralInfo
    form_class = GeneralInfoForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_info.html'

    def get_object(self):
        return self.model.objects.first()


class AddressView(AdminUpdateView):

    model = Address
    form_class = AddressForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_address.html'

    def get_object(self):
        return self.model.objects.first()

class AdminSettingsView(AdminUpdateView):

    model = AdminSettings
    form_class = AdminSettingsForm
    success_url = reverse_lazy('generalsettings_index')
    template_name = 'multitenancy/admin/adminUser/update_adminsettings.html'

    def get_object(self):
        return self.model.objects.first()
