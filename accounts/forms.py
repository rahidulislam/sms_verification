from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2',)
        
        