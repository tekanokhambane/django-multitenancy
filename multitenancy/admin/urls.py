from django.urls import path


from multitenancy.admin.views import adminViews, authViews

# app_name = "multitenancy"

urlpatterns = [
    path(r"", adminViews.AdminIndexView.as_view(), name="admin_dashboard"),
    path("teams/all", adminViews.TeamsIndexView.as_view(), name="teams_index"),
    path("acounts/login/", authViews.LoginView.as_view(), name="accounts_login"),
    path(r"^account/signup/$", authViews.SignupView.as_view(), name="account_signup"),
    path("page-not-found/", authViews.pageNotFound.as_view(), name="page_not_found"),
]
handler404 = "multitenancy.admin.views.authViews.pageNotFound"
