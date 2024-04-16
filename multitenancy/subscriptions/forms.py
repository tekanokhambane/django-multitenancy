from django import forms
from .models import Plan

class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = ['name', 'description', 'price']


class ProductFeatureForm(forms.Form):
    name = forms.CharField(label="Name", max_length=250)
    description = forms.CharField(label="Description", max_length=250, widget=forms.Textarea(
        attrs={"class": "form-control"}))
    plan = forms.IntegerField(label="plan", widget=forms.HiddenInput())
    plan_name = forms.CharField(widget=forms.HiddenInput())