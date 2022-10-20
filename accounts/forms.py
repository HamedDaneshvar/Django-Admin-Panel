from django import forms
from django.contrib.auth.forms import (
	UserCreationForm,
	UserChangeForm,
)
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	password2 = None
	
	class Meta:
		model = CustomUser
		fields = ("email", "full_name")


class CustomUserChangeForm(UserChangeForm):
	
	class Meta:
		model = CustomUser
		fields = ("email",)


class ProfileForm(forms.ModelForm):
	address = forms.Textarea()
	
	class Meta:
		model = CustomUser
		fields = ("nick_name", "full_name", "phone",
				  "email", "address", "avatar",)
		