from django.shortcuts import render
from django.views.generic import View
from account.mixins import LoginRequiredMixin
from multitenancy.admin.decorators import allowed_users
from multitenancy.apps.models import Tenant, Domain
from account.models import Account
from helpdesk.models import Ticket

class CustomerIndexView(View, LoginRequiredMixin):
    @allowed_users(allowed_types=["Customer"])
    def get(self, request, *args, **kwargs):
        tenants = Tenant.objects.filter(owner=request.user)
        #invoices = PayfastOrder.objects.filter(user=request.user)
        domains = Domain.objects.filter(tenant__owner=request.user).filter(has_custom=True)
        account = Account.objects.get_or_create(user=request.user)
        #domains = RegisteredDomain.objects.filter(owner=request.user)
        tickets = Ticket.objects.filter(
            submitter_email=request.user.email, status=1)
        alltickets = Ticket.objects.filter(submitter_email=request.user.email)

        return render(request, 'multitenancy/admin/publicUser/index.html',
                      {'nbar': 'admin', "tenants": tenants, 'account': account, 'domains':domains,  'tickets': tickets, 'alltickets': alltickets}
                      )
