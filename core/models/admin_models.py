from django_tenants_portal.core.models.user_models import AdminUser, Staff
from django.db import models
from django.db.models import manager
from django_countries.fields import CountryField

class Department(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    #department_head = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)

class Address(models.Model):
    address_line_1 = models.CharField(max_length=200, null=True, blank=True,)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True, verbose_name="State/Province")
    country = CountryField()
    postal_code = models.CharField(max_length=64, null=True, blank=True, verbose_name="Post/Zip-code")

class  CompanyDetails(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Company Name")
    logo = models.ImageField()
    manager = models.ForeignKey(AdminUser, null=True, blank=True, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    departments = models.ManyToManyField(Department, blank=True)

