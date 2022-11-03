import django
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginCheckMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.type == "Admin":
                if modulename == "multitenancy.core.adminViews":
                    pass
                else:
                    return HttpResponseRedirect(reverse("dashboard"))
            elif user.type == "Staff":
                if modulename == "multitenancy.core.teamViews":
                    pass
                else:
                    return HttpResponseRedirect(reverse("team_dashboard"))
            elif user.type == "Customer":
                if modulename == "multitenancy.core.CustomerViews":
                    pass
                else:
                    return HttpResponseRedirect(reverse("customer_dashboard"))
            else:
                return HttpResponseRedirect(reverse("account_login"))
        else:
            if request.path == reverse("account_login") or request.path == reverse("doLogin") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("account_login"))