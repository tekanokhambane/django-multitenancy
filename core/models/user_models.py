from django.db import models
from ...users.models import TenantUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from ...customers.models import Client, Domain
import requests
from requests.auth import HTTPBasicAuth
import json
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
#from .user_models import DEPARTMENTS
from django.core.validators import RegexValidator


class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(TenantUser, on_delete=models.CASCADE)
    job_description = models.CharField(max_length=250, blank=True, null=True)
    address_line = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    suburb = models.CharField(_("Suburb"), max_length=55, blank=True, null=True)
    city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    province = models.CharField(_("Province"), max_length=255, blank=True, null=True)
    postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, null=True
    )
    #country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^(\+27|0)[6-8][0-9]{8}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=14, null=True, blank=True) # validators should be a list
    educational_qualification = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(TenantUser, on_delete=models.CASCADE)
    address_line = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    suburb = models.CharField(_("Suburb"), max_length=55, blank=True, null=True)
    city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    province = models.CharField(_("Province"), max_length=255, blank=True, null=True)
    postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, null=True
    )
    phone_regex = RegexValidator(regex=r'^(\+27|0)[6-8][0-9]{8}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True) # validators should be a list
    #country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    department = models.ForeignKey("core.Department",on_delete=models.CASCADE, max_length=250, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    educational_qualification = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(TenantUser, on_delete=models.CASCADE)
    address_line = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    suburb = models.CharField(_("Suburb"), max_length=55, blank=True, null=True)
    city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    province = models.CharField(_("Province"), max_length=255, blank=True, null=True)
    postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, null=True
    )
    phone_regex = RegexValidator(regex=r'^(\+27|0)[6-8][0-9]{8}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True) # validators should be a list
    #country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True)
    organisation = models.TextField(blank=True, null=True)
    objects = models.Manager()


@receiver(post_save, sender=TenantUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminUser.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance, address_line='', suburb='', city='', province='', postcode='', phone_number='', job_description='',
                                 department='', skills='', educational_qualification='')
        if instance.user_type == 3:
            Customers.objects.create(
                admin=instance, organisation='', address_line='', suburb='', city='', province='', postcode='', phone_number='',)


@receiver(post_save, sender=TenantUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminuser.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.customers.save()

