from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.shortcuts import redirect, render
from django.contrib import auth
from account.conf import settings
from account.utils import default_redirect
import account.forms
from django.core.exceptions import ImproperlyConfigured
import account.views
from django.views.generic import View
from multitenancy.admin.forms import SignupForm

from multitenancy.profiles.models import Profile


class pageNotFound(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "404.html",
            {
                "nbar": "admin",
                "title": "Dashboard!",
            },
        )


class LoginView(account.views.LoginView):

    form_class = account.forms.LoginEmailForm
    redirect_field_name = "next"

    def form_valid(self, form):
        self.login_user(form)
        self.after_login(form)
        return redirect(self.get_success_url())

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            if self.request.user.is_authenticated:
                if self.request.user.type == "Admin":  # type: ignore
                    fallback_url = reverse("admin_dashboard")
                elif self.request.user.type == "Staff":  # type: ignore
                    fallback_url = reverse("team_dashboard")
                else:
                    fallback_url = reverse("customer_dashboard")
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


class SignupView(account.views.SignupView):

    form_class = SignupForm

    def login_user(self):
        user = auth.authenticate(**self.user_credentials())
        if not user:
            raise ImproperlyConfigured(
                "Configured auth backends failed to authenticate on signup"
            )
        auth.login(
            self.request, user, backend="tenant_users.permissions.backend.UserBackend"
        )
        self.request.session.set_expiry(0)
