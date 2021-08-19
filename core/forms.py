from django.core.files.storage import FileSystemStorage
from django.forms.models import inlineformset_factory
from django_tenants_portal.core.models.admin_models import Address, CompanyDetails, Department
from django.conf import settings
from django.http import request
from ..users.models import TenantUser
from django import forms
from django.utils.translation import templatize, ugettext_lazy as _
from ..customers.models import Client
from .models import Staff, Customers
#from phonenumber_field.formfields import PhoneNumberField
#from phonenumber_field.widgets import PhoneNumber, PhoneNumberInternationalFallbackWidget
from django.utils.text import slugify
from .utils import COUNTRIES
from modelcluster.forms import ClusterForm
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField


department = Department.objects.all()


class CompanyAddressForm(forms.Form):

    address_line_1 = forms.CharField(
        max_length=250, label="Address Line 1", widget=forms.TextInput(attrs={"class": "form-control"}))
    address_line_2 = forms.CharField(
        max_length=250, label="Address Line 2", widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(
        max_length=250, label="City", widget=forms.TextInput(attrs={"class": "form-control"}))
    state = forms.CharField(
        max_length=250, label="State", widget=forms.TextInput(attrs={"class": "form-control"}))
    country =  forms.ChoiceField(choices=COUNTRIES, widget=forms.Select(attrs={"class": "form-control"}))
    class Meta:
        model = Address
     


class CompanyDetailForm(forms.Form):
    name = forms.CharField(required=False, label="Company Name", max_length=250,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    logo = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={"class": "form-control"}))

    class Meta:
        model = CompanyDetails
        exclude = ['address', 'manager', 'departments']
        #fields = ["website", "phone", "email"]


class AddCustomerForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    phone_number = forms.RegexField(label="Cellphone", regex=r'^(\+27|0)[6-8][0-9]{8}$', error_messages={
                                    'required': "Cellphone must be 10 or 14 digits"}, widget=forms.TextInput(attrs={"class": "form-control"}))
    #country = forms.ChoiceField(label="Country", choices=COUNTRIES, widget=forms.Select(attrs={"class":"form-control"}))
    organisation = forms.CharField(
        label="Organisation", max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))


class QuickAddCustomerForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    phone_number = forms.RegexField(label="Cellphone", regex=r'^(\+27|0)[6-8][0-9]{8}$', error_messages={
                                    'required': "Cellphone must be 10 or 14 digits"}, widget=forms.TextInput(attrs={"class": "form-control"}))
    #country = forms.ChoiceField(label="Country", choices=COUNTRIES, widget=forms.Select(attrs={"class":"form-control"}))
    organisation = forms.CharField(
        label="Organisation", max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))


class AddStaffForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    job_description = forms.CharField(
        label="Job Description", max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    departments = Department.objects.all()
    department_list = []
    for department in departments:
        small_department = (department.id, department.name)
        department_list.append(small_department)
    department = forms.ChoiceField(
        choices=department_list, widget=forms.Select(attrs={"class": "form-control"}))
    #address = inlineformset_factory()
    #skills = forms.CharField(label="Skills", max_length=250, widget=forms.TextInput(attrs={"class":"form-control"}))
    #educational_qualification = forms.CharField(label="Educational Qualifications", max_length=250, widget=forms.TextInput(attrs={"class":"form-control"}))
    #address_line = forms.CharField(label="address_line", max_length=250, widget=forms.TextInput(attrs={"class":"form-control"}))
    #suburb = forms.CharField(label="Suburb", max_length=250, widget=forms.TextInput(attrs={"class":"form-control"}))
    #city = forms.CharField(label="City", max_length=250, widget=forms.TextInput(attrs={"class":"form-control"}))
    #province = forms.CharField(label="State/Province", max_length=250, widget=forms.TextInput(attrs={"class":"form-control"}))
    #postcode = forms.CharField(label="Postal/Zip-code", max_length=250, widget=forms.TextInput(attrs={"class":"form-control"}))
   # country = forms.ChoiceField(label="Country", choices=COUNTRIES, widget=forms.Select(attrs={"class":"form-control"}))
    #phone = PhoneNumberField(label="Phone", )


class QuickAddStaffForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))


class EditstaffForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    job_description = forms.CharField(
        label="Job Description", max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    department = forms.CharField(label="Department", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    skills = forms.CharField(label="Skills", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    educational_qualification = forms.CharField(
        label="Educational Qualifications", max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
    #phone = PhoneNumberField(label="Phone")


class EditCustomerForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, show_hidden_initial=True,
                             initial="customer.admin.email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=250, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    organisation = forms.CharField(
        label="Organisation", max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
   #phone = PhoneNumberField(label="Phone", max_length=250, widget=PhoneNumberInternationalFallbackWidget)


class AddTenantForm(forms.Form):
    name = forms.CharField(label="Name", max_length=300, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    slug = forms.SlugField(label="Slug", max_length=300, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    user_list = []
    if settings.DEBUG == True:
        template_list = (
            ('tenant1', 'template1'),
            ('t2_1608114756', 'template2'),
            ('t3_1607982529', 'template3'),
            ('t4_1605533761', 'template4'),
        )
    else:
        template_list = (
            ('snowball', 'snowball'),
        )
    try:
        users = TenantUser.objects.filter(user_type=3)
        for user in users:
            one_user = (user.id, user.email)
            user_list.append(one_user)
    except:
        user_list = []

    templates = forms.ChoiceField(label="Template", choices=template_list, widget=forms.Select(
        attrs={"class": "form-control"}))
    owner = forms.ChoiceField(label="Email", choices=user_list, widget=forms.Select(
        attrs={"class": "form-control"}))

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class EditTenantForm(forms.Form):
    name = forms.CharField(label="Name", max_length=300, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=500, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    slug = forms.CharField(label="Slug", max_length=300, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    #user_list = []
    # try:
    #    users = TenantUser.objects.filter(user_type=3)
    #    #user = TenantUser.objects.all()
    #    for user in users:
    #        one_user=(user.id, user.id)
    #        user_list.append(one_user)
    # except:
    #    user_list=[]
    #owner_id = forms.ChoiceField(label="User Id",choices=user_list, widget=forms.Select(attrs={"class":"form-control"}))


class CustomerAddTenantForm(forms.Form):
    name = forms.CharField(label="Name", max_length=300, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    slug = forms.CharField(label="Slug", max_length=300, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    user_list = []
    if settings.DEBUG == True:
        template_list = (
            ('t1_1605528147', 'template1'),
            ('t2_1605530124', 'template2'),
            ('t3_1605532812', 'template3'),
            ('t4_1605533761', 'template4'),
        )
    else:
        template_list = (
            ('snowball_1604918204', 'snowball'),
        )
    try:
        users = TenantUser.objects.filter(user_type=3)
        for user in users:
            one_user = (user.id, user.email)
            user_list.append(one_user)
    except:
        user_list = []

    templates = forms.ChoiceField(label="Template", choices=template_list, widget=forms.Select(
        attrs={"class": "form-control"}))
    owner = forms.ChoiceField(initial="user.email", label="Email",
                              choices=user_list, widget=forms.Select(attrs={"class": "form-control"}))


class EditTenantForm(forms.Form):
    name = forms.CharField(label="Name", max_length=300, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    description = forms.CharField(label="Description", max_length=500, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    slug = forms.CharField(label="Slug", max_length=300, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    #user_list = []
    # try:
    #    users = TenantUser.objects.filter(user_type=3)
    #    #user = TenantUser.objects.all()
    #    for user in users:
    #        one_user=(user.id, user.id)
    #        user_list.append(one_user)
    # except:
    #    user_list=[]
    #owner_id = forms.ChoiceField(label="User Id",choices=user_list, widget=forms.Select(attrs={"class":"form-control"}))


class DepartmentCreateForm(forms.Form):
    name = forms.CharField(max_length=250, label="Name", widget=forms.TextInput(
        attrs={"class": "form-control"}))
