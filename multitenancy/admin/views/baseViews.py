from django.views.generic import TemplateView, ListView, DeleteView, View, CreateView, UpdateView
from django.http import Http404
from django.utils.translation import gettext as _
from multitenancy.admin.decorators import allowed_users
from account.mixins import LoginRequiredMixin

class AdminCreateView(CreateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class AdminUpdateView(UpdateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class AdminDeleteView(DeleteView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AdminListView(ListView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

class AdminTemplateView(TemplateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class StaffCreateView(CreateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class StaffUpdateView(UpdateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class StaffDeleteView(DeleteView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class StaffListView(ListView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

class StaffTemplateView(TemplateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TeamCreateView(CreateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class TeamUpdateView(UpdateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class TeamDeleteView(DeleteView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TeamListView(ListView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

class TeamTemplateView(TemplateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    

class CustomerTemplateView(TemplateView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Customer"])
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CustomerListView(ListView, LoginRequiredMixin):
    @allowed_users(allowed_types=["Customer"])
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)