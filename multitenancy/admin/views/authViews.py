from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.shortcuts import render
from django.contrib import  auth
import account.forms
from django.core.exceptions import ImproperlyConfigured
import account.views
from django.views.generic import View
from multitenancy.admin.forms import SignupForm

from multitenancy.profiles.models import Profile

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
                if self.request.user and not Profile.objects.filter(user=self.request.user).exists():
                    Profile.objects.create(user=self.request.user)
                return HttpResponseRedirect(reverse("admin_dashboard"))
            elif self.request.user.type == "Staff":  # type: ignore
                if self.request.user and not Profile.objects.filter(user=self.request.user).exists():
                    Profile.objects.create(user=self.request.user)
                return HttpResponseRedirect(reverse("team_dashboard"))
            else:
                return HttpResponseRedirect(reverse("customer_dashboard"))
        # return redirect(self.get_success_url())

class SignupView(account.views.SignupView):

   form_class = SignupForm

   def login_user(self):
        user = auth.authenticate(**self.user_credentials())
        if not user:
            raise ImproperlyConfigured("Configured auth backends failed to authenticate on signup")
        auth.login(self.request, user, backend='tenant_users.permissions.backend.UserBackend')
        self.request.session.set_expiry(0)

   