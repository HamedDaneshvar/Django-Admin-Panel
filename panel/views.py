from django.http import HttpResponse
from django.shortcuts import (
	render,
	redirect,
	get_object_or_404
)
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import (
	Group,
	Permission,
)
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm
from .forms import (
	ProfileForm,
	CreateUserPanelForm,
	UpdateUserPanelForm,
	PermissionPanelForm,
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
			full_name = form.cleaned_data.get("full_name")
			user = form.save(commit=False)
			user.username = email
			user.nick_name = full_name
			user.save()
			return redirect("panel:users_list")
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
			return redirect("panel:users_list")
	else:
		return HttpResponse("Method not allowed!")

@login_required
def delete_user(request, id):
	user = get_object_or_404(CustomUser, id=id)
	if request.method == "POST":
		user.delete()
		return redirect("panel:users_list")
	else:
		return HttpResponse("Method not allowed!")


@login_required
def management_users_list(request):
	if request.user.is_superuser:
		users = CustomUser.objects.filter(Q(is_staff=True) |
									  	  Q(is_superuser=True))
	else:
		users = CustomUser.objects.filter(is_staff=True)

	create_user_form = CreateUserPanelForm()
	update_user_from = UpdateUserPanelForm()
	return render(request,
				  "panel/management/list.html",
				  {"users": users,
				   "create_user_form": create_user_form,
				   "update_user_form": update_user_from,})


@login_required
def create_staff_user(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST, request.FILES)
		if form.is_valid():
			email = form.cleaned_data.get("email")
			full_name = form.cleaned_data.get("full_name")
			user = form.save(commit=False)
			user.username = email
			user.nick_name = full_name
			user.is_staff = True
			user.save()
			return redirect("panel:management_users_list")
	else:
		return HttpResponse("Method not allowed!")

@login_required
def update_staff_user(request, id):
	user = get_object_or_404(CustomUser, id=id)

	if request.method == "POST":
		form = UpdateUserPanelForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			user = form.save(commit=False)
			if form.cleaned_data['password']:
				user.set_password(form.cleaned_data['password'])
			user.save()
			return redirect("panel:management_users_list")
	else:
		return HttpResponse("Method not allowed!")

@login_required
def delete_staff_user(request, id):
	user = get_object_or_404(CustomUser, id=id)

	if request.user.id == id:
		return redirect("panel:management_users_list")

	if request.method == "POST":
		user.delete()
		return redirect("panel:management_users_list")
	else:
		return HttpResponse("Method not allowed!")


@login_required
def roles_list(request):
	groups = Group.objects.all()
	create_group_form = PermissionPanelForm()
	update_group_form = PermissionPanelForm()
	return render(request,
				  "panel/management/role_list.html",
				  {"groups": groups,
				   "create_group_form": create_group_form,
				   "update_group_form": update_group_form,})

@login_required
def create_role(request):
	if request.method == "POST":
		form = PermissionPanelForm(request.POST)
		if form.is_valid():
			role_name = form.cleaned_data['name'].lower()
			role = Group.objects.filter(name=role_name)
			if role:
				return HttpResponse("role already exist!")
			group = form.save()

			# set permission to group
			if form.cleaned_data['management']:
				permission = Permission.objects.get(codename="can_manage_staff_users")
				group.permissions.add(permission)
			if form.cleaned_data['settings']:
				permission = Permission.objects.get(codename="can_manage_website_settings")
				group.permissions.add(permission)
			if form.cleaned_data['category']:
				permission = Permission.objects.get(codename="can_manage_categories")
				group.permissions.add(permission)
			if form.cleaned_data['users']:
				permission = Permission.objects.get(codename="can_manage_simple_users")
				group.permissions.add(permission)

			return redirect("panel:roles_list")
		else:
			return HttpResponse("role already exist!")
	else:
		return HttpResponse("Method not allowed!")

@login_required
def update_role(request, id):
	group = get_object_or_404(Group, id=id)
	if request.method == "POST":
		form = PermissionPanelForm(request.POST, instance=group)
		if form.is_valid():
			group.name = form.cleaned_data['name']
			# set or remove permission to group
			permission = Permission.objects.get(codename="can_manage_staff_users")
			if form.cleaned_data['management']:
				group.permissions.add(permission)
			else:
				group.permissions.remove(permission)
			
			permission = Permission.objects.get(codename="can_manage_website_settings")
			if form.cleaned_data['settings']:
				group.permissions.add(permission)
			else:
				group.permissions.remove(permission)
			
			permission = Permission.objects.get(codename="can_manage_categories")
			if form.cleaned_data['category']:
				group.permissions.add(permission)
			else:
				group.permissions.remove(permission)
			
			permission = Permission.objects.get(codename="can_manage_simple_users")
			if form.cleaned_data['users']:
				group.permissions.add(permission)
			else:
				group.permissions.remove(permission)

			group.save()
			return redirect("panel:roles_list")
		else:
			return HttpResponse("role already exist!")
	else:
		return HttpResponse("Method not allowed!")

@login_required
def delete_role(request, id):
	group = get_object_or_404(Group, id=id)

	if request.method == "POST":
		group.delete()
		return redirect("panel:roles_list")
	else:
		return HttpResponse("Method not allowed!")