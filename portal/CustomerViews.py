from django.conf import settings
from django.contrib import messages
#from django.core.checks import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from ..portal.forms import CustomerAddTenantForm
from django.contrib import admin
from ..portal.models import Customers
from django.http import request
from tenant_users.compat import (get_tenant_model, TENANT_SCHEMAS, get_public_schema_name,
                                 get_tenant_domain_model, schema_context)
import time
from django.shortcuts import render
from tenant_users.tenants.models import InactiveError, ExistsError
from django.contrib.auth.decorators import login_required, permission_required
from ..customers.models import Client, Domain
from ..users.models import TenantUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView


@login_required
def customer_dashboard(request):
    #customer = Customers.objects.get(customer=request.customer.id)
    return render(request, 'portal/customer_template/home_content.html', {})

@login_required
def sidebar(request):
    customer = Customers.objects.filter(user_id=request.user)
    return render(request, 'portal/customer_template/sidebar_template.html', {'customer': customer})


@login_required
def customer_view_accounts(request):
   # owner= Customers.objects.get(admin=request.user.id)
   # user = Customers.objects.get(id=request.user)
    tenants= Client.objects.filter(owner_id=request.user)
    return render(request, 'portal/customer_template/customer_view_accounts.html', {'tenants':tenants, })

#@permission_required
@login_required
def customer_view_domain(request):
    #user = Client.objects.filter(owner=request.user)
    #tenant= Client.objects.filter(owner_id=request.user)
    #domain_list = []    
    #domains = Domain.objects.filter(tenant=tenant)
    #for domain in domains:
    #    one_domain = (domain.id, domain.domain)
    #    domain_list.append(one_domain)
    #url = domain.split(",")

    #url = Client.objects.filter()

    tenant_list = []
    tenants= Client.objects.filter()
    #for tenant in tenants:
    #    on_tenant = (tenant.id)
    #    tenant_list.append(on_tenant)
        

    domain_list = []
    user = request.user    
    domains = Domain.objects.filter(tenant__owner=user)
    owner = request.user
    for domain in domains:
        one_domain = (domain.id, )
        domain_list.append(one_domain)
        

    return render(request, 'portal/customer_template/customer_view_domains.html', {'domains':domains, "tenants": tenants})




@login_required
def profile(request):
   # user=TenantUser.objects.get(id=request.user.id)
    administrator=Customers.objects.get(admin=request.user)
    location=Customers.objects.get(admin=request.user)
    return render(request, 'portal/customer_template/profile.html', {'nbar': 'admin_profile', 'administrator':administrator, 'location':location })

@login_required
def update_profile(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed!")    
    else:
        address_line = request.POST.get("address_line")
        suburb = request.POST.get("suburb")
        city = request.POST.get("city")
        province = request.POST.get("province")
        postcode = request.POST.get("postcode")
        phone_number = request.POST.get("phone_number")
        organisation = request.POST.get("organisation")

        try:
            user = TenantUser.objects.get(id=customer_id)
            user.customers.address_line = address_line
            user.customers.suburb = suburb
            user.customers.city = city
            user.customers.province = province
            user.customers.postcode = postcode
            user.customers.phone_number = phone_number
            user.customers.organisation = organisation
            user.save()

            customer_model = Customers.objects.get(admin=customer_id)
            # customer_model.admin.first_name = first_name
            # customer_model.admin.last_name = last_name
            # customer_model.admin.username = username
            customer_model.organisation = organisation
            customer_model.save()
            messages.success(request, "Successfully Added Domain!")
            return HttpResponseRedirect("/add_tenant_domain")
        except:
            print(messages.error)(request, "Failed to Add Domain!")
            return HttpResponseRedirect("/add_tenant_domain")


@login_required
def create_tenant(request):
    form = CustomerAddTenantForm()
    user = Customers.objects.get(admin=request.user)
    #service = TenantUser.objects.all()

    return render(request, 'portal/customer_template/add_tenant.html', {'nbar': 'create_tenant', 'form': form})


@login_required
def create_tenant_save(request, is_staff=False):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")

    else:
        form=CustomerAddTenantForm(request.POST, request.FILES)
        if form.is_valid():

        # tenant = None
            name = form.cleaned_data["name"]
            tenant_slug = form.cleaned_data["slug"]
            owner = form.cleaned_data["owner"]
            #tenant_name = request.POST.get('name')
            #tenant_slug = request.POST.get('slug')
            #email = request.POST.get('owner')
            template = form.cleaned_data['templates']
            settings.TENANT_BASE_SCHEMA = template
            user = TenantUser.objects.get(id=request.user.id)

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
                          
                    messages.success(request, "Successfully Added Tenant!")
                    return HttpResponseRedirect("/create_service")
                except:
                    messages.error(request, "Failed to Add Tenant!")
                    return HttpResponseRedirect("/create_service")
        else:
            form=CustomerAddTenantForm(request.POST)
            return render(request, 'portal/customer_template/create_tenant.html', {'nbar': 'create_tenant', 'form': form})


@csrf_exempt
def check_service_exist(request):
    name=request.POST.get("name")
    tenant_obj=Client.objects.filter(name=name).exists()
    if tenant_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
