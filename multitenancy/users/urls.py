from django.urls import path
from . import views

urlpatterns = [
    path("customers/create/", views.CreateCustomerView.as_view(), name="create_customer"),
    path("customers/<int:pk>/update", views.UpdateCustomerView.as_view(), name="update_customer"),
    path(route="customers/", view=views.CustomerListView.as_view(), name="customer_list", ),
    path("customers/<int:pk>/delete", views.DeleteCustomerView.as_view(), name="delete_customer"),
    path(route="staff/", view=views.StaffListView.as_view(), name="staff_list", ),
    path("staff/<int:pk>/delete", views.DeleteStaffView.as_view(), name="delete_staff"),
    path("staff/create/", views.CreateStaffView.as_view(), name="create_staff"),



]