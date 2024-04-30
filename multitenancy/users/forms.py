import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.forms import SignupForm
from multitenancy.users.models import Customer, Staff, TenantUser


class CustomerForm(UserCreationForm):
    type = forms.CharField(label="Type", widget=forms.HiddenInput, initial="Customer")

    class Meta:
        model = TenantUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "type",
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomerUpdateForm(forms.ModelForm):

    class Meta:
        model = TenantUser
        fields = ["first_name", "last_name", "username", "email"]
        widgets = {
            "email": forms.EmailInput(),
        }


class StaffForm(UserCreationForm):
    type = forms.CharField(label="Type", widget=forms.HiddenInput, initial="Staff")

    class Meta:
        model = TenantUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "type",
        ]

    # validate email
    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if email and TenantUser.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email already exists")
    #     # create regex to validate email
    #     if email:
    #         if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
    #             raise forms.ValidationError("Invalid email address")
    #     return email


class StaffUpdateForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ["first_name", "last_name", "username", "email"]
        widgets = {
            "email": forms.EmailInput(),
        }


class UserInviteForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255, required=True)
