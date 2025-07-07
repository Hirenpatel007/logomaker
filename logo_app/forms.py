from django import forms
from django.core.exceptions import ValidationError
from .models import LogoRequest, LogoFeedback, Industry, LogoStyle, ColorScheme

class LogoGenerationForm(forms.ModelForm):
    """Professional logo generation form"""
    
    class Meta:
        model = LogoRequest
        fields = [
            'business_name', 'business_description', 'industry', 
            'style', 'color_scheme', 'custom_prompt', 'variations_count'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your business name',
                'maxlength': 200
            }),
            'business_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Describe your business, values, and what makes you unique...',
                'rows': 4,
                'maxlength': 1000
            }),
            'industry': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'style': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'color_scheme': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'custom_prompt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Any specific requirements or ideas for your logo...',
                'rows': 3,
                'maxlength': 500
            }),
            'variations_count': forms.Select(
                choices=[(i, f'{i} variations') for i in range(1, 9)],
                attrs={
                    'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set querysets for choice fields
        self.fields['industry'].queryset = Industry.objects.filter(is_active=True).order_by('name')
        self.fields['style'].queryset = LogoStyle.objects.filter(is_active=True).order_by('sort_order', 'name')
        self.fields['color_scheme'].queryset = ColorScheme.objects.filter(is_active=True).order_by('sort_order', 'name')
        
        # Set default values
        self.fields['variations_count'].initial = 4
        
        # Add help text
        self.fields['business_name'].help_text = "The name of your business or brand"
        self.fields['business_description'].help_text = "Tell us about your business to help AI create better logos"
        self.fields['custom_prompt'].help_text = "Optional: Any specific design elements you want included"
        self.fields['variations_count'].help_text = "Number of logo variations to generate (1-8)"
    
    def clean_business_name(self):
        business_name = self.cleaned_data.get('business_name')
        if not business_name or len(business_name.strip()) < 2:
            raise ValidationError("Business name must be at least 2 characters long.")
        return business_name.strip()
    
    def clean_variations_count(self):
        variations_count = self.cleaned_data.get('variations_count')
        if not 1 <= variations_count <= 8:
            raise ValidationError("Variations count must be between 1 and 8.")
        return variations_count

class FeedbackForm(forms.ModelForm):
    """Logo feedback form"""
    
    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ Excellent'),
        (4, '⭐⭐⭐⭐ Good'),
        (3, '⭐⭐⭐ Average'),
        (2, '⭐⭐ Poor'),
        (1, '⭐ Very Poor'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'rating-radio'
        })
    )
    
    class Meta:
        model = LogoFeedback
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Share your thoughts about this logo...',
                'rows': 3,
                'maxlength': 500
            })
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        try:
            rating = int(rating)
            if not 1 <= rating <= 5:
                raise ValidationError("Rating must be between 1 and 5.")
            return rating
        except (ValueError, TypeError):
            raise ValidationError("Invalid rating value.")

class ContactForm(forms.Form):
    """Contact form for support"""
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Your full name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'your.email@example.com'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '+91 9876543210'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'What can we help you with?'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Tell us more about your inquiry...',
            'rows': 5
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove non-digit characters
            phone_digits = ''.join(filter(str.isdigit, phone))
            if len(phone_digits) < 10:
                raise ValidationError("Please enter a valid phone number.")
        return phone

class NewsletterForm(forms.Form):
    """Newsletter subscription form"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Basic email validation (Django handles most of it)
            if len(email) > 254:
                raise ValidationError("Email address is too long.")
        return email