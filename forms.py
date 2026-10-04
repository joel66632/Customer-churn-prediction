from django import forms
from django.contrib.auth.models import User

class ChurnPredictionForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John Doe'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 35'}))
    gender = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female")], widget=forms.Select(attrs={'class': 'form-select'}))
    tenure = forms.IntegerField(label="Tenure (months)", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12'}))
    usage_frequency = forms.IntegerField(label="Usage Frequency", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Times/month'}))
    support_calls = forms.IntegerField(label="Support Calls", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2'}))
    payment_delay = forms.IntegerField(label="Payment Delay", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5'}))
    subscription_type = forms.ChoiceField(
        choices=[("Basic", "Basic"), ("Standard", "Standard"), ("Premium", "Premium")],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    contract_length = forms.IntegerField(label="Contract Length", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12'}))
    total_spend = forms.FloatField(label="Total Spend", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1200'}))
    last_interaction = forms.IntegerField(label="Last Interaction", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 30'}))

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    store_name = forms.CharField(max_length=255, required=True)
    license_number = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    license_file = forms.FileField(required=True, label="Store License (PDF/Image)")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)