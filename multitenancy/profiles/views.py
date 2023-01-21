from django.urls.base import reverse

from multitenancy.admin.views.baseViews import TeamUpdateView, TeamListView, TeamDetailView

from django.contrib import messages

from account.mixins import LoginRequiredMixin

from .forms import ProfileForm
from .models import Profile


class ProfileEditView(LoginRequiredMixin, TeamUpdateView):

    form_class = ProfileForm
    model = Profile

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("profiles_list")

    def form_valid(self, form):
        response = super(ProfileEditView, self).form_valid(form)
        messages.success(self.request, "You successfully updated your profile.")
        return response


class ProfileDetailView(LoginRequiredMixin, TeamDetailView):

    model = Profile
    slug_url_kwarg = "username"
    slug_field = "user__username"
    context_object_name = "profile"


class ProfileListView(LoginRequiredMixin, TeamListView):

    model = Profile
    context_object_name = "profiles"
