
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
   path('django-admin/', admin.site.urls),
   path(r'', include("multitenancy.urls")),
   url(r"^admin/teams/", include("pinax.teams.urls", namespace="pinax_teams")),
   url(r"^admin/invitations/", include("pinax.invitations.urls", namespace="pinax_invitations")),
   path("select2/", include("django_select2.urls")),
   path('admin/support/', include('helpdesk.urls', namespace='helpdesk')),
   url(r"^admin/account/", include("account.urls")),
   url(r'^admin/settings/groups-manager/', include('groups_manager.urls', namespace='groups_manager')),
    
]
if settings.DEBUG:
   from django.conf.urls.static import static
   from django.contrib.staticfiles.urls import staticfiles_urlpatterns
   urlpatterns += staticfiles_urlpatterns()
   urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

