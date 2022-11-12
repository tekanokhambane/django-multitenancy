from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.type == "Admin":  # type: ignore
                return redirect("dashboard")
            elif self.request.user.type == "Staff":  # type: ignore
                return redirect("team_dashboard")
            else:
                return redirect("customer_dashboard")
        return view_func(request, *args, **kwargs)
    
    return wrapper_func