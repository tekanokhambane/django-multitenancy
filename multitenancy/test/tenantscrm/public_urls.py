
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from multitenancy.admin import urls as admin_urls
#from portal.HodViews import GetEmails
urlpatterns = [
   
   # Admin
   #   path(r'^cart/', include('cart.urls', namespace='cart')),
   #url(r'^payfast/', include('django_tenants_portal.billing.urls')),
   path('django-admin/', admin.site.urls),
   path(r'', include("multitenancy.urls")),
   url(r"^admin/teams/", include("pinax.teams.urls", namespace="pinax_teams")),
   url(r"^admin/invitations/", include("pinax.invitations.urls", namespace="pinax_invitations")),
   
   path("select2/", include("django_select2.urls")),
   path('admin/support/', include('helpdesk.urls', namespace='helpdesk')),
   #url(r'', include(accounts_urls)),
   #url(r'', include(customers_urls)),
   #path('accounts/', include('allauth.urls')),
   url(r"^admin/account/", include("account.urls")),
   url(r'^admin/settings/groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

