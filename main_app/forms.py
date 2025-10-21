from django import forms
from .models import Feeding
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    class Meta: 
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']