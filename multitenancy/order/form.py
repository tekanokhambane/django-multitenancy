import datetime
from django.utils import timezone
from django import forms
from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import Order, Coupon


class CouponForm(forms.ModelForm):

    code = forms.CharField(
        label="Coupon Code",
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    discount = forms.DecimalField(
        label="Discount",
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    is_active = forms.BooleanField(
        label="Is Active",
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    start_date = forms.DateField(
        label="Start Date",
        required=True,
        initial=timezone.now().strftime("%Y-%m-%d"),
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Start Date",
                "aria-label": "Start Date",
                "aria-required": "true",
                "required": "true",
                "type": "date",
                "autocomplete": "off",
            }
        ),
    )
    end_date = forms.DateField(
        label="End Date",
        required=False,
        initial=timezone.now() + datetime.timedelta(days=30),
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Start Date",
                "aria-label": "Start Date",
                "aria-required": "false",
                "required": "false",
                "type": "date",
                "autocomplete": "off",
            }
        ),
    )
    redeem_by = forms.DateField(
        label="Redeem By",
        required=False,
        initial=timezone.now() + datetime.timedelta(days=30),
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Redeem Date",
                "aria-label": "Redeem Date",
                "aria-required": "false",
                "required": "false",
                "type": "date",
                "autocomplete": "off",
            }
        ),
    )
    usage_limit = forms.IntegerField(
        label="Usage Limit",
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    usage_count = forms.HiddenInput(
        attrs={
            "class": "form-control",
            "value": 0,
            "aria-required": "false",
        },
    )
    minimum_order_amount = forms.DecimalField(
        label="Minimum Order Amount",
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Coupon
        fields = [
            "code",
            "discount",
            "is_active",
            "start_date",
            "end_date",
            "usage_limit",
            "minimum_order_amount",
            "redeem_by",
        ]
