import django
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginCheckMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "django_tenants_portal.core.HodViews":
                    pass
                elif modulename == "django_tenants_portal.core.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type == "2":
                if modulename == "django_tenants_portal.core.StaffViews":
                    pass
                elif modulename == "django_tenants_portal.core.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_dashboard"))
            elif user.user_type == "3":
                if modulename == "django_tenants_portal.core.CustomerViews":
                    pass
                elif modulename == "django_tenants_portal.core.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("customer_dashboard"))
            else:
                return HttpResponseRedirect(reverse("show_login"))
        else:
            if request.path == reverse("show_login") or request.path == reverse("doLogin") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))