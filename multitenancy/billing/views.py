from django.shortcuts import render

from multitenancy.admin.views.baseViews import AdminTemplateView


class BillingIndexView(AdminTemplateView):
    template_name = "multitenancy/billing/billing.html"