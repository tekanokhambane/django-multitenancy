from django.urls import path, include
# from django.conf.urls import url
from .admin import team_urls
from .admin import customer_urls
from .admin import urls as admin_urls
from .profiles import urls as profile_urls
from .subscriptions import urls as subscription_urls
from .users import  urls as users_urls
from .apps import urls as apps_urls
from .apps import  customer_urls as customer_app_urls
from .settings import urls as settings_urls
from .billing import urls as billing_urls
from . import  api


urlpatterns = [
    path('admin/', include(admin_urls)),
    path('admin/', include(users_urls)),
    path('admin/', include(apps_urls)),
    path('admin/', include(subscription_urls)),
    path('admin/', include(billing_urls)),
    path('admin/', include(settings_urls)),
    path('dashboard/', include(customer_app_urls)),
    path('dashboard/', include(customer_urls)),
    path('admin/', include(team_urls)),
    path('admin/profiles/', include(profile_urls)),
    path('api/', include(api)),
]
