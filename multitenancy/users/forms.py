from django import forms
from django.contrib.auth.forms import UserCreationForm
from multitenancy.users.models import Customer, Staff, TenantUser

class CustomerForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = TenantUser
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
        }
    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CustomerUpdateForm(forms.ModelForm):
    
    class Meta:
        model = TenantUser
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'email': forms.EmailInput(),
        }


class StaffForm(forms.ModelForm):
    type = forms.CharField(label='Type', widget=forms.HiddenInput)
    class Meta:
        model = TenantUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password',  'type']
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class StaffUpdateForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'email': forms.EmailInput(),
        }