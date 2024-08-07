from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import permissions
from account.mixins import LoginRequiredMixin
from multitenancy.admin.views.baseViews import AdminCreateView, AdminTemplateView
from multitenancy.billing.forms import InvoiceForm, RefundForm
from multitenancy.billing.serializers import (
    CreditSerializer,
    InvoiceSerializer,
    PaymentGatewaySerializer,
    PaymentSerializer,
    RefundSerializer,
)

from .models import Invoice, PaymentGateWay, Payment, Refund, Credit


class BillingIndexView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/billing/billing.html"


class InvoiceListView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/billing/invoice_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        form = InvoiceForm
        context["form"] = form
        return context


class CreditsListView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/billing/credits_list.html"


class RefundsListView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/billing/refunds_list.html"


class PaymentGatewaysView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/billing/payment_gateways_list.html"


class PaymentView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/billing/payments.html"


class RefundCreateView(LoginRequiredMixin, AdminCreateView):
    model = Refund
    template_name = "multitenancy/billing/refund_create.html"
    form_class = RefundForm


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    model = Invoice

    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q")
        query_id = self.request.GET.get("id")
        query_due_date = self.request.GET.get("due_date")
        query_start_date = self.request.GET.get("start_date")
        query_end_date = self.request.GET.get("end_date")
        query_status = self.request.GET.get("status")
        queryset = (
            Invoice.objects.filter()
            .search(query=query)
            .filter_by_id(id=query_id)
            .get_due_date(date=query_due_date)
            .filter_date_range(start_date=query_start_date, end_date=query_end_date)
            .get_status(status=query_status)
        )
        return queryset


class RefundViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    model = Refund
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

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
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = Credit.objects.filter().get_customer_credit(customer_id=query)
        return queryset


class PaymentGateWayViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    model = PaymentGateWay
    queryset = PaymentGateWay.objects.all()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class PaymentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
