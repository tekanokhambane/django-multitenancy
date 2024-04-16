from django.urls import path, include
from rest_framework.routers import DefaultRouter
from multitenancy.subscriptions import views as subscriptions_views
from multitenancy.apps import views as tenant_views
from multitenancy.users import views as users_views
from multitenancy.billing import views as billing_views
from multitenancy.order import  views as orders_views

router = DefaultRouter()
router.register(r'users/customers', users_views.CustomerViewSet,basename="customers")
router.register(r'users/staff', users_views.StaffViewSet,basename="staff")
router.register(r'plans', subscriptions_views.PlanViewSet,basename="plans", )
router.register(r'subscriptions', subscriptions_views.SubscriptionsViewSet,basename="subscriptions")
router.register(r'product-types', subscriptions_views.ProductTypeViewSet,basename="product_type")
router.register(r'orders', orders_views.OdersViewSet,basename="orders")
router.register(r'coupons', orders_views.CouponViewSet,basename="coupons")
router.register(r'billing/invoices', billing_views.InvoiceViewSet,basename="invoices")
router.register(r'billing/payments', billing_views.PaymentViewSet,basename="payments")
router.register(r'billing/payment-gateways', billing_views.PaymentGateWayViewSet,basename="payment-gateways")
router.register(r'billing/refunds', billing_views.RefundViewSet,basename="refunds")
router.register(r'billing/credits', billing_views.CreditViewSet,basename="credits")
router.register(r'templates', tenant_views.TenantTemplateViewSet,basename="templates")

urlpatterns = [
    path('', include(router.urls)),
]