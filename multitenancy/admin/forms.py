from django import forms
from multitenancy.apps.models import Package, Tenant, TenantType
from multitenancy.subscriptions.models import Plan

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
    
    class Meta:
        model = Tenant
        fields = ['name', 'slug', 'type']

class PlanForm(forms.ModelForm):
    
    class Meta:
        model = Plan
        fields = ['name', 'description', 'price']
