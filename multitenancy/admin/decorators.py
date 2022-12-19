from django.shortcuts import redirect, render


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
