from django.db import models
from django.conf import settings
from account.languages import DEFAULT_LANGUAGE
from account.fields import TimeZoneField
from django.utils.translation import gettext_lazy as _
from multitenancy.core.models import BaseSetting
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class SettingsPage:
    def __init__(self, hook_name) -> None:
        pass
    settings_items = []


class Logo(BaseSetting):
    logo = models.ImageField(default="core/logo.png")
    name = 'slug'
    help_text = _('Upload Company Logo')

    class Meta:
        verbose_name = 'Logo'


class GeneralInfo(BaseSetting):
    help_text = 'Update the name, phone number, etc of the company'
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    website = models.URLField(null=True, blank=True,)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = 'General Details'


class Address(BaseSetting):
    help_text = 'Update Company Address'
    address_line_1 = models.CharField(max_length=200, null=True, blank=True,)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True, verbose_name="State/Province")
    country = CountryField(null=True, blank=True)
    postal_code = models.CharField(max_length=64, null=True, blank=True, verbose_name="Post/Zip-code")

    class Meta:
        verbose_name = 'Address'


class AdminSettings(BaseSetting):
    help_text = 'Update company timezone, currency and other related details.'
    timezone = TimeZoneField(_("timezone"))
    language = models.CharField(_("language"), max_length=10,
                                choices=settings.ACCOUNT_LANGUAGES, default=DEFAULT_LANGUAGE)

    class Meta:
        verbose_name = 'Time zone and currency'
