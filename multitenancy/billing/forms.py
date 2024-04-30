from django import forms
from django_select2.forms import ModelSelect2Widget
from .models import Invoice, Refund


class InvoiceSelect2Widget(ModelSelect2Widget):
    search_fields = ["invoice__invoice_number__icontains"]


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "subscription",
            "due_date",
            "amount",
            "credit_used",
            "payment_method",
            "status",
            "notes",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "subscription": "Subscription",
            "due_date": "Due date",
            "invoice_number": "Invoice number",
            "amount": "Amount",
            "credit_used": "Credit used",
            "payment_method": "Payment method",
            "status": "Status",
            "notes": "Notes",
        }


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = "__all__"
        exclude = ["created_at", "updated_at"]
        help_texts = {
            "invoice": "Search for an invoice by invoice number.",
            "amount": "Enter the amount to refund.",
        }
        labels = {
            "invoice": "Invoice",
            "amount": "Amount",
        }
        widgets = {"invoice": InvoiceSelect2Widget(queryset=Invoice.objects.all())}
