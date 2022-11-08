from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import (
	UserCreationForm,
	UserChangeForm,
)
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(),
		validators=[validate_password],)
	password2 = None
	
	class Meta:
		model = CustomUser
		fields = ("email", "full_name")


class CustomUserChangeForm(UserChangeForm):
	
	class Meta:
		model = CustomUser
		fields = ("email",)