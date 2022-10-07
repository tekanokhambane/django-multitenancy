from django.urls import path, include, re_path
from django_multitenancy.admin.views import (
    adminViews
)
from .admin import urls as admin_urls
from .profiles import urls as profile_urls
urlpatterns =[
    path('admin/', include(admin_urls)),
    path('admin/profiles/', include(profile_urls)),

]