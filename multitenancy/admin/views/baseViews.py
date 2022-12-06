from django.views.generic import TemplateView, ListView, DeleteView, View, CreateView, UpdateView
from django.http import Http404
from django.utils.translation import gettext as _
from multitenancy.admin.decorators import allowed_users


class AdminCreateView(CreateView):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class AdminUpdateView(UpdateView):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class AdminDeleteView(DeleteView):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class AdminListView(ListView):
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

class AdminTemplateView(TemplateView):
    @allowed_users(allowed_types=["Admin"])
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class StaffCreateView(CreateView):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class StaffUpdateView(UpdateView):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class StaffDeleteView(DeleteView):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class StaffListView(ListView):
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

class StaffTemplateView(TemplateView):
    @allowed_users(allowed_types=["Staff"])
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TeamCreateView(CreateView):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class TeamUpdateView(UpdateView):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)


class TeamDeleteView(DeleteView):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TeamListView(ListView):
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

class TeamTemplateView(TemplateView):
    @allowed_users(allowed_types=["Admin", "Staff"])
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)