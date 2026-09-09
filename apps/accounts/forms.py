from django import forms
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
import re


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email Address'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '+91 98765 43210'}))
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. Mumbai, Delhi, Bengaluru'}))
    state = forms.ChoiceField(choices=UserProfile.INDIAN_STATES, required=False, widget=forms.Select(attrs={'class': 'form-select luxury-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Create Password (min 6 characters)'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Username'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        cleaned = re.sub(r'[\s\-\+]', '', phone)
        if len(cleaned) < 10:
            raise forms.ValidationError("Please provide a valid 10-digit mobile number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control luxury-input'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control luxury-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control luxury-input'}))

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'alternate_phone', 'address_line1', 'address_line2', 'landmark', 'city', 'state', 'pincode']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '+91 98765 43210'}),
            'alternate_phone': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Alternate Contact (Optional)'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Flat/House No., Building, Street'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Area, Locality'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Nearby Landmark'}),
            'city': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'City'}),
            'state': forms.Select(attrs={'class': 'form-select luxury-input'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '6-digit Pincode'}),
        }
