from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['subscription', 'due_date', 'invoice_number', 'amount', 'credit_used', 'payment_method', 'status', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'subscription': 'Subscription',
            'due_date': 'Due date',
            'invoice_number': 'Invoice number',
            'amount': 'Amount',
            'credit_used': 'Credit used',
            'payment_method': 'Payment method',
            'status': 'Status',
            'notes': 'Notes',
        }