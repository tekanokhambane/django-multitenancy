import os
import uuid

from django.db import models
from django.utils import timezone

from django_multitenancy.users.models import TenantUser


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)


class Profile(models.Model):

    user = models.OneToOneField(TenantUser, related_name="profile", on_delete=models.PROTECT)  # type: ignore
    name = models.CharField(max_length=75, blank=True)
    job_title = models.CharField(max_length=75, blank=True)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    bio = models.TextField(blank=True)
    affiliation = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=250, blank=True)
    twitter_username = models.CharField("Twitter Username", max_length=100, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super(Profile, self).save(*args, **kwargs)

    @property
    def display_name(self):
        if self.name:
            return self.name
        else:
            return self.user.username
