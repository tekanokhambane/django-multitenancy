from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        modulename=view_func.__module__
        if request.user.is_authenticated:
            if request.user.user_type == "1":
                return redirect("dashboard")
            elif request.user.user_type == "2":
                return redirect("staff_dashboard")
            elif request.user.user_type == "3":
                return redirect("customer_dashboard")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
