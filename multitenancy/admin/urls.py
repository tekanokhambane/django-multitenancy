from django.urls import path

from multitenancy.admin.views import (
    adminViews,
    teamViews,
    authViews
)

urlpatterns = [
    path("", adminViews.admin_home, name="dashboard"),

    path("tenants/", adminViews.tenant_list, name="tenant_list"),
    path("customers/", adminViews.customer_list, name="customer_list"),
    path("teams?", adminViews.TeamsIndexView.as_view(), name="teams_index"),
    path("acounts/login/", authViews.LoginView.as_view(), name="accounts_login"),

]
