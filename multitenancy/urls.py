from django.urls import path, include, re_path
from multitenancy.admin.views import (
    adminViews
)
from.admin import team_urls
from .admin import urls as admin_urls
from .profiles import urls as profile_urls
urlpatterns =[
    path('admin/', include(admin_urls)),
    path('dashboard/', include(team_urls)),
    path('admin/profiles/', include(profile_urls)),


]