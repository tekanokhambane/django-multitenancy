from django.shortcuts import render
from django.views.generic import View
from account.mixins import LoginRequiredMixin
from multitenancy.admin.decorators import allowed_users

class CustomerIndexView(View, LoginRequiredMixin):
    @allowed_users(allowed_types=["Customer"])
    def get(self, request, *args, **kwargs):
        return render(request, 'multitenancy/admin/publicUser/index.html',
                      {
                          'nbar': 'admin',
                          'title': 'Dashboard!',

                      }
                      )
