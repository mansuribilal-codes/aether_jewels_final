from django import forms
from apps.consultations.models import ConsultationBooking, BespokeInquiry
import datetime


class ConsultationBookingForm(forms.ModelForm):
    class Meta:
        model = ConsultationBooking
        fields = ['name', 'email', 'phone', 'consultation_type', 'preferred_date', 'time_slot', 'interest_category', 'budget_range', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '+91 98765 43210'}),
            'consultation_type': forms.Select(attrs={'class': 'form-select luxury-input'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control luxury-input', 'type': 'date', 'min': datetime.date.today().isoformat()}),
            'time_slot': forms.Select(attrs={'class': 'form-select luxury-input'}),
            'interest_category': forms.Select(attrs={'class': 'form-select luxury-input'}),
            'budget_range': forms.Select(attrs={'class': 'form-select luxury-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 3, 'placeholder': 'Describe your design vision, gemstone preferences or special requirements...'}),
        }


class BespokeInquiryForm(forms.ModelForm):
    class Meta:
        model = BespokeInquiry
        fields = ['name', 'email', 'phone', 'city', 'metal_preference', 'gemstone_preference', 'budget_estimate', 'design_idea']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '+91 Mobile'}),
            'city': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'City (e.g. Mumbai, Delhi)'}),
            'metal_preference': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. 18K Yellow Gold / Platinum 950'}),
            'gemstone_preference': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. D/IF Diamonds, Zambian Emeralds'}),
            'budget_estimate': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'e.g. ₹5,00,000 - ₹10,00,000'}),
            'design_idea': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 4, 'placeholder': 'Describe your custom bespoke heirloom concept...'}),
        }
