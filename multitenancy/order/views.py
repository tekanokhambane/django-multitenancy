from django.shortcuts import render
from account.mixins import LoginRequiredMixin
from multitenancy.admin.views.baseViews import AdminTemplateView
from rest_framework import viewsets

from multitenancy.order.models import Order, Coupon
from multitenancy.order.serializers import CouponSerializer, OrdersSerializer


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


class OrdersListView(LoginRequiredMixin ,AdminTemplateView):

    template_name = 'multitenancy/order/orders_list.html'


class CouponListView(LoginRequiredMixin ,AdminTemplateView):

    template_name = 'multitenancy/order/coupon_list.html'
