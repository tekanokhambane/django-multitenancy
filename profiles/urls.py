from django.conf.urls import include, url
from .views import ProfileDetailView, ProfileEditView, ProfileListView


urlpatterns = [
   
    url(r"^profile/edit/", ProfileEditView.as_view(), name="profiles_edit"),
    url(r"^u/$", ProfileListView.as_view(), name="profiles_list"),
    url(r"^u/(?P<username>[\w\._-]+)/$", ProfileDetailView.as_view(), name="profiles_detail"),
  #

 #   url(r"", include("pinax.wiki.urls"))
]