from django.urls import path, include
from .admin import team_urls
from .admin import urls as admin_urls
from .profiles import urls as profile_urls
urlpatterns = [
    path('admin/', include(admin_urls)),
    path('dashboard/', include(team_urls)),
    path('profiles/', include(profile_urls)),
]
