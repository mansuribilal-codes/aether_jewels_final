from django import forms
from apps.store.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(5, '★★★★★ (5 Stars - Exceptional)'), (4, '★★★★☆ (4 Stars - Great)'), (3, '★★★☆☆ (3 Stars - Good)'), (2, '★★☆☆☆ (2 Stars - Fair)'), (1, '★☆☆☆☆ (1 Star - Poor)')], attrs={'class': 'form-select luxury-input'}),
            'title': forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Review Headline'}),
            'comment': forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 3, 'placeholder': 'Share your experience with this jewellery piece...'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Your Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Email Address'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': '+91 Phone Number'}))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control luxury-input', 'placeholder': 'Subject / Inquiry Type'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control luxury-input', 'rows': 4, 'placeholder': 'Your Message / Inquiry...'}))
