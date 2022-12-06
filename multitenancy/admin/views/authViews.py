from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.shortcuts import render
import account.forms
import account.views
from django.views.generic import View

class pageNotFound(View):
    def get(self, request, *args, **kwargs):
        return render(request, '404.html',
                      {
                          'nbar': 'admin',
                          'title': 'Dashboard!',

                      }
                      )


class LoginView(account.views.LoginView):

    form_class = account.forms.LoginEmailForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.type == "Admin":  # type: ignore
                return HttpResponseRedirect(reverse("admin_dashboard"))
            elif self.request.user.type == "Staff":  # type: ignore
                return HttpResponseRedirect(reverse("team_dashboard"))
            else:
                return HttpResponseRedirect(reverse("customer_dashboard"))
            # return redirect(self.get_success_url())
        return super(LoginView, self).get(*args, **kwargs)

    def form_valid(self, form):
        self.login_user(form)
        self.after_login(form)
        if self.request.user.is_authenticated:
            if self.request.user.type == "Admin":  # type: ignore
                return HttpResponseRedirect(reverse("admin_dashboard"))
            elif self.request.user.type == "Staff":  # type: ignore
                return HttpResponseRedirect(reverse("team_dashboard"))
            else:
                return HttpResponseRedirect(reverse("customer_dashboard"))
        # return redirect(self.get_success_url())
