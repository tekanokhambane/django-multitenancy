from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from multitenancy.admin import urls as admin_urls

# from portal.HodViews import GetEmails
urlpatterns = (
    [
        path("django-admin/", admin.site.urls),
        path(r"", include("multitenancy.urls")),
        url(
            r"^admin/teams/",
            include("multitenancy.teams.urls", namespace="pinax_teams"),
        ),
        url(
            r"^admin/invitations/",
            include("multitenancy.invitations.urls", namespace="pinax_invitations"),
        ),
        path("select2/", include("django_select2.urls")),
        path("admin/support/", include("helpdesk.urls", namespace="helpdesk")),
        url(r"^admin/account/", include("account.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
