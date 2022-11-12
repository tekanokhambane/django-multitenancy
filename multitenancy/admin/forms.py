from django import forms
from multitenancy.apps.models import Package, Tenant, TenantType

from multitenancy.users.models import Customer


class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name','username', 'password', 'email']
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
    
    type_list = []
    try:
        types = TenantType.objects.filter()
        for type in types:
            one_type = (type.name, type.name)
            type_list.append(one_type)
    except:
        plan_list = []
    
    type = forms.ChoiceField(label="Type", choices=type_list, widget=forms.Select(
        attrs={"class": "form-control"}))
    class Meta:
        model = Tenant
        fields = ['name', 'slug', 'type']

class PackageForm(forms.ModelForm):
    
    class Meta:
        model = Package
        fields = ['name', 'price']
