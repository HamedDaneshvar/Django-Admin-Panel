from django.shortcuts import (
	render,
	redirect,
)
from django.contrib import messages
from django.utils.translation import gettext as _
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
			full_name = form.cleaned_data.get("full_name")
			raw_password = form.cleaned_data.get("password1")
			form = form.save(commit=False)
			form.username = email
			form.nick_name = full_name
			form.save()
			user = authenticate(email=email, password=raw_password)
			login(request, user)
			message_text = _(f"حساب کاربری شما با موفقیت ساخته شد. لطفا ایمیل خود را تایید کنید.")
			messages.success(request, message_text)
			return redirect("/")
		else:
			if form.errors.get('email'):
				message_text = _(f"این ایمیل قبلا ثبت شده است. لطفا وارد شوید.")
				messages.error(request, message_text)
			elif form.errors.get('password1'):
				for err in form.errors.get('password1'):
					message_text = _(err)
					messages.error(request, message_text)

	else:
		form = CustomUserCreationForm()
	return render(request,
				  "accounts/signup.html",
				  {"form": form,})