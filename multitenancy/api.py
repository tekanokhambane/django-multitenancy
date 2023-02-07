from django.urls import path, include
from rest_framework.routers import DefaultRouter
from multitenancy.subscriptions import views as subscriptions_views
from multitenancy.apps import views as tenant_views
from multitenancy.users import views as users_views

router = DefaultRouter()
router.register(r'customers', users_views.CustomerViewSet,basename="customers")
router.register(r'staff', users_views.StaffViewSet,basename="staff")
router.register(r'plans', subscriptions_views.PlanViewSet,basename="plans")
router.register(r'subscriptions', subscriptions_views.SubscriptionsViewSet,basename="subscriptions")
router.register(r'tenants', tenant_views.TenantViewSet,basename="tenants")

urlpatterns = [
    path('', include(router.urls)),
]