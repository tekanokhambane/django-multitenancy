from django.urls import path
from multitenancy.admin.views import (
    customerViews
)

urlpatterns = [

    path("", customerViews.CustomerIndexView.as_view(), name="customer_dashboard"),
    path("subscriptions/",customerViews.SubscriptionsListView.as_view(), name="subscriptions"),
    path("subscriptions/create/",customerViews.CreateService.as_view(), name="create_service"),

]
