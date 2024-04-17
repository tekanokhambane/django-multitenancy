from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_countries.widgets import CountrySelectWidget

from multitenancy.settings.models import Address, AdminSettings, GeneralInfo, Logo


class LogoForm(forms.ModelForm):
    logo = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "multiple": False}),
    )

    class Meta:
        model = Logo
        fields = ["logo"]
        widgets = {
            "logo": forms.FileField(),
        }


class GeneralInfoForm(forms.ModelForm):
    phone_number = PhoneNumberField()

    class Meta:
        model = GeneralInfo
        fields = ["company_name", "phone_number", "website", "email"]
        widgets = {
            "email": forms.EmailInput(),
        }


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "country",
            "postal_code",
        ]
        widgets = {"country": CountrySelectWidget()}


class AdminSettingsForm(forms.ModelForm):

    class Meta:
        model = AdminSettings
        fields = ["timezone", "language"]
