from django.core.validators import RegexValidator
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
    company_name = models.CharField(max_length=255, blank=True, default="Django Multitenancy")
    phone_number = PhoneNumberField(blank=True, default="+27212345678")
    website = models.URLField(blank=True, default="https://example.com")
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = 'General Details'

class State(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Address(BaseSetting):
    help_text = 'Update Company Address'
    address_line_1 = models.CharField(max_length=200, blank=True, help_text='Enter the first line of the address')
    address_line_2 = models.CharField(max_length=200, blank=True,null=True, help_text='Enter the second line of the address')
    city = models.CharField(max_length=200, blank=True, help_text='Enter the city')
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True, verbose_name="State/Province")
    country = CountryField(blank=True, null=True,help_text='Select the country')
    postal_code = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Post/Zip-code",
        validators=[RegexValidator(
            regex=r'^\d{5}(?:[-\s]\d{4})?$',
            message="Invalid postal code"
        )],
        help_text='Enter the postal or zip code'
    )

    class Meta:
        verbose_name = 'Address'
        ordering = ['id']


class AdminSettings(BaseSetting):
    help_text = 'Update company timezone, currency and other related details.'
    timezone = TimeZoneField(_("timezone"))
    language = models.CharField(_("language"), max_length=10,
                                choices=settings.ACCOUNT_LANGUAGES, default=DEFAULT_LANGUAGE)

    class Meta:
        verbose_name = 'Time zone and currency'


class Currency(models.Model):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    
    code = models.CharField(max_length=3, unique=True, help_text="The currency code.")
    name = models.CharField(max_length=50, help_text="The name of the currency.")
    country = CountryField(help_text="The country of the currency.", null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, help_text="The exchange rate of the currency.", null=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the currency was created.",null=True)
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time the currency was last updated.")
    description = models.TextField(blank=True, null=True, help_text="Additional information about the currency.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE, help_text="Indicates if the currency is active or not.")

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self) -> str:
        """
        Returns the currency code and name as a string.
        """
        return f'{self.code} - {self.name}'


# class Currency(BaseSetting):
#     code = models.CharField(max_length=3)
#     name = models.CharField(max_length=50)
#     symbol = models.CharField(max_length=10)
#     default = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.default:
#             Currency.objects.filter(default=True).update(default=False)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.code
