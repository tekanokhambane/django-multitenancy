from django.shortcuts import render
from django.views.generic import View
from account.mixins import LoginRequiredMixin
from multitenancy.admin.decorators import allowed_users
from .baseViews import (StaffCreateView, StaffListView, TeamListView, StaffUpdateView)
from helpdesk.models import Ticket


class StaffIndexView(View, LoginRequiredMixin):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        active_tickets = Ticket.objects.select_related('queue').exclude(
        status__in=[Ticket.CLOSED_STATUS, Ticket.RESOLVED_STATUS],
        )

        # open & reopened tickets, assigned to current user
        tickets = active_tickets.filter(
            assigned_to=request.user,
        )
        return render(request, 'multitenancy/admin/teamUser/index.html',
                      {
                          'nbar': 'admin',
                          'title': 'Dashboard!',
                        'user_tickets':tickets
                      }
                      )
