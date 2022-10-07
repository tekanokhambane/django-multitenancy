from django.urls import path

from django_multitenancy.admin.views import (
    adminViews
)

urlpatterns = [
    path("", adminViews.admin_home, name="dashboard"),
    path("teams", adminViews.TeamsIndexView.as_view(), name="teams_index"),

]
