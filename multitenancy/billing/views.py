from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import permissions
from multitenancy.admin.views.baseViews import AdminTemplateView
from multitenancy.billing.forms import InvoiceForm
from multitenancy.billing.serializers import CreditSerializer, InvoiceSerializer, RefundSerializer

from .models import (
    Invoice,
    PaymentGateWay, 
    Payment, 
    Refund,
    Credit
    )

class BillingIndexView(AdminTemplateView):
    template_name = "multitenancy/billing/billing.html"

class InvoiceListView(AdminTemplateView):
    template_name = "multitenancy/billing/invoice_list.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        form = InvoiceForm
        context['form'] = form
        return context


class CreditsListView(AdminTemplateView):
    template_name = "multitenancy/billing/credits_list.html"

class RefundsListView(AdminTemplateView):
    template_name = "multitenancy/billing/refunds_list.html"

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    model = Invoice
    
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q") 
        query_id = self.request.GET.get("id")
        query_due_date = self.request.GET.get("due_date")
        query_start_date = self.request.GET.get("start_date")
        query_end_date = self.request.GET.get("end_date")
        query_status = self.request.GET.get("status")
        queryset = Invoice.objects.filter().search(query=query).filter_by_id(id=query_id).get_due_date(date=query_due_date).filter_date_range(start_date=query_start_date, end_date=query_end_date).get_status(status=query_status)
        return queryset


class RefundViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    model = Refund
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q") 
        queryset = Refund.objects.filter().get_invoice(invoice_id=query)
        return queryset
    
class CreditViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    model = Credit
    
    serializer_class = CreditSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q") 
        queryset = Credit.objects.filter().get_customer_credit(customer_id=query)
        return queryset

