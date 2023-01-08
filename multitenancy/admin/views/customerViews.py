from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from account.mixins import LoginRequiredMixin
from multitenancy.admin.decorators import allowed_users
from multitenancy.admin.filters import TenantFilter
from multitenancy.admin.views.baseViews import CustomerListView
from multitenancy.apps.models import Tenant, Domain
from account.models import Account
from helpdesk.models import Ticket

class CustomerIndexView(View, LoginRequiredMixin):
    @allowed_users(allowed_types=["Customer"])
    def get(self, request, *args, **kwargs):
        subscriptions = Tenant.objects.filter(owner=self.request.user)
        domains = Domain.objects.filter(tenant__owner=request.user).filter(is_custom=True)
        account = Account.objects.get_or_create(user=request.user)
        tickets = Ticket.objects.filter(
            submitter_email=request.user.email, status=1)
        alltickets = Ticket.objects.filter(submitter_email=request.user.email)
        context = {'nbar': 'admin', "subscriptions": subscriptions, 'account': account, 'domains':domains,  'tickets': tickets, 'alltickets': alltickets}
        return render(request, 'multitenancy/admin/publicUser/index.html',context
                      )


class SubscriptionsListView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        subscriptions = TenantFilter(queryset=Tenant.objects.filter(owner=request.user))
        #print(settings.TENANT_DISPLAY_NAME_PLURAL)
        context = {"filter":subscriptions}
        return render(request, "multitenancy/admin/publicUser/subscriptions.html",context) 
    
    
class CreateService(View, LoginRequiredMixin):
    def get(self,request):
        return render(request,"multitenancy/admin/publicUser/create_service.html")