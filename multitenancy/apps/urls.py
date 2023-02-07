from django.urls import path, include
from multitenancy.apps import views

urlpatterns = [
    path("templates/", views.TemplateListView.as_view(), name="template_list"),
    path("templates/create/", views.CreateTemplateView.as_view(), name="create_template"),
    path("templates/<int:pk>/update/", views.UpdateTemplateView.as_view(), name="update_template"),
    path("templates/<int:pk>/delete/", views.DeleteTemplateView.as_view(), name="delete_tenant"),
    path("tenants/", views.TenantListView.as_view(), name="tenant_list"),
    
]