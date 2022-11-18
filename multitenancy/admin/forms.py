from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_countries.widgets import CountrySelectWidget
from multitenancy.apps.models import Tenant
from multitenancy.settings.models import Address, AdminSettings, GeneralInfo, Logo
from multitenancy.subscriptions.models import Plan

from multitenancy.users.models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class TenantForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = ['name', 'slug', 'type']


class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = ['name', 'description', 'price']


class LogoForm(forms.ModelForm):
    logo = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Logo
        fields = ['logo']
        widgets = {
            'logo': forms.FileField(),
        }


class GeneralInfoForm(forms.ModelForm):
    phone_number = PhoneNumberField()

    class Meta:
        model = GeneralInfo
        fields = ['company_name', 'phone_number', 'website', 'email']
        widgets = {
            'email': forms.EmailInput(),
        }


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'postal_code']
        widgets = {
            'country': CountrySelectWidget()
        }


class AdminSettingsForm(forms.ModelForm):

    class Meta:
        model = AdminSettings
        fields = ['timezone', 'language']
