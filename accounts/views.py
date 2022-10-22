from django.shortcuts import (
	render,
	redirect,
)
from django.contrib.auth import (
	login,
	authenticate,
)
from .forms import (
	CustomUserCreationForm,
)


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