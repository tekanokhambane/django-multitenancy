from django.urls import path
from .views import ProfileDetailView, ProfileEditView, ProfileListView


urlpatterns = [
    path(r"^profile/edit/", ProfileEditView.as_view(), name="profiles_edit"),
    path(r"^u/$", ProfileListView.as_view(), name="profiles_list"),
    path(
        r"^u/(?P<username>[\w\._-]+)/$",
        ProfileDetailView.as_view(),
        name="profiles_detail",
    ),
]
