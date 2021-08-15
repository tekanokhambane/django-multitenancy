from django.core.files.storage import FileSystemStorage
from django.forms.models import inlineformset_factory
from django.urls.base import reverse, reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django_tenants_portal.core.models.admin_models import Address, CompanyDetails, Department
import os
from django.views.decorators.csrf import csrf_exempt
#import environ
from django.db import connection, transaction
from django.core.exceptions import PermissionDenied
from django.http import response
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from requests.api import request
from .models.user_models import AdminUser, Staff, Customers
from django.core.checks import messages
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.forms import fields
import requests
from ..customers.models import Domain, Client
import time
from django.conf import settings
from django.contrib.auth import get_user_model
from tenant_users.compat import (get_tenant_model, TENANT_SCHEMAS, get_public_schema_name,
                                 get_tenant_domain_model, schema_context)
from tenant_users.tenants.models import InactiveError, ExistsError
from ..users.models import TenantUser
from .forms import AddCustomerForm, AddStaffForm, AddTenantForm, CompanyDetailForm, DepartmentCreateForm, EditCustomerForm, EditTenantForm, EditstaffForm, QuickAddCustomerForm, QuickAddStaffForm, forms
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.mixins import LoginRequiredMixin

#from google.cloud import dns
#from google.cloud import dns

#env = environ.Env()


# Admin 
@login_required
def admin_home(request):
    tenants = Client.objects.all()
    customers = Customers.objects.all()
    staff = Staff.objects.all()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":                  
                return render(request, 'core/hod_template/home_content.html',
                            {'nbar': 'admin',
                            'title': 'Dashboard!',
                            'tenants': tenants,
                            'customers': customers,
                            'staff': staff})

@login_required
def admin_profile(request):
   # user=TenantUser.objects.get(id=request.user.id)
    administrator=AdminUser.objects.get(admin=request.user)
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":              
                return render(request, 'core/hod_template/admin_profile.html', {'nbar': 'admin_profile', 'administrator':administrator })

@login_required
def admin_profile_manage(request):
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/admin_profile.html', {'nbar': 'admin_profile'})

@login_required
def edit_profile(request, admin_id):
    tenants = Client.objects.all()
    adminhod = AdminUser.objects.get(admin=request.user)
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/admin_profile.html', {'adminhod': adminhod, 'tenants': tenants})

@login_required
def edit_profile_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed!</h2>")
    else:
        admin_id = request.POST.get("admin_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")

        try:
            user = TenantUser.objects.get(id=admin_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            admin_model = AdminUser.objects.get(admin=admin_id)
            admin_model.save()
            messages.success(request, "Successfully Edited Profile!")
            return HttpResponseRedirect("/admin_profile/"+admin_id)
        except:
            messages.error(request, "Failed to Edit Profile!")
            return HttpResponseRedirect("/admin_profile/"+admin_id)


#Staff views

@login_required
def add_staff(request):
    form = AddStaffForm() 
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/add_staff.html', {'nbar': 'add_staff', 'form': form})


@login_required
def staff_quick_create(request):
    form = QuickAddStaffForm()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1": 
                return render(request, 'core/hod_template/modals/staff_create_form.html', {'nbar': 'add_staff', 'form': form})

StaffFormSet = inlineformset_factory(TenantUser, Staff, extra=1, fields=['job_description', 'department',])
AddressFormSet = inlineformset_factory(Address, Staff, fields=['job_description'] )

class CreateAddressView(CreateView):
    model = Address
    fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country']
    #template_name = "user"

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["children"] = AddressFormSet(self.request.POST,)
        else:
            data["children"] = AddressFormSet()
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("parents:list")


class CreateStafView(CreateAddressView):
    model = TenantUser
    fields = ['first_name', 'last_name', 'email', 'password' ]
    

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["children"] = StaffFormSet(self.request.POST,)
        else:
            data["children"] = StaffFormSet()
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("parents:list")


@login_required
def add_staff_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        form=AddStaffForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            job_description = form.cleaned_data["job_description"]
            depart_field= form.cleaned_data["department"]

            #skills = form.cleaned_data["skills"]
            #educational_qualification = form.cleaned_data[
            #    "educational_qualification"]
           
            try:
                user = TenantUser.objects.create_user(
                    email=email, first_name=first_name, last_name=last_name, username=username, password=password, user_type=2, is_active=True, is_staff=True)
                
                dep = Department.objects.get(id=depart_field)
                user.staff.job_description = job_description
                user.staff.departement = dep
                #user.staff.skills = skills
                #user.staff.educational_qualification = educational_qualification
                user.save()
                messages.success(request, "Successfully Added Staff!")
                return HttpResponseRedirect("/admin/staff/create/")
            except:
                messages.error(request, "Failed to Add Staff!")
                return HttpResponseRedirect("/admin/staff/create/")
        else:
            form=AddStaffForm(request.POST)
            return render(request, 'core/hod_template/add_staff.html', {'nbar': 'add_staff', 'form': form})


@login_required
def quick_staff_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        form=QuickAddStaffForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            
           
            try:
                user = TenantUser.objects.create_user(
                    email=email, first_name=first_name, last_name=last_name, username=username, password=password, user_type=2, is_active=True, is_staff=True)
               
                
                user.save()
                messages.success(request, "Successfully Added Staff!")
                return HttpResponseRedirect("/admin/staff/view/")
            except:
                messages.error(request, "Failed to Add Staff!")
                return HttpResponseRedirect("/admin/staff/view/")
        else:
            form=AddStaffForm(request.POST)
            return render(request, 'core/hod_template/manage_staff.html', {'nbar': 'add_staff', 'form': form})


@login_required
def manage_staff(request):
    staff = Staff.objects.all()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/manage_staff.html', {'nbar': 'manage_staff', 'staff': staff})

@login_required
def manage_customer(request):
    customers = Customers.objects.all()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/manage_customer.html', {'nbar': 'manage_customer', 'customers': customers})


@login_required
def edit_staff(request, staff_id):    
    request.session["staff_id"]=staff_id
    staff = Staff.objects.get(admin=staff_id)
    form=EditstaffForm()
    form.fields['email'].initial=staff.admin.email
    form.fields['first_name'].initial=staff.admin.first_name
    form.fields['last_name'].initial=staff.admin.last_name
    form.fields['username'].initial=staff.admin.username
    form.fields['job_description'].initial=staff.job_description
    form.fields['department'].initial=staff.department
    form.fields['skills'].initial=staff.skills
    form.fields['educational_qualification'].initial=staff.educational_qualification
    #form.fields['address'].initial=staff.address
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/edit_staff_template.html', {'nbar': 'manage_staff','staff': staff, "form":form},)


@login_required
def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed!</h2>")
    else:
        staff_id = request.session.get("staff_id")
        if staff_id==None:
            return HttpResponseRedirect('/manane_staff')
        form=EditstaffForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data["email"]
           # password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            job_description = form.cleaned_data["job_description"]
            department = form.cleaned_data["department"]
            skills = form.cleaned_data["skills"]
            educational_qualification = form.cleaned_data[
                "educational_qualification"]
            address = form.cleaned_data["address"]

            try:
                user = TenantUser.objects.get(id=staff_id)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.staff.job_description = job_description
                user.staff.department = department
                user.staff.skills = skills
                user.staff.educational_qualification = educational_qualification
                user.staff.address = address
                user.save()

                staff_model = Staff.objects.get(admin=staff_id)
                #staff_model.first_name = first_name
                #staff_model.last_name = last_name
                #staff_model.username = username
                staff_model.job_description = job_description
                staff_model.skills = skills
                staff_model.department = department
                staff_model.address = address
                staff_model.save()
                messages.success(request, "Successfully Edited Staff!")
                return HttpResponseRedirect("/dashboard/edit/staff/"+staff_id)
            except:
                messages.error(request, "Failed to Edit Staff!")
                return HttpResponseRedirect("/dashboard/edit/staff/"+staff_id)
        else:
            form=EditstaffForm(request.POST)
            staff = Staff.objects.get(admin=staff_id)
            return render(request, 'core/hod_template/edit_staff_template.html', {'staff':staff, 'form':form, "id":staff_id, "username":username})


class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = Staff
    template_name = "core/hod_template/delete_staff.html"
    success_url = reverse_lazy("manage_staff")


class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = "core/hod_template/view_staff.html"


# Customer View


@login_required
def add_customer(request):
    form = AddCustomerForm()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1": 
                return render(request, 'core/hod_template/add_customer.html', {'nbar': 'add_customer', 'form': form})


@login_required
def add_customer_save(request):
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
                    email=email, password=password, first_name=first_name, last_name=last_name, username=username, user_type=3, is_active=True, is_staff=False)
                user.customers.organisation = organisation
                user.customers.phone_number = phone_number
                              
                user.save()
                messages.success(request, "Successfully Added Customer!")
                return HttpResponseRedirect("add_customer/")
            except:
                messages.error(request, "Failed to Add Customer!")
                return HttpResponseRedirect("add_customer/")
        else:
            form=AddCustomerForm(request.POST)
            return render(request, 'core/hod_template/add_customer.html', {'nbar': 'add_customer', 'form': form})

def customer_quick_create(request):
    form = QuickAddCustomerForm()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1": 
                return render(request, 'core/hod_template/modals/customer_create_form.html', {'nbar': 'add_customer', 'form': form})


@login_required
def quick_customer_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed!")
    else:
        form=QuickAddCustomerForm(request.POST, request.FILES)
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
                    email=email, password=password, first_name=first_name, last_name=last_name, username=username, user_type=3, is_active=True, is_staff=True)
                user.customers.organisation = organisation
                user.customers.phone_number = phone_number
                             
                user.save()
                messages.success(request, "Successfully Added Customer!")
                return HttpResponseRedirect("/admin/customer/view/")
            except:
                messages.error(request, "Failed to Add Customer!")
                return HttpResponseRedirect("/admin/customer/view/")
        else:
            form=QuickAddCustomerForm(request.POST)
            return render(request, 'core/hod_template/manage_customer.html', {'nbar': 'add_customer', 'form': form})



    
class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customers
    template_name = "core/hod_template/delete_customer.html"
    success_url = reverse_lazy("manage_customer")    


@login_required
def edit_customer(request, customer_id):
    #customer_address = Customers.objects.filter()
   # address_id = Address.objects.all()
    request.session["customer_id"]=customer_id
    #request.session["address_id"]=address_id
    customer = Customers.objects.get(admin=customer_id)
   # location = Customers.objects.get(address=customer_id)
    #userprofile = TenantUser.objects
    form=EditCustomerForm()
    form.fields['email'].initial=customer.admin.email
    form.fields['first_name'].initial=customer.admin.first_name
    form.fields['last_name'].initial=customer.admin.last_name
    form.fields['username'].initial=customer.admin.username
    form.fields['organisation'].initial=customer.organisation
   #form.fields['address_line_1'].initial= location.address.address_line_1
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/edit_customer_template.html', {'nbar': 'manage_customer', "form":form, 'id': customer_id, "customer": customer, },)


@login_required
def edit_customer_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed!</h2>")
    else:
        customer_id = request.session.get("customer_id")
        if customer_id==None:
            return HttpResponseRedirect('/manage_customer')
        form=EditCustomerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
        # password = request.POST.get("password")
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            organisation = form.cleaned_data["organisation"]

            try:
                user = TenantUser.objects.get(id=customer_id)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.customers.organisation = organisation
                user.save()

                customer_model = Customers.objects.get(admin=customer_id)
               # customer_model.admin.first_name = first_name
               # customer_model.admin.last_name = last_name
               # customer_model.admin.username = username
                customer_model.organisation = organisation
                customer_model.save()
                messages.success(request, "Successfully Edited Customer!")
                return HttpResponseRedirect("/dashboard/edit/customer/"+customer_id)
            except:
                messages.error(request, "Failed to Edit Customer!")
                return HttpResponseRedirect("/dashboard/edit/customer/"+customer_id)
        else:
            form=EditCustomerForm(request.POST)
            customer = Customers.objects.get(admin=customer_id)
            return render(request, 'core/hod_template/edit_customer_template.html', {'customer':customer, 'form':form, "id":customer_id})


# Tenant Views

@login_required
def add_tenant(request):
    form = AddTenantForm()
    #user = TenantUser.objects.filter(user_type=3)
    #user = TenantUser.objects.all()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/add_tenant.html', {'nbar': 'add_tenant', 'form': form})


@login_required
def add_tenant_save(request, is_staff=True):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")

    else:
        form=AddTenantForm(request.POST, request.FILES)
        if form.is_valid():

        # tenant = None
            name = form.cleaned_data["name"]
            tenant_slug = form.cleaned_data["slug"]
            owner = form.cleaned_data["owner"]
            #tenant_name = request.POST.get('name')
            #tenant_slug = request.POST.get('slug')
            #email = request.POST.get('owner')
            settings.TENANT_CREATION_FAKES_MIGRATIONS = True
            template = form.cleaned_data['templates']
            settings.TENANT_BASE_SCHEMA = template
            user = TenantUser.objects.get(id=owner)

            TenantModel = get_tenant_model

           # if not user.is_active:
             #   raise InactiveError("Inactive user passed to provision tenant")
            tenant_domain = '{}.{}.{}'.format(
                tenant_slug, 'site', settings.TENANT_USERS_DOMAIN)

            if TENANT_SCHEMAS:
                if TenantModel.objects.filter(domain_url=tenant_domain).first():
                    raise ExistsError("Tenant URL already exists")
            else:
                if get_tenant_domain_model().objects.filter(domain=tenant_domain).first():
                    raise ExistsError("Tenant URL already exists.")
                time_string = str(int(time.time()))
                # Must be valid postgres schema characters see:
                # https://www.postgresql.org/docs/9.2/static/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
                # We generate unique schema names each time so we can keep tenants around without
                # taking up url/schema namespace.
                schema_name = '{}_{}'.format(tenant_slug, time_string)
                #domain = None

                try:
                 
                  
                    tenant = Client.objects.create(name=name,
                                                slug=tenant_slug,
                                                schema_name=schema_name,
                                                owner=user)
                    domain = get_tenant_domain_model().objects.create(domain=tenant_domain,
                                                                    tenant=tenant,
                                                                    is_primary=True)
                    tenant.add_user(user, is_superuser=True, is_staff=is_staff)
                    tenant.auto_create_schema = False
                    tenant.save()




                    # Create cursor
                          
                    messages.success(request, "Successfully Added Tenant!")
                    return HttpResponseRedirect("/dashboard/add/tenant")
                except:
                    messages.error(request, "Failed to Add Tenant!")
                    return HttpResponseRedirect("/dashboard/add/tenant")
        else:
            form=AddTenantForm(request.POST)
            return render(request, 'core/hod_template/add_tenant.html', {'nbar': 'add_tenant', 'form': form})


@login_required
def manage_tenant(request):
    tenant = Client.objects.all()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/manage_tenant.html', {'nbar': 'manage_tenant', 'tenant': tenant})


@login_required
def edit_tenant(request, tenant_id):
    request.session["tenant_id"]=tenant_id
    #tenant = get_tenant_model().objects.get(id=tenant_id)
    tenant = get_tenant_model().objects.get(pk=tenant_id)

    form=EditTenantForm()
    form.fields['name'].initial=tenant.name
    form.fields['description'].initial=tenant.description
    form.fields['slug'].initial=tenant.slug
   # form.fields['owner_id'].initial=tenant.owner_id
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/edit_tenant_template.html', {'nbar': 'manage_tenant', 'tenant': tenant, 'form':form})

@login_required
def edit_tenant_save(request):
    if request.method !="POST":
        return HttpResponse("<h2>Method Not Allowed!</h2>")
    else:
        tenant_id = request.session.get("tenant_id")
        if tenant_id==None:
            return HttpResponseRedirect('/manage_tenant')
        form=EditTenantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            slug = form.cleaned_data["slug"]
           # owner_id = form.cleaned_data["owner_id"]


        
            try:
                tenant = get_tenant_model().objects.get(pk=tenant_id)
                tenant.name = name
                tenant.slug = slug
                tenant.description = description
               # tenant.owner_id = owner_id
                tenant.save()
                messages.success(request, "Successfully Edited Tenant!")
                return HttpResponseRedirect("tenant/edit/"+tenant_id)
            except:
                messages.error(request, "Failed to Edit Tenant!")
                return HttpResponseRedirect("tenant/edit/"+tenant_id)
        else:
            form=EditTenantForm(request.POST)
            tenant = get_tenant_model().objects.get(pk=tenant_id)
            return render(request, 'core/hod_template/edit_tenant_template.html', {'tenant':tenant, 'form':form, "id":tenant_id})


# Add Domain

@login_required
def add_tenant_domain(request):
    domain = Domain.objects.all()
    tenant = Client.objects.filter()
    domain = Domain.objects.filter()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1": 
                return render(request, 'core/hod_template/add_domain_template.html', {'tenant': tenant, 'domain': domain, 'nbar': 'add_tenant_domain'},)


@login_required
def add_domain_save(request, is_primary=False):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        domain = request.POST.get('domain')
        tenant_id = request.POST.get("tenant")
        tenant = Client.objects.get(pk=tenant_id)
        is_primary = request.POST.get("is_primary")
        try:
        
            domain_name = Domain.objects.create(domain=domain, tenant=tenant, is_primary=is_primary)
            
           
            domain_name.save()
            messages.success(request, "Successfully Added Domain!")
            return HttpResponseRedirect("/add_tenant_domain")
        except:
            print(messages.error)(request, "Failed to Add Domain!")
            return HttpResponseRedirect("/add_tenant_domain")

@login_required
def manage_domain(request):
    domain = Domain.objects.all()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/manage_domain.html', {'nbar': 'manage_domain', 'domain': domain})


@login_required
def edit_domain(request, domain_id):
    #tenant_id = get_tenant_domain_model().objects.filter(tenant_id)
    #tenant = Client.objects.filter(id=tenant_id)
    #domain_id = get_tenant_model().objects.filter(pk=domain_id)
    domain = get_tenant_domain_model().objects.filter(id=domain_id)
    #tenant = get_tenant_domain_model().filter(id=t)
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/edit_domain_template.html', {'nbar': 'manage_domain', 'domain':domain,})

@login_required
def edit_domain_save(request):
    if request.method !='POST':
        return HttpResponseRedirect("Method Not Allowed")
    else:
        domain_id = request.POST.get("id")
       # domain_id = get_tenant_domain_model().objects.get(id=domain_id)
        domain = request.POST.get("domain")
        is_primary = request.POST.get("is_primary")      
       
        try:
            domain = Domain.objects.get(domain=domain)
            domain.domain = domain
            domain.is_primary = is_primary           
            domain.save()
            messages.success(request, "Successfully Edited Tenant Domain!")
            return HttpResponseRedirect("/domain/edit/"+domain_id)
        except:
            messages.error(request, "Failed to Edit Tenant Domain!")
            return HttpResponseRedirect("/domain/edit/"+domain_id)

# Department Views

class DepartmentListView(ListView, LoginRequiredMixin):
    model = Department
    template_name = 'core/hod_template/department_list.html'
    #fields = ['name']


def create_department_view(request):
    form = DepartmentCreateForm()
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/modals/department_create_form.html', {'nbar': 'add_customer', 'form': form})


#class DepartmentCreateView(CreateView):
#    model = Department
    #template_name = 'core/hod_template/modals/department_create_form.html'
#    fields = ['name']


@login_required
def quick_department_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed!")
    else:
        form=DepartmentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]         
            

            try:
                department = Department.objects.create(
                    name=name, )                                           
                department.save()
                messages.success(request, "Successfully Added Department!")
                return HttpResponseRedirect("/admin/departments/")
            except:
                messages.error(request, "Failed to Add Customer!")
                return HttpResponseRedirect("/admin/departments/")
        else:
            form=DepartmentCreateForm(request.POST)
            return render(request, 'core/hod_template/modals/department_create_form.html', {'nbar': 'department', 'form': form})




class AddressListView(ListView, LoginRequiredMixin):
    model = Address
    template_name = 'core/hod_template/address_list.html'


# Company details

class CompanyListView(TemplateView, LoginRequiredMixin):
   # model = CompanyDetails
    template_name = 'core/hod_template/company_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_address = Address.objects.get_or_create(id=1)
        company_name = CompanyDetails.objects.get_or_create(id=1)
       # address = CompanyDetails.objects.get(address_id=company_address)

        context['company_details'] = company_name[0]
       # context['company_address'] = address[0]
        return context

class CompanyUpdateView(UpdateView, LoginRequiredMixin):
    model = CompanyDetails
    form_class = CompanyDetailForm
   # fields = ["name", "logo", "website", "phone", "email"]
    success_url = reverse_lazy('company_details')
    template_name = 'core/hod_template/companydetails_form.html'

@login_required
def update_company(request, company_id):
    request.session["company_id"]=company_id
    companydetails = CompanyDetails.objects.get(id=company_id)
    form=CompanyDetailForm()
    form.fields['email'].initial=companydetails.email
    form.fields['name'].initial=companydetails.name
    form.fields['website'].initial=companydetails.website
    form.fields['phone'].initial=companydetails.phone
    form.fields['logo'].initial=companydetails.logo
    user=request.user
    if user.is_authenticated:
            if user.user_type == "1":
                return render(request, 'core/hod_template/update_company-details.html', {'nbar': 'update_company', "form":form, 'company_id': company_id},)


def update_company_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not Allowed!</h2>")
    else:
        company_id= request.session.get("company_id")
        form=CompanyDetailForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            name = form.cleaned_data["name"]
            website = form.cleaned_data["website"]

            if request.FILES.get('logo', False):
                logo=request.FILES["logo"]
                fs=FileSystemStorage()
                filename=fs.save(logo.name, logo)
                logo_url=fs.url(filename)
            else:
                logo_url=None
            
            try:
                details = CompanyDetails.objects.get(id=company_id)
                details.name = name
                details.email = email
                details.phone = phone
                details.website = website
                if logo_url != None:
                    details.logo = logo_url
                details.save()
                del request.session["company_id"]
                messages.success(request, "Successfully Updated Company Details!")
                return HttpResponseRedirect(reverse_lazy("company_details"))
            except:
                messages.error(request, "Failed to update company details!")
                return HttpResponseRedirect(reverse_lazy("update_company", kwargs={"company_id": company_id}))
        else:
            form=CompanyDetailForm(request.POST)
            details= CompanyDetails.objects.get(id=company_id)
            return render(request, 'core/hod_template/update_company-details.html', {'nbar': 'update_company', "form":form, 'company_id': company_id, })

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=TenantUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=TenantUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_tenant_exist(request):
    name=request.POST.get("name")
    tenant_obj=Client.objects.filter(name=name).exists()
    if tenant_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_slug_exist(request):
    slug=request.POST.get("slug")
    tenant_obj=Client.objects.filter(slug=slug).exists()
    if tenant_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
# Google cloud dns

