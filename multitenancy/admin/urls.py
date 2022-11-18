from django.urls import path

from multitenancy.admin.views import (
    adminViews,
    authViews
)

urlpatterns = [
    path("", adminViews.AdminIndexView.as_view(), name="dashboard"),

    path("templates/", adminViews.TemplateListView.as_view(), name="template_list"),
    path("templates/create/", adminViews.CreateTemplateView.as_view(), name="create_template"),
    path("templates/<int:pk>/update/", adminViews.UpdateTemplateView.as_view(), name="update_template"),
    path("templates/<int:pk>/delete/", adminViews.DeleteTenantView.as_view(), name="delete_tenant"),
    path("customers/", adminViews.CustomerList.as_view(), name="customer_list"),
    path("customers/create/", adminViews.CreateCustomerView.as_view(), name="create_customer"),
    path("customers/<int:pk>/update", adminViews.UpdateCustomerView.as_view(), name="update_customer"),
    path("customers/<int:pk>/delete", adminViews.DeleteCustomerView.as_view(), name="delete_customer"),
    path("teams/all", adminViews.TeamsIndexView.as_view(), name="teams_index"),
    path("settings/", adminViews.SettingsIndexView.as_view(), name="settings_index"),
    path("settings/plans/", adminViews.PlanListView.as_view(), name="plan_list"),
    path("settings/plans/create/", adminViews.CreatePlanView.as_view(), name="create_plan"),
    path("settings/plans/<int:pk>/update/", adminViews.CreatePlanView.as_view(), name="update_plan"),
    path("settings/plans/<int:pk>/delete/", adminViews.DeletePlanView.as_view(), name="delete_plan"),
    path("settings/usersubscriptions/", adminViews.UserSubcriptionsListView.as_view(), name="usersubscription_list"),
    path("settings/general/", adminViews.SettingsView.as_view(), name="generalsettings_index"),
    path("settings/general/<int:pk>/logo/", adminViews.UpdateLogoView.as_view(), name="update_logo"),
    path("settings/general/<int:pk>/info/", adminViews.GeneralInfoView.as_view(), name="update_info"),
    path("settings/general/<int:pk>/address/", adminViews.AddressView.as_view(), name="update_address"),
    path("settings/general/<int:pk>/adminsettings/", adminViews.AdminSettingsView.as_view(), name="update_adminsettings"),
    path("acounts/login/", authViews.LoginView.as_view(), name="accounts_login"),

]
