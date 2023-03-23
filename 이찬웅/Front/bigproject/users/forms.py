from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
# from .models import User

[]
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
