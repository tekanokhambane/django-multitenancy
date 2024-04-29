from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from account.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from multitenancy.admin.views.baseViews import AdminTemplateView, AdminCreateView
from rest_framework import viewsets

from multitenancy.order.models import Order, Coupon
from multitenancy.order.serializers import CouponSerializer, OrdersSerializer
from multitenancy.order.form import CouponForm


class OdersViewSet(viewsets.ModelViewSet):
    model = Order
    serializer_class = OrdersSerializer
    queryset = Order.objects.all()


class CouponViewSet(viewsets.ModelViewSet):
    model = Coupon
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()


class OrderIndexView(AdminTemplateView):
    template_name = "multitenancy/order/order_index.html"


class OrdersListView(LoginRequiredMixin, AdminTemplateView):

    template_name = "multitenancy/order/orders_list.html"


class CouponListView(LoginRequiredMixin, AdminTemplateView):

    template_name = "multitenancy/order/coupon_list.html"


class CreateCouponView(LoginRequiredMixin, AdminCreateView):
    model = Coupon
    form_class = CouponForm
    success_url = reverse_lazy("coupon_list", urlconf="multitenancy.urls")
    template_name = "multitenancy/order/create_coupon.html"

    # print logs
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        print(form.errors)
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print(form.errors)
        return super().form_invalid(form)
