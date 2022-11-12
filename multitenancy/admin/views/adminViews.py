from django.core.files.storage import FileSystemStorage
from django.forms.models import inlineformset_factory
from django.urls.base import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
import sweetify
import os
from django.views.decorators.csrf import csrf_exempt
#import environ
from django.db import connection, transaction
from django.core.exceptions import PermissionDenied
from django.http import response
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from requests.api import request
# from .models.user_models import AdminUser, Employee
from django.core.checks import messages
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.forms import fields
import requests
# from ..customers.models import RegisteredDomain, Domain, Client, DomainTld, Packages
import time
from django.conf import settings
from django.contrib.auth import get_user_model
from tenant_users.tenants.utils import (get_tenant_model, get_public_schema_name,
                                 get_tenant_domain_model)
from django_tenants.utils import schema_context
from tenant_users.tenants.models import InactiveError, ExistsError, UserProfile
# from .forms import AddCustomerForm, AddStaffForm, AddTenantForm, CompanyAddressForm, CompanyDetailForm, DepartmentCreateForm, EditCustomerForm, EditTenantForm, EditstaffForm, QuickAddCustomerForm, QuickAddStaffForm, TLDForm, PackageForm, ProductForm
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, View
from django.contrib.auth.decorators import login_required
import json
from account.mixins import LoginRequiredMixin
from multitenancy.admin.filters import CustomerFilter, PackageFilter, TenantFilter
from multitenancy.admin.forms import CustomerForm, PackageForm, TenantForm
from pinax.teams.models import SimpleTeam, Team
from tenant_users.permissions.models import UserTenantPermissions
# from django_tenants_portal.portal.models.admin_models import Address, CompanyDetails, Department
from multitenancy.users.models import Customer, Staff, TenantUser
from multitenancy.apps.models import Package, Tenant, TenantType
# from django_tenants_portal.product.models import Product
#from groups_manager.models import Group, Member
# from ..accounts.models import Account

#env = environ.Env()

class AdminIndexView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        tenants = get_tenant_model().objects.all().exclude(schema_name='public')
        users = TenantUser.objects.all()
        staff = Staff.objects.filter()
        customers = Customer.objects.filter()
        user=request.user
        if user.type == "Admin":                  
            return render(request, 'multitenancy/admin/adminUser/index.html',
                        {
                        'nbar': 'admin',
                        'title': 'Dashboard!',
                        'tenants': tenants,
                        'customers': customers,
                        'staff': staff,
                            'users':users
                        }
                        )

class CreateCustomerView(CreateView, LoginRequiredMixin):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')
    template_name = 'multitenancy/admin/adminUser/create_customer.html'


class UpdateCustomerView(UpdateView, LoginRequiredMixin):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')
    template_name = 'multitenancy/admin/adminUser/update_customer.html'


class DeleteCustomerView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = "multitenancy/admin/adminUser/delete_customer.html"
    success_url = reverse_lazy("customer_list")

    
    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs['pk']
        

        user = Customer.objects.filter(id=customer_id)
        user.delete()
        return HttpResponseRedirect(reverse('customer_list'))



class TeamsIndexView(TemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/teamIndex.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['simple_teams'] = SimpleTeam.objects.all()
        context['teams'] = Team.objects.all()
        return context


class TenantListView(TemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/tenant_list.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryset =  TenantFilter(queryset=Tenant.objects.filter())   # type: ignore

        context['filter'] = queryset
        return context

class CreateTenantView(CreateView, LoginRequiredMixin):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('tenant_list')
    template_name = 'multitenancy/admin/adminUser/create_tenant.html'

    def post(self, request,is_staff=True, *args, **kwargs):
        form=self.get_form()
        if form.is_valid():
            name = form.cleaned_data["name"]
            tenant_slug = form.cleaned_data["slug"]
            type = form.cleaned_data['type']
            user = request.user
            TenantModel = get_tenant_model

            if not user.is_active:
               raise InactiveError("Inactive user passed to provision tenant")
            tenant_domain = '{}.{}'.format(
                tenant_slug,  settings.TENANT_USERS_DOMAIN)
            DomainModel = get_tenant_domain_model()
            if DomainModel.objects.filter(domain=tenant_domain).exists():
                raise ExistsError('Tenant URL already exists.')
            time_string = str(int(time.time()))
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
                #messages.success(request, "Successfully Added Tenant!")
                return redirect("tenant_list")
            except:
                if domain is not None: 
                    domain.delete() 
                if tenant is not None: 
                    # Flag is set to auto-drop the schema for the tenant
                    tenant.delete(True) 
                raise
                return tenant_domain
        #return super().post(request, *args, **kwargs)


class DeleteTenantView(LoginRequiredMixin, DeleteView):
    model = Tenant
    template_name = "multitenancy/admin/adminUser/delete_tenant.html"
    success_url = reverse_lazy("tenant_list")

    
    def delete(self, request, *args, **kwargs):
        tenant_id = self.kwargs['pk']
        

        tenant = Tenant.objects.filter(id=tenant_id)
        tenant.delete()
        return HttpResponseRedirect(reverse('tenant_list'))

class TenantTypes(ListView, LoginRequiredMixin):
    template_name = 'multitenancy/admin/adminUser/tenant_types.html'
    model = TenantType

class CreateType(CreateView, LoginRequiredMixin):
    model= TenantType
    fields = ['name']
    success_url = reverse_lazy('tenant_types')
    template_name = 'multitenancy/admin/adminUser/create_tenant_type.html'


class TenantList(TemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/tenant_list.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = TenantFilter(self.request.GET, queryset=Tenant.objects.all())
        context['filter'] = f
        return context

class CustomerList(TemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/customer_list.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = CustomerFilter(self.request.GET, queryset=Customer.objects.all())
        context['filter'] = f
        return context

class SettingsIndexView(TemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/settings_list.html"


class PackageListView(ListView, LoginRequiredMixin):
    model = Package
    template_name= 'multitenancy/admin/adminUser/package_list.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        f = PackageFilter(self.request.GET, queryset=Package.objects.all())
        context['filter'] = f
        return context

class CreatePackageView(CreateView, LoginRequiredMixin):
    model = Package
    form_class = PackageForm
    template_name = 'multitenancy/admin/adminUser/create_package.html'