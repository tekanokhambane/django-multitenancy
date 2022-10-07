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
from pinax.teams.models import SimpleTeam, Team
# from django_tenants_portal.portal.models.admin_models import Address, CompanyDetails, Department
from django_multitenancy.users.models import TenantUser
# from django_tenants_portal.product.models import Product
#from groups_manager.models import Group, Member
# from ..accounts.models import Account

#env = environ.Env()

class AdminIndexView(TemplateView, LoginRequiredMixin):
    template_name= "django_multitenancy/admin/adminUser/index.html"


# Admin 
@login_required  # type: ignore
def admin_home(request):
    tenants = get_tenant_model().objects.all().exclude(schema_name='public')
    users = TenantUser.objects.all()
    customers = TenantUser.objects.filter(user_type=3)
    staff = TenantUser.objects.filter(user_type=2)
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":                  
                return render(request, 'django_multitenancy/admin/adminUser/index.html',
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
    template_name = "django_multitenancy/admin/adminUser/teamIndex.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['simple_teams'] = SimpleTeam.objects.all()
        context['teams'] = Team.objects.all()
        return context
