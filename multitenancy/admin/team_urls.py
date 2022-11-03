from django.urls import path

from multitenancy.admin.views import (
    adminViews,
    teamViews,
    authViews
)

urlpatterns = [
   
    path("staff/", teamViews.team_home, name="team_dashboard"),
   

]
