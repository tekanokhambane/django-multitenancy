from django.urls import path, include
# from django.conf.urls import url
from .admin import team_urls
from .admin import customer_urls
from .admin import urls as admin_urls
from .profiles import urls as profile_urls
from .subscriptions import urls as subscription_urls
urlpatterns = [
    path('admin/', include(admin_urls)),
    path('dashboard/', include(customer_urls)),
    path('admin/', include(team_urls)),
    path('admin/profiles/', include(profile_urls)),
    path('api/', include(subscription_urls)),
    # path(r'admin/support/', include('helpdesk.urls')),
]
