from django import forms

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
    # country = forms.ChoiceField(label="Country", choices=COUNTRIES, widget=forms.Select(attrs={"class":"form-control"}))
    organisation = forms.CharField(
        label="Organisation", max_length=250, widget=forms.TextInput(attrs={"class": "form-control"}))
