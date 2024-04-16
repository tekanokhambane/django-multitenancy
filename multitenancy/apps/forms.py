from django import forms
from multitenancy.apps.models import Tenant

class TenantForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = ['name', 'slug', 'type']
