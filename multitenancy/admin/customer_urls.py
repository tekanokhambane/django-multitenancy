from django.urls import path
from multitenancy.admin.views import (
    customerViews
)

urlpatterns = [

    path("", customerViews.CustomerIndexView.as_view(), name="customer_dashboard"),


]
