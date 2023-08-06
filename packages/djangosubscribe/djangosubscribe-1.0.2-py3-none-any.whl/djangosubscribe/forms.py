from django import forms
from djangosubscribe.models import SubscriberModel


class SubscriberEmailOnlyForm(forms.ModelForm):
    class Meta:
        model = SubscriberModel
        fields = ["email"]

        labels = {
            "email": "Email"
        }

        help_texts = {
            "email": "We'll never share your email with anyone else."
        }

        widgets = {
            "email": forms.EmailInput(attrs={'type': 'email', 'class': 'form-control rounded-0', 'placeholder': 'Email Address.'})
        }
