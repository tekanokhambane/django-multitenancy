from django.urls import path
from . import views
urlpatterns = [
    path('billing/',views.BillingIndexView.as_view(), name="billing"),
    path('billing/invoices/',views.InvoiceListView.as_view(), name="invoice_list"),
    path('billing/refunds/',views.RefundsListView.as_view(), name="refunds_list"),
    path('billing/credits/',views.CreditsListView.as_view(), name="credits_list"),
]