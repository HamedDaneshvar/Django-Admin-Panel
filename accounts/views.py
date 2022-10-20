from django.shortcuts import (
	render,
	redirect,
)
from django.contrib.auth import (
	login,
	authenticate,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import CustomUser
from .forms import (
	CustomUserCreationForm,
	ProfileForm,
)

@login_required
def index(request):
	return render(request,
				  "base.html",)


def signup(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get("email")
			raw_password = form.cleaned_data.get("password1")
			form = form.save(commit=False)
			form.username = email
			form.save()
			user = authenticate(email=email, password=raw_password)
			login(request, user)
			return redirect("/")
	else:
		form = CustomUserCreationForm()
	return render(request,
				  "accounts/signup.html",
				  {"form": form,})

@login_required
def profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	if request.method == "POST":
		profile_form = ProfileForm(request.POST, request.FILES, instance=user)
		profile_form.save()
		return redirect("accounts:profile")
	else:
		profile_form = ProfileForm(instance=user)
		password_change_form = PasswordChangeForm(user=request.user)

	return render(request,
				  "accounts/profile.html",
				  {"profile_form": profile_form,
				   "password_change_form": password_change_form,})
