from django.views.generic import TemplateView, ListView, DeleteView, View, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from multitenancy.admin.decorators import allowed_users




class AdminView(UserPassesTestMixin, View):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404

class AdminCreateView(UserPassesTestMixin, CreateView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404

class AdminDetailView(UserPassesTestMixin, DetailView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404

    


class AdminUpdateView(UserPassesTestMixin, UpdateView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404
    
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)



class AdminDeleteView(UserPassesTestMixin, DeleteView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AdminListView(UserPassesTestMixin, ListView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404
    


class AdminTemplateView(UserPassesTestMixin, TemplateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404

class StaffCreateView(UserPassesTestMixin, CreateView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        raise Http404


class StaffUpdateView(UserPassesTestMixin, UpdateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        raise Http404


class StaffDeleteView(UserPassesTestMixin, DeleteView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        raise Http404


class StaffListView(UserPassesTestMixin, ListView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        raise Http404

class StaffTemplateView(UserPassesTestMixin, TemplateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        raise Http404


class TeamDetailView(UserPassesTestMixin, DetailView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404


class TeamCreateView(UserPassesTestMixin, CreateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404


class TeamUpdateView(UserPassesTestMixin, UpdateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404


class TeamDeleteView(UserPassesTestMixin, DeleteView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404


class TeamListView(UserPassesTestMixin, ListView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404

class TeamTemplateView(UserPassesTestMixin, TemplateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        raise Http404
    

class CustomerView(UserPassesTestMixin, View):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Customer'
    
    def handle_no_permission(self):
        raise Http404

class CustomerTemplateView(UserPassesTestMixin, TemplateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Customer'
    
    def handle_no_permission(self):
        raise Http404
    
class CustomerListView(UserPassesTestMixin, ListView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Customer'
    
    def handle_no_permission(self):
        raise Http404

class CustomerDetailView(UserPassesTestMixin, DetailView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Customer'
    
    def handle_no_permission(self):
        raise Http404
