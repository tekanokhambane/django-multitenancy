import os
from django.conf import settings
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import View
from account.mixins import LoginRequiredMixin
from multitenancy.admin.decorators import allowed_users
from multitenancy.admin.filters import TenantFilter
from multitenancy.admin.views.baseViews import CustomerListView, CustomerTemplateView, CustomerView
from multitenancy.apps.models import Tenant, Domain
from account.models import Account
from helpdesk.models import Ticket

from multitenancy.subscriptions.models import Plan

class CustomerIndexView(LoginRequiredMixin, CustomerTemplateView):
    template_name = "multitenancy/admin/publicUser/index.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['subscriptions'] = Tenant.objects.filter(owner=self.request.user)
        context['domains'] = Domain.objects.filter(tenant__owner=self.request.user).filter(is_custom=True)
        context['account'] = Account.objects.get_or_create(user=self.request.user)
        context['tickets'] = Ticket.objects.filter(
            submitter_email=self.request.user.email, status=1)
        context['alltickets'] = Ticket.objects.filter(submitter_email=self.request.user.email)
        
        return context
    


class SubscriptionsListView(LoginRequiredMixin, CustomerTemplateView):
    template_name = "multitenancy/admin/publicUser/subscriptions.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        subscriptions = TenantFilter(queryset=Tenant.objects.filter(owner=self.request.user))
        context['filter'] = subscriptions
        return context
    

class CreateService(LoginRequiredMixin, CustomerView):
    def get(self,request):
        plans = Plan.objects.all()
        settings.STATICFILES_DIRS = [
            os.path.join(settings.PROJECT_DIR, 'templates/client/static/'),
        ]
        settings.TENANT_CREATION_TEMPLATE ="client/static/publicUser/index.html"
        return render(request,settings.TENANT_CREATION_TEMPLATE, {"plans":plans})