from django.urls import path

from multitenancy.admin.views import (
    adminViews,
    authViews
)

#app_name = "multitenancy"

urlpatterns = [
    path(r"", adminViews.AdminIndexView.as_view(), name="admin_dashboard"),

    path("templates/", adminViews.TemplateListView.as_view(), name="template_list"),
    path("templates/create/", adminViews.CreateTemplateView.as_view(), name="create_template"),
    path("templates/<int:pk>/update/", adminViews.UpdateTemplateView.as_view(), name="update_template"),
    path("templates/<int:pk>/delete/", adminViews.DeleteTenantView.as_view(), name="delete_tenant"),
    path("subscriptions/", adminViews.SubscriptionList.as_view(), name="subscription_list"),
    path(route="customers/", view=adminViews.CustomerList.as_view(), name="customer_list", ),
    path("customers/create/", adminViews.CreateCustomerView.as_view(), name="create_customer"),
    path("customers/<int:pk>/update", adminViews.UpdateCustomerView.as_view(), name="update_customer"),
    path("customers/<int:pk>/delete", adminViews.DeleteCustomerView.as_view(), name="delete_customer"),
    path("teams/all", adminViews.TeamsIndexView.as_view(), name="teams_index"),
    path("settings/", adminViews.SettingsIndexView.as_view(), name="settings_index"),
    path("settings/plans/", adminViews.PlanListView.as_view(), name="plan_list"),
    path("settings/plans/<str:slug>/", adminViews.PlanDetailView.as_view(), name="plan_detail"),
    path("settings/plans/feature/create/", adminViews.FeatureCreateView.as_view(), name="create_feature"),
    path("settings/plans/create/", adminViews.CreatePlanView.as_view(), name="create_plan"),
    path("settings/plans/<int:pk>/update/", adminViews.UpdatePlanView.as_view(), name="update_plan"),
    path("settings/plans/<int:pk>/delete/", adminViews.DeletePlanView.as_view(), name="delete_plan"),
    path("settings/usersubscriptions/", adminViews.UserSubscriptionsListView.as_view(), name="usersubscription_list"),
    path("settings/producttypes/", adminViews.ProductTypeListView.as_view(), name="producttype_list"),
    path("settings/general/", adminViews.SettingsView.as_view(), name="generalsettings_index"),
    path("settings/general/logo/", adminViews.UpdateLogoView.as_view(), name="update_logo"),
    path("settings/general/info/", adminViews.GeneralInfoView.as_view(), name="update_info"),
    path("settings/general/address/", adminViews.AddressView.as_view(), name="update_address"),
    path("settings/general/adminsettings/", adminViews.AdminSettingsView.as_view(), name="update_adminsettings"),
    path("acounts/login/", authViews.LoginView.as_view(), name="accounts_login"),
    path("page-not-found/", authViews.pageNotFound.as_view(), name="page_not_found"),

]
handler404 = 'multitenancy.admin.views.authViews.pageNotFound'
