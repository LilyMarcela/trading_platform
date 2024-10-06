# trading/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Strategy

# trading/forms.py

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email Address",  # Custom label for email
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    username = forms.CharField(
        label="Username",  # Custom label for username
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        help_text="Choose a unique username."  # Custom help text for username
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter a strong password."
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# trading/forms.py

from django import forms
from .models import Strategy

# Form to run a strategy
class RunStrategyForm(forms.Form):  # Using Form instead of ModelForm if you're selecting an existing strategy
    strategy = forms.ModelChoiceField(queryset=Strategy.objects.all(), label="Select Strategy")
