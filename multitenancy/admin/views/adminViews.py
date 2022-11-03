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
from tenant_users.tenants.models import InactiveError, ExistsError
# from .forms import AddCustomerForm, AddStaffForm, AddTenantForm, CompanyAddressForm, CompanyDetailForm, DepartmentCreateForm, EditCustomerForm, EditTenantForm, EditstaffForm, QuickAddCustomerForm, QuickAddStaffForm, TLDForm, PackageForm, ProductForm
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
import json
from account.mixins import LoginRequiredMixin
from multitenancy.admin.filters import CustomerFilter, TenantFilter
from multitenancy.admin.forms import AddCustomerForm
from pinax.teams.models import SimpleTeam, Team
from tenant_users.permissions.models import UserTenantPermissions
# from django_tenants_portal.portal.models.admin_models import Address, CompanyDetails, Department
from multitenancy.users.models import Customer, Staff, TenantUser
from multitenancy.apps.models import Tenant
# from django_tenants_portal.product.models import Product
#from groups_manager.models import Group, Member
# from ..accounts.models import Account

#env = environ.Env()

class AdminIndexView(TemplateView, LoginRequiredMixin):
    template_name= "multitenancy/admin/adminUser/index.html"


# Admin 
@login_required  # type: ignore
def admin_home(request):
    tenants = get_tenant_model().objects.all().exclude(schema_name='public')
    users = TenantUser.objects.all()
    staff = Staff.objects.filter()

    customers = Customer.objects.filter()
    user=request.user
    if user.is_authenticated:
            
        if user.type == "Admin":                  
            print(request.path)
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


class TeamsIndexView(TemplateView, LoginRequiredMixin):
    template_name = "multitenancy/admin/adminUser/teamIndex.html"
    def get_context_data(self,request, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(request.user)
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

def tenant_list(request):
    f = TenantFilter(request.GET, queryset=Tenant.objects.all())
    return render(request, 'multitenancy/admin/adminUser/tenant_list.html', {'filter': f})


def customer_list(request):
    f = CustomerFilter(request.GET, queryset=Customer.objects.all())
    return render(request, 'multitenancy/admin/adminUser/customer_list.html', {'filter': f})



def add_customer(request):
    form = AddCustomerForm()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1": 
                return render(request, 'portal/hod_template/add_customer.html', {'nbar': 'add_customer', 'form': form})


@login_required
def save_customer(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed!")
    else:
        form=AddCustomerForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            phone_number = form.cleaned_data["phone_number"]
            organisation = form.cleaned_data["organisation"]
           

            try:
                user = TenantUser.objects.create_user(
                    email=email, password=password, is_staff=False, first_name=first_name, last_name=last_name, username=username, user_type=3, is_active=True)
                user.account.organisation = organisation
                user.account.phone_number = phone_number
                              
                user.save()
                sweetify.success(request, "Successfully Added Customer!", icon='success', timer=5000)
                
                return HttpResponseRedirect("manage_customer")
            except:
                messages.error(request, "Failed to Add Customer!")
                return HttpResponseRedirect("manage_customer")
        else:
            form=AddCustomerForm(request.POST)
            return render(request, 'portal/hod_template/add_customer.html', {'nbar': 'add_customer', 'form': form})
