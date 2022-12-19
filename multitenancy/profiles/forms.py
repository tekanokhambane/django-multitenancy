import re

from django import forms

from .models import Profile
from django_select2 import forms as s2forms


class SkillsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "name",
            "job_title",
            
            "bio",
            "skills",
            "display_profile",
            "education",
            "location",
            "website",
            "twitter_username",
        ]
        widgets = {
            'skills': SkillsWidget,

        }

    def clean_twitter_username(self):
        value = self.cleaned_data["twitter_username"]
        value = value.strip()
        if not value:
            return value
        if value.startswith("@"):
            value = value[1:]
        m = re.match(r"^[a-zA-Z0-9_]{1,20}$", value)
        if not m:
            raise forms.ValidationError("invalid Twitter username")
        return value
