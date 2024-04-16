import os
from django.conf import settings

from account.mixins import LoginRequiredMixin
from multitenancy.admin.views.baseViews import CustomerTemplateView
from multitenancy.apps.models import Tenant, Domain
from account.models import Account
from helpdesk.models import Ticket



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
    


