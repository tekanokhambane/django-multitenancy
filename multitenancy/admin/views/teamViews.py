from django.shortcuts import render
from django.views.generic import View
from account.mixins import LoginRequiredMixin
from multitenancy.admin.decorators import allowed_users
from .baseViews import (StaffCreateView, StaffListView, TeamListView, StaffUpdateView)


class StaffIndexView(View, LoginRequiredMixin):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        return render(request, 'multitenancy/admin/teamUser/index.html',
                      {
                          'nbar': 'admin',
                          'title': 'Dashboard!',

                      }
                      )
