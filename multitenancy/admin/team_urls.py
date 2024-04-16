from django.urls import path
from multitenancy.admin.views import (
    teamViews
)

urlpatterns = [

    path("home/", teamViews.StaffIndexView.as_view(), name="team_dashboard"),


]
