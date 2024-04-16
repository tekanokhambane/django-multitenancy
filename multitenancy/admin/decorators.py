from django.shortcuts import redirect, render
import functools
from django.contrib import messages
from django.conf import settings


def allowed_users(allowed_types=[]):
    def decorator(view_func):
        def wrapper(self, *args, **kwargs):
            if self.request.user.is_authenticated:
                if self.request.user.type in allowed_types:
                    return view_func(self, *args, **kwargs)
                elif self.request.user.type == "Admin":
                    return render(self.request, '404.html')
                elif self.request.user.type == "Staff":
                    return render(self.request, '404.html')
                elif self.request.user.type == "Customer":
                    return render(self.request, '404.html')
            else:
                return redirect("accounts_login")
        return wrapper
    return decorator

# def allowed_users(allowed_types=[]):
#     def authenticated_user(view_func):
#         def wrapper_func(request, *args, **kwargs):
#             if request.user.is_authenticated:
#                 if request.user.type in allowed_types:
#                     return view_func(request, *args, **kwargs)
#                 if request.user.type == "Admin":
#                     return render(request, '404.html')
#                 elif request.user.type == "Staff":
#                     return render(request, '404.html')
#                 elif request.user.type == "Customer":
#                     return render(request, '404.html')
#             else:
#                 return redirect(settings.LOGIN_REDIRECT_URL)
#         return wrapper_func
#     return authenticated_user

def verification_required(view_func, verification_url="accounts:activate_email"):
    """
        this decorator restricts users who have not been verified
        from accessing the view function passed as it argument and
        redirect the user to page where their account can be activated
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_active:
            return view_func(request, *args, **kwargs)
        messages.info(request, "Email verification required")
        print("You need to be logged out")
        return redirect(verification_url)  
    return wrapper
