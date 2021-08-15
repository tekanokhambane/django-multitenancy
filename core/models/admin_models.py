from django.core.files import storage
from django.db.models.fields import related
from django.db import models
from django.db.models import manager
from django_countries.fields import CountryField
from modelcluster.fields import ParentalKey
from phonenumber_field.modelfields import PhoneNumberField
from django.core.files.storage import FileSystemStorage


class Department(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    objects = models.Manager()

    #department_head = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

        
class Address(models.Model):
    name = models.CharField(default="Company Name", max_length=255, blank=True, null=True)
    address_line_1 = models.CharField(default="12 Small Street", max_length=200, null=True, blank=True,)
    address_line_2 = models.CharField(default="Braamfontein", max_length=200, null=True, blank=True)
    city = models.CharField(default="Johannesburg", max_length=200, null=True, blank=True)
    state = models.CharField(default="Gauteng", max_length=200, null=True, blank=True, verbose_name="State/Province")
    country = CountryField()
    postal_code = models.CharField(max_length=64, null=True, blank=True, verbose_name="Post/Zip-code")
    
    def __str__(self):
        return "{}, {}, {}".format(self.name, self.city, self.country)


fs = FileSystemStorage(location='/media/')


class  CompanyDetails(models.Model):
    name = models.CharField(default="Organisation Name", max_length=200, blank=True, null=True, verbose_name="Company Name")
    logo = models.FileField(default="logo.jpg", null=True, blank=True)
    manager = models.ForeignKey("core.AdminUser", default=1, null=True, blank=True, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, default=1, on_delete=models.CASCADE, blank=True, null=True)
    departments = models.ManyToManyField(Department, blank=True)
    website = models.URLField(default="http://exmple.com", null=True, blank=True,)
    phone = PhoneNumberField(default="+27829999999", null=True, blank=True)
    email = models.EmailField(default="info@company.com", null=True, blank=True)
    

    def __str__(self):
        return self.name

