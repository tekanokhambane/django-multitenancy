from django.test import SimpleTestCase

from django.urls import reverse, resolve
from multitenancy.profiles.views import ProfileListView, ProfileDetailView, ProfileEditView

class TestUrls(SimpleTestCase):

    def test_list_resolved(self):
        url = reverse('profiles_list')
        self.assertEquals(resolve(url).func, ProfileListView)