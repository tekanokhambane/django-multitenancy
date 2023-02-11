from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from rest_framework.reverse import reverse
from rest_framework import permissions
from account.mixins import LoginRequiredMixin
from multitenancy.admin.views.baseViews import(
    AdminDeleteView,
    AdminCreateView,
    AdminUpdateView,
    AdminTemplateView,
    )
from tenant_users.permissions.models import UserTenantPermissions
from .forms import CustomerForm, CustomerUpdateForm, StaffForm, StaffUpdateForm
from .serializers import UserSerializer
from .models import Customer, TenantUser, Staff


class CustomerListView(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/users/customer_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("q") 
        f = TenantUser.objects.filter(type="Customer").search(query=query)
        context['filter'] = f
        return context

class DeleteCustomerView(LoginRequiredMixin ,AdminDeleteView):
    model = Customer
    template_name = "multitenancy/users/delete_customer.html"
    success_url = reverse_lazy("customer_list", urlconf="multitenancy.urls")

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs['pk']

        user = Customer.objects.filter(id=customer_id)
        user.delete()
        return HttpResponseRedirect(reverse('customer_list', urlconf="multitenancyl.urls"))

class CreateCustomerView(LoginRequiredMixin ,AdminCreateView):
    model = TenantUser
    form_class = CustomerForm
    # success_url = '/admin/customers/'
    success_url = reverse_lazy('customer_list', urlconf="multitenancy.urls")
    template_name = 'multitenancy/users/create_customer.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'type': 'Customer'}
        return kwargs

class UpdateCustomerView(LoginRequiredMixin ,AdminUpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    success_url = reverse_lazy('customer_list', urlconf="multitenancy.urls")
    template_name = 'multitenancy/users/update_customer.html'


class StaffListView(LoginRequiredMixin ,AdminTemplateView):
    template_name = "multitenancy/users/staff_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("q") 
        f = TenantUser.objects.filter(type="Staff").search(query=query)
        context['filter'] = f
        return context
    

class CreateStaffView(LoginRequiredMixin ,AdminCreateView):
    model = TenantUser
    form_class = StaffForm
    # success_url = '/admin/customers/'
    success_url = reverse_lazy('staff_list', urlconf="multitenancy.urls")
    template_name = 'multitenancy/users/create_staff.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'type': 'Staff'})
        return render(request, self.template_name, {'form': form})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        user_permission = UserTenantPermissions.objects.create(profile_id=user.pk, is_staff=True, is_superuser=False)
        user_permission.save()
        return response

class UpdateStaffView(LoginRequiredMixin ,AdminUpdateView):
    model = Staff
    form_class = StaffUpdateForm
    success_url = reverse_lazy('staff_list', urlconf="multitenancy.urls")
    template_name = 'multitenancy/users/update_staff.html'


class DeleteStaffView(LoginRequiredMixin ,AdminDeleteView):
    model = Staff
    template_name = "multitenancy/users/delete_staff.html"
    success_url = reverse_lazy("staff_list", urlconf="multitenancy.urls")

    def delete(self, request, *args, **kwargs):
        staff_id = self.kwargs['pk']

        user = Staff.objects.filter(id=staff_id)
        user.delete()
        return HttpResponseRedirect(reverse('staff_list', urlconf="multitenancy.urls"))


class CustomerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    model = TenantUser
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q")
        id_query  = self.request.GET.get("id")
        queryset = TenantUser.objects.filter(type="Customer").exclude(email="AnonymousUser").search(query=query).filter_by_id(query=id_query).distinct()
        return queryset


class StaffViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    model = TenantUser
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.GET.get("q") 
        queryset = TenantUser.objects.filter(type="Staff").search(query=query)
        return queryset