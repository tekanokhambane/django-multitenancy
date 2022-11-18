from django.urls import path
from multitenancy.admin.views import (
    teamViews
)

urlpatterns = [

    path("staff/", teamViews.team_home, name="team_dashboard"),


]
