from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from accounts.models import CustomUser


class ProfileForm(forms.ModelForm):
	address = forms.CharField(widget=forms.Textarea(attrs={"rows":2}),
							  required=False,)
	
	class Meta:
		model = CustomUser
		fields = ("nick_name", "full_name", "phone",
				  "email", "address", "avatar",)


class CreateUserPanelForm(UserCreationForm):
	password2 = None

	class Meta:
		model = CustomUser
		fields = ("full_name", "email", "avatar",)


class UpdateUserPanelForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(),
							   required=False,)
	address = forms.CharField(widget=forms.Textarea(attrs={"rows":2}),
							  required=False,)

	class Meta:
		model = CustomUser
		fields = ("nick_name", "full_name", "password", "phone",
				  "email", "address", "avatar", "is_active",)


class PermissionPanelForm(forms.ModelForm):
	permissions = None
	management = forms.BooleanField(required=False,)
	settings = forms.BooleanField(required=False,)
	category = forms.BooleanField(required=False,)
	users = forms.BooleanField(required=False,)
	
	class Meta:
		model = Group
		fields = ['name', 'management', 'settings',
				  'category', 'users',]