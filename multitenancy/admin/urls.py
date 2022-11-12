from django.urls import path

from multitenancy.admin.views import (
    adminViews,
    teamViews,
    authViews
)

urlpatterns = [
    path("", adminViews.AdminIndexView.as_view(), name="dashboard"),

    path("tenants/", adminViews.TenantList.as_view(), name="tenant_list"),
    path("tenants/create/", adminViews.CreateTenantView.as_view(), name="create_tenant"),
    path("tenants/<int:pk>/delete/", adminViews.DeleteTenantView.as_view(), name="delete_tenant"),
    path("tenants/tenanttypes/", adminViews.TenantTypes.as_view(), name="tenant_types"),
    path("tenants/tenanttypes/create/", adminViews.CreateType.as_view(), name="create_tenant_type"),
    path("customers/", adminViews.CustomerList.as_view(), name="customer_list"),
    path("customers/create/", adminViews.CreateCustomerView.as_view(), name="create_customer"),
    path("customers/<int:pk>/update", adminViews.UpdateCustomerView.as_view(), name="update_customer"),
    path("customers/<int:pk>/delete", adminViews.DeleteCustomerView.as_view(), name="delete_customer"),
    path("teams/all", adminViews.TeamsIndexView.as_view(), name="teams_index"),
    path("settings/", adminViews.SettingsIndexView.as_view(), name="settings_index"),
    path("settings/packages/", adminViews.PackageListView.as_view(), name="package_list"),
    path("settings/packages/create", adminViews.CreatePackageView.as_view(), name="create_package"),
    path("acounts/login/", authViews.LoginView.as_view(), name="accounts_login"),

]
