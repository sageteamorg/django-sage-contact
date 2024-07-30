from django import forms
from django.utils.translation import gettext_lazy as _

from sage_contact.models import (
    SupportRequestBase,
    SupportRequestWithLocation,
    SupportRequestWithPhone,
    FullSupportRequest
)


class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequestBase
        fields = ['subject', 'full_name', 'email', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': _('Enter the main topic of your message'),
                'class': 'form-control',
                'maxlength': 100,
            }),
            'full_name': forms.TextInput(attrs={
                'placeholder': _('Enter your full name'),
                'class': 'form-control',
                'maxlength': 100,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': _('Enter your email address'),
                'class': 'form-control',
                'maxlength': 254,
            }),
            'message': forms.Textarea(attrs={
                'placeholder': _('Enter your message or inquiry'),
                'class': 'form-control',
                'rows': 5,
            }),
        }
        help_texts = {
            'subject': _('Please provide a brief subject for your message (max 100 characters).'),
            'full_name': _('Enter your full name as you would like us to address you. Only letters, spaces, hyphens, and apostrophes are allowed.'),
            'email': _('We will use this email to contact you. Make sure it is a valid email address.'),
            'message': _('Provide detailed information about your inquiry or issue.'),
        }
        error_messages = {
            'subject': {
                'required': _('Subject is required.'),
                'max_length': _('Subject cannot exceed 100 characters.'),
            },
            'full_name': {
                'required': _('Full name is required.'),
                'max_length': _('Full name cannot exceed 100 characters.'),
                'invalid': _('Enter a valid name. Only letters, spaces, hyphens, and apostrophes are allowed.'),
            },
            'email': {
                'required': _('Email is required.'),
                'max_length': _('Email cannot exceed 254 characters.'),
                'invalid': _('Enter a valid email address.'),
            },
            'message': {
                'required': _('Message is required.'),
            },
        }


class SupportRequestWithPhoneForm(SupportRequestForm):
    class Meta(SupportRequestForm.Meta):
        model = SupportRequestWithPhone
        fields = SupportRequestForm.Meta.fields + ['phone_number']
        widgets = {
            **SupportRequestForm.Meta.widgets,
            'phone_number': forms.TextInput(attrs={
                'placeholder': _('Enter your phone number in international format, e.g., +12025550109'),
                'class': 'form-control',
            }),
        }
        help_texts = {
            **SupportRequestForm.Meta.help_texts,
            'phone_number': _('Your phone number in international format, e.g., +12025550109.'),
        }
        error_messages = {
            **SupportRequestForm.Meta.error_messages,
            'phone_number': {
                'invalid': _('Enter a valid phone number.'),
            },
        }


class SupportRequestWithLocationForm(SupportRequestWithPhoneForm):
    class Meta(SupportRequestWithPhoneForm.Meta):
        model = SupportRequestWithLocation
        fields = SupportRequestWithPhoneForm.Meta.fields + ['country', 'ip_address']
        widgets = {
            **SupportRequestWithPhoneForm.Meta.widgets,
            'country': forms.Select(attrs={
                'class': 'form-control',
            }),
            'ip_address': forms.TextInput(attrs={
                'placeholder': _('Your IP address (for internal use only)'),
                'class': 'form-control',
            }),
        }
        help_texts = {
            **SupportRequestWithPhoneForm.Meta.help_texts,
            'country': _('Select the country you are contacting us from. Useful for regional marketing campaigns and statistics.'),
            'ip_address': _('For internal use only. Your IP address is recorded for security and demographic purposes.'),
        }
        error_messages = {
            **SupportRequestWithPhoneForm.Meta.error_messages,
            'ip_address': {
                'invalid': _('Enter a valid IP address.'),
            },
        }

class FullSupportRequestForm(SupportRequestWithLocationForm):
    class Meta(SupportRequestWithLocationForm.Meta):
        model = FullSupportRequest
        fields = SupportRequestWithLocationForm.Meta.fields + [
            'user', 'contacted_before', 'contact_reason', 'preferred_contact_method'
        ]
        widgets = {
            **SupportRequestWithLocationForm.Meta.widgets,
            'user': forms.Select(attrs={
                'class': 'form-control',
            }),
            'contacted_before': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'contact_reason': forms.Select(attrs={
                'class': 'form-control',
            }),
            'preferred_contact_method': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        help_texts = {
            **SupportRequestWithLocationForm.Meta.help_texts,
            'user': _('If you are a registered user, this field links your account to the contact form.'),
            'contacted_before': _('Check this box if you have made previous contact. It helps us track our ongoing relationship with you.'),
            'contact_reason': _('Specify the reason for your contact. This helps us to direct your query to the appropriate team.'),
            'preferred_contact_method': _('Indicate your preferred method of communication. We respect your choice and will contact you accordingly.'),
        }
        error_messages = {
            **SupportRequestWithLocationForm.Meta.error_messages,
            'contact_reason': {
                'invalid_choice': _('Select a valid reason for contact.'),
            },
            'preferred_contact_method': {
                'invalid_choice': _('Select a valid preferred contact method.'),
            },
        }
