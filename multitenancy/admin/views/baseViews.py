from django.views.generic import TemplateView, ListView, DeleteView, View, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.template.loader import get_template
from django.http import Http404, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from multitenancy.admin.decorators import allowed_users





class AdminView(UserPassesTestMixin, View):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

class AdminCreateView(UserPassesTestMixin, CreateView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

class AdminDetailView(UserPassesTestMixin, DetailView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

    


class AdminUpdateView(UserPassesTestMixin, UpdateView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)
    
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)



class AdminDeleteView(UserPassesTestMixin, DeleteView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AdminListView(UserPassesTestMixin, ListView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)
    


class AdminTemplateView(UserPassesTestMixin, TemplateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

class StaffCreateView(UserPassesTestMixin, CreateView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)


class StaffUpdateView(UserPassesTestMixin, UpdateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)


class StaffDeleteView(UserPassesTestMixin, DeleteView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)


class StaffListView(UserPassesTestMixin, ListView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

class StaffTemplateView(UserPassesTestMixin, TemplateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)


class TeamDetailView(UserPassesTestMixin, DetailView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)


class TeamCreateView(UserPassesTestMixin, CreateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)


class TeamUpdateView(UserPassesTestMixin, UpdateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)


class TeamDeleteView(UserPassesTestMixin, DeleteView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)


class TeamListView(UserPassesTestMixin, ListView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

class TeamTemplateView(UserPassesTestMixin, TemplateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Staff' or self.request.user.type == 'Admin'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)
    

class CustomerView(UserPassesTestMixin, View):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Customer'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

class CustomerTemplateView(UserPassesTestMixin, TemplateView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Customer'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)
    
class CustomerListView(UserPassesTestMixin, ListView):
    redirect_field_name = 'next'
    def test_func(self):
        return  self.request.user.type == 'Customer'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)

class CustomerDetailView(UserPassesTestMixin, DetailView):
    redirect_field_name = 'next'
    def test_func(self):
        return self.request.user.type == 'Customer'
    
    def handle_no_permission(self):
        template = get_template('404.html')
        html = template.render()
        return HttpResponseNotFound(html)
