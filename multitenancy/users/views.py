from django.conf import settings
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, JsonResponse
from django.urls.base import reverse, reverse_lazy
from rest_framework.reverse import reverse
from rest_framework import permissions
from django.core.mail import send_mail
from account.mixins import LoginRequiredMixin
from multitenancy.admin.views.baseViews import (
    AdminDeleteView,
    AdminCreateView,
    AdminUpdateView,
    AdminTemplateView,
    AdminView,
)
from tenant_users.permissions.models import UserTenantPermissions
from .forms import (
    CustomerForm,
    CustomerUpdateForm,
    StaffForm,
    StaffUpdateForm,
    UserInviteForm,
)
from .serializers import UserSerializer
from .models import Customer, TenantUser, Staff


class CustomerListView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/users/customer_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("q")
        f = TenantUser.objects.filter(type="Customer").search(query=query)
        context["filter"] = f
        return context


class DeleteCustomerView(LoginRequiredMixin, AdminDeleteView):
    model = Customer
    template_name = "multitenancy/users/delete_customer.html"
    success_url = reverse_lazy("customer_list", urlconf="multitenancy.urls")

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs["pk"]

        user = Customer.objects.filter(id=customer_id)
        user.delete()
        return HttpResponseRedirect(
            reverse("customer_list", urlconf="multitenancy.urls")
        )


class CreateCustomerView(LoginRequiredMixin, AdminCreateView):
    model = TenantUser
    form_class = CustomerForm
    # success_url = '/admin/customers/'
    success_url = reverse_lazy("customer_list", urlconf="multitenancy.urls")
    template_name = "multitenancy/users/create_customer.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = {"type": "Customer"}
        return kwargs


class UpdateCustomerView(LoginRequiredMixin, AdminUpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    success_url = reverse_lazy("customer_list", urlconf="multitenancy.urls")
    template_name = "multitenancy/users/update_customer.html"


class StaffListView(LoginRequiredMixin, AdminTemplateView):
    template_name = "multitenancy/users/staff_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        form = UserInviteForm()
        context["form"] = form
        query = self.request.GET.get("q")
        f = TenantUser.objects.filter(type="Staff").search(query=query)
        context["filter"] = f
        return context


class InviteUserView(LoginRequiredMixin, AdminView):

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        if TenantUser.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "User already exists"})
        try:
            subject = "Invitation to join staff"

            invite_link = request.scheme + "://" + request.get_host()
            # use a template to write the message
            message = (
                f"Click here to join staff:  {invite_link}/admin/join-staff/{email}/"
            )
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, [email])
            return JsonResponse({"success": True, "message": "Invitation sent"})
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "message": str(e)})


class UpdateStaffView(LoginRequiredMixin, AdminUpdateView):
    model = Staff
    form_class = StaffUpdateForm
    success_url = reverse_lazy("staff_list", urlconf="multitenancy.urls")
    template_name = "multitenancy/users/update_staff.html"


class DeleteStaffView(LoginRequiredMixin, AdminDeleteView):
    model = Staff
    template_name = "multitenancy/users/delete_staff.html"
    success_url = reverse_lazy("staff_list", urlconf="multitenancy.urls")

    def delete(self, request, *args, **kwargs):
        staff_id = self.kwargs["pk"]

        user = Staff.objects.filter(id=staff_id)
        user.delete()
        return HttpResponseRedirect(reverse("staff_list", urlconf="multitenancy.urls"))


class CustomerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    model = TenantUser

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q")
        id_query = self.request.GET.get("id")
        queryset = (
            TenantUser.objects.filter(type="Customer")
            .exclude(email="AnonymousUser")
            .search(query=query)
            .filter_by_id(query=id_query)
            .distinct()
        )
        return queryset


class StaffViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    model = TenantUser

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = TenantUser.objects.filter(type="Staff").search(query=query)
        return queryset
