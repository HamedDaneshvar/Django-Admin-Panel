from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from accounts.models import CustomUser
from .models import (
	Category,
	Settings,
	AboutUs,
	ContactUs,
)


class ProfileForm(forms.ModelForm):
	address = forms.CharField(widget=forms.Textarea(attrs={"rows":2}),
							  required=False,)
	
	class Meta:
		model = CustomUser
		fields = ("nick_name", "full_name", "phone",
				  "email", "address", "avatar",)


class CreateStaffUserForm(UserCreationForm):
	password2 = None
	roles = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
	
	class Meta:
		model = CustomUser
		fields = ("email", "full_name", "roles",)


class UpdateStaffUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(),
							   required=False,)
	address = forms.CharField(widget=forms.Textarea(attrs={"rows":2}),
							  required=False,)
	roles = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

	class Meta:
		model = CustomUser
		fields = ("nick_name", "full_name", "password", "phone",
				  "email", "address", "avatar", "is_active", "roles",)


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

class CategoryPanelForm(forms.ModelForm):

	class Meta:
		model = Category
		fields = ["name", "parent", "slug",]


class SettingsPanelForm(forms.ModelForm):

	class Meta:
		model = Settings
		fields = ["name", "url", "logo", "favicon"]


class AboutUsPanelForm(forms.ModelForm):

	class Meta:
		model = AboutUs
		fields = ["text", "email", "phone",]


class ContactUsPanelForm(forms.ModelForm):

	class Meta:
		model = ContactUs
		fields = ["full_name", "email", "phone", "text",]