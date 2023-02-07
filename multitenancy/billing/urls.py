from django.urls import path
from . import views
urlpatterns = [
    path('billing/',views.BillingIndexView.as_view(), name="billing"),
]