from django.http import HttpResponse
from django.shortcuts import (
	render,
	redirect,
	get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm
from .forms import (
	ProfileForm,
	CreateUserPanelForm,
	UpdateUserPanelForm,
)

@login_required
def index(request):
	return render(request,
				  "base.html",)


@login_required
def profile(request):
	user = CustomUser.objects.get(id=request.user.id)
	if request.method == "POST":
		profile_form = ProfileForm(request.POST, request.FILES, instance=user)
		profile_form.save()
		return redirect("panel:profile")
	else:
		profile_form = ProfileForm(instance=user)
		password_change_form = PasswordChangeForm(user=request.user)

	return render(request,
				  "panel/profile.html",
				  {"profile_form": profile_form,
				   "password_change_form": password_change_form,})


@login_required
def users_list(request):
	users = CustomUser.objects.filter(is_superuser=False,
									  is_staff=False,)

	create_user_form = CreateUserPanelForm()
	update_user_from = UpdateUserPanelForm()
	return render(request,
				  "panel/users/list.html",
				  {"users": users,
				   "create_user_form": create_user_form,
				   "update_user_form": update_user_from,})

@login_required
def create_user(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST, request.FILES)
		if form.is_valid():
			email = form.cleaned_data.get("email")
			form = form.save(commit=False)
			form.username = email
			form.save()
			return redirect("panel:users")
	else:
		return HttpResponse("Method not allowed!")

@login_required
def update_user(request, id):
	user = get_object_or_404(CustomUser, id=id)

	if request.method == "POST":
		form = UpdateUserPanelForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			user = form.save(commit=False)
			if form.cleaned_data['password']:
				user.set_password(form.cleaned_data['password'])
			user.save()
			return redirect("panel:users")
	else:
		return HttpResponse("Method not allowed!")

@login_required
def delete_user(request, id):
	user = get_object_or_404(CustomUser, id=id)
	if request.method == "POST":
		user.delete()
		return redirect("panel:users")
	else:
		return HttpResponse("Method not allowed!")
