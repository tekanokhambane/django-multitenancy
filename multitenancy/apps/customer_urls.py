from django.urls import path
from multitenancy.apps import views

urlpatterns = [
    path("subscriptions/",views.CustomerTenantListView.as_view(), name="subscriptions"),
    path("subscriptions/create/",views.CreateService.as_view(), name="create_service"),
]