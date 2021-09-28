from os import name
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib import auth
#from django.contrib.auth import u
from django.urls import path, include, re_path

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django_tenants_portal.portal import HodViews, views, StaffViews, CustomerViews
from django.contrib import admin
from django_tenants_portal.customers.views import client_list, client_detail
#from portal.HodViews import GetEmails
urlpatterns = [
    # Admin
    path('client/', client_list),
    path('detail/client/', client_detail),
    path('djangoadmin/', admin.site.urls),
    #url(r'^', include('saas.urls')),
    path('demo/', views.showDemoPage),
    path('', views.ShowLoginPage, name="show_login"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('get_user_details', views.GetUserDetails),
    path('logout', views.logout_user, name="logout" ),
    path('login', views.doLogin, name="doLogin"),
    path('admin/', HodViews.admin_home, name="dashboard"),
    path('admin/profile/', HodViews.admin_profile, name="admin_profile"),
    path('edit_profile_save/', HodViews.edit_profile_save, name="edit_profile_save"),
   # path('admin_profile/', HodViews.edit_profile, name="admin_profile"),
    path('admin/staff/create/', HodViews.add_staff, name="add_staff"),
    path('quick_staff_save', HodViews.quick_staff_save, name="quick_staff_save"),
    path('staff_quick_create', HodViews.staff_quick_create, name="staff_quick_create"),
    path('add_staff_save', HodViews.add_staff_save, name="add_staff_save"),
    path('admin/staff/<int:pk>/delete/', HodViews.StaffDeleteView.as_view(), name="delete_staff"),
    path('admin/staff/<int:pk>/view/', HodViews.StaffDetailView.as_view(), name="view_staff"),
    path('admin/customer/<int:pk>/view/', HodViews.CustomerDetailView.as_view(), name="view_customer"),
    path('admin/customer/<int:pk>/delete/', HodViews.CustomerDeleteView.as_view(), name="delete_customer"),
    path('admin/customer/create/', HodViews.add_customer, name="add_customer"),
    path('add_customer_save', HodViews.add_customer_save, name="add_customer_save"),
    path('quick_customer_save', HodViews.quick_customer_save, name="quick_customer_save"),
    path('customer_quick_create', HodViews.customer_quick_create, name="customer_quick_create"),
    path('admin/staff/view/', HodViews.manage_staff, name="manage_staff"),
    path('admin/customer/view/', HodViews.manage_customer, name="manage_customer"),
    path('admin/staff/edit/<int:staff_id>', HodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save, name="edit_staff_save"),
    path('admin/customer/<str:customer_id>/edit/', HodViews.edit_customer, name="edit_customer"),
    path('dashboard/edit_customer_save', HodViews.edit_customer_save, name="edit_customer_save"),
    path('admin/tenant/create/', HodViews.add_tenant, name="add_tenant"),
    path('add_tenant_save', HodViews.add_tenant_save, name="add_tenant_save"),
    path('admin/tenant_domain/create/', HodViews.add_tenant_domain, name="add_tenant_domain"),
    path('admin/edit/tenant/<str:tenant_id>', HodViews.edit_tenant, name="edit_tenant"),
    path('edit_tenant_save', HodViews.edit_tenant_save, name="edit_tenant_save"),
    path('add_domain_save', HodViews.add_domain_save, name="add_domain_save"),
    path('admin/domains/view/', HodViews.manage_domain, name="manage_domain"),
    path('admin/tenants/view', HodViews.manage_tenant, name="manage_tenant"),
    path('edit_domain_save', HodViews.edit_domain_save, name="edit_domain_save"),
    path('admin/edit/domain/<str:domain_id>', HodViews.edit_domain, name="edit_domain"),
    path('admin/addresses', HodViews.address_list, name="view_addresses"),
    path('admin/companyinfo', HodViews.CompanyDetailsView.as_view(), name="company_details"),
    path('admin/companyinfo/<str:company_id>/update', HodViews.update_company, name="update_company"),
    path('admin/companyinfo/address/<str:address_id>/update', HodViews.update_company_address, name="update_company_address"),
    path('update_company_save', HodViews.update_company_save, name="update_company_save"),
    path('update_company_address_save', HodViews.update_company_address_save, name="update_company_address_save"),
    #path('dashboard/manage_email_domains/', HodViews.GetEmails.as_view(), name="view_email_domains"),
    path('check_email_exist', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist', HodViews.check_username_exist,name="check_username_exist"),
    path('check_tenant_exist', HodViews.check_tenant_exist,name="check_tenant_exist"),
    path('check_slug_exist', HodViews.check_slug_exist,name="check_slug_exist"),
    path('admin/create/staff', HodViews.CreateStafView.as_view(),),
    path('admin/create/address', HodViews.CreateAddressView.as_view(),),

    #path('dns/', HodViews.get_dns, name="get_dns"),
    # staff urls path
    path('admin/staff', StaffViews.staff_dashboard, name="staff_dashboard"),

    # customer urls path
    #path('sidebar', )
    path('admin/home', CustomerViews.customer_dashboard, name="customer_dashboard"),
    path('customer_view_accounts/', CustomerViews.customer_view_accounts, name="customer_view_accounts"),
    path('customer_view_domain/', CustomerViews.customer_view_domain, name="customer_view_domain"),
    path('profile/', CustomerViews.profile, name="profile"),
    path('create_service', CustomerViews.create_tenant, name="create_tenant"),
    path('create_tenant_save', CustomerViews.create_tenant_save, name="create_tenant_save"),
    path('profile/', CustomerViews.profile, name="profile"),
    path('check_service_exist', CustomerViews.check_service_exist, name="check_service_exist"),


    # Department urls
    path('admin/departments/', HodViews.DepartmentListView.as_view(), name="view_departments"),

    path('department_create', HodViews.create_department_view, name="create_department_view"),
    path('quick_department_save', HodViews.quick_department_save, name="quick_department_save"),
    
    #  path('edit_tenant_save', HodViews.edit_tenant_save),

    # Alternatively, if you want CMS pages to be served from a subpath
    # of your site, rather than the site root:
    #    re_path(r"^pages/", include(codered_urls)),
]
