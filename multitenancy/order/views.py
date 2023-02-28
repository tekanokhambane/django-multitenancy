from django.shortcuts import render
from account.mixins import LoginRequiredMixin
from multitenancy.admin.views.baseViews import AdminTemplateView


class OrderIndexView(AdminTemplateView):
    template_name = "multitenancy/order/order_index.html"


class OrdersListView(LoginRequiredMixin ,AdminTemplateView):

    template_name = 'multitenancy/order/orders_list.html'