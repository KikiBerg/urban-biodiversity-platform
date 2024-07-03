from .models import ContactUs
from django import forms


class ContactUsForm(forms.ModelForm):
    """
    Form class for users to request contact
    """
    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'message')
