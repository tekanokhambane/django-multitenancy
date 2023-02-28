from django.urls import path

from . import views

urlpatterns = [
    path('billing/orders/',views.OrdersListView.as_view(), name="orders_list"),
    path('billing/orders/dashboard/', views.OrderIndexView.as_view(), name="orders_index" ),
]