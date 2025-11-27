from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):

    # Safe: password will be hashed using set_password() in views.py
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
