from django import forms
from apps.orders.models import Order
from apps.accounts.models import UserProfile
import re


class CheckoutForm(forms.ModelForm):
    state = forms.ChoiceField(choices=UserProfile.INDIAN_STATES, widget=forms.Select(attrs={'class': 'form-select luxury-input'}))

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone',
            'address_line1', 'address_line2', 'landmark',
            'city', 'state', 'pincode',
            'payment_method', 'gift_message', 'special_instructions'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email for Order & Valuation Certificate'}),
            'phone': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '+91 98765 43210'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Residence / Suite / Building'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Street, Area, Colony'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Prominent Landmark (for armored courier)'}),
            'city': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '6-digit PIN Code'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input luxury-radio'}),
            'gift_message': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 2, 'placeholder': 'Complimentary Hand-written Calligraphy Greeting Message (Optional)'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 2, 'placeholder': 'Delivery instructions, preferred delivery slot or discretion requests'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned = re.sub(r'[\s\-\+]', '', phone)
        if len(cleaned) < 10:
            raise forms.ValidationError("Please provide a valid 10-digit Indian phone number.")
        return phone

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        cleaned = re.sub(r'\s', '', pincode)
        if len(cleaned) != 6 or not cleaned.isdigit():
            raise forms.ValidationError("Please provide a valid 6-digit Indian Postal PIN Code.")
        return cleaned
