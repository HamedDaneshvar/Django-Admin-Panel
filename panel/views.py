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
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm
from .models import (
	Category,
	Settings,
	AboutUs,
	ContactUs,
)
from .forms import (
	AboutUsPanelForm,
	ProfileForm,
	CreateUserPanelForm,
	UpdateUserPanelForm,
	PermissionPanelForm,
	CategoryPanelForm,
	CreateStaffUserForm,
	UpdateStaffUserForm,
	SettingsPanelForm,
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
@permission_required("accounts.can_manage_simple_users", raise_exception=True,)
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
@permission_required("accounts.can_manage_simple_users", raise_exception=True,)
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
@permission_required("accounts.can_manage_simple_users", raise_exception=True,)
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
@permission_required("accounts.can_manage_simple_users", raise_exception=True,)
def delete_user(request, id):
	user = get_object_or_404(CustomUser, id=id)
	if request.method == "POST":
		user.delete()
		return redirect("panel:users_list")
	else:
		return HttpResponse("Method not allowed!")


@login_required
@permission_required("accounts.can_manage_staff_users", raise_exception=True,)
def management_users_list(request):
	if request.user.is_superuser:
		users = CustomUser.objects.filter(Q(is_staff=True) |
									  	  Q(is_superuser=True))
	else:
		users = CustomUser.objects.filter(Q(is_staff=True) &
									  	  Q(is_superuser=False))

	groups = Group.objects.all()
	create_staffuser_form = CreateStaffUserForm()
	update_staffuser_form = UpdateStaffUserForm()
	return render(request,
				  "panel/management/list.html",
				  {"users": users,
				   "groups": groups,
				   "create_staffuser_form": create_staffuser_form,
				   "update_staffuser_form": update_staffuser_form,})

@login_required
@permission_required("accounts.can_manage_staff_users", raise_exception=True,)
def create_staff_user(request):
	if request.method == "POST":
		form = CreateStaffUserForm(request.POST, request.FILES)
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
@permission_required("accounts.can_manage_staff_users", raise_exception=True,)
def update_staff_user(request, id):
	user = get_object_or_404(CustomUser, id=id)

	if request.method == "POST":
		form = UpdateStaffUserForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			user = form.save(commit=False)
			if form.cleaned_data['password'] != '':
				user.set_password(form.cleaned_data['password'])
			if form.cleaned_data['roles']:
				group = form.cleaned_data['roles']
				user.groups.add(group)
			else:
				user.groups.clear()
			user.save()
			return redirect("panel:management_users_list")
	else:
		return HttpResponse("Method not allowed!")

@login_required
@permission_required("accounts.can_manage_staff_users", raise_exception=True,)
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
@permission_required("accounts.can_manage_staff_users", raise_exception=True,)
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
@permission_required("accounts.can_manage_staff_users", raise_exception=True,)
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
@permission_required("accounts.can_manage_staff_users", raise_exception=True,)
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
@permission_required("accounts.can_manage_staff_users", raise_exception=True,)
def delete_role(request, id):
	group = get_object_or_404(Group, id=id)

	if request.method == "POST":
		group.delete()
		return redirect("panel:roles_list")
	else:
		return HttpResponse("Method not allowed!")

@login_required
@permission_required("accounts.can_manage_categories", raise_exception=True,)
def categories_list(request):
	categories = Category.objects.all()

	create_category_form = CategoryPanelForm()
	update_category_form = CategoryPanelForm()

	return render(request,
				  "panel/categories/list.html",
				  {"categories": categories,
				   "create_category_form": create_category_form,
				   "update_category_form": update_category_form,})

@login_required
@permission_required("accounts.can_manage_categories", raise_exception=True,)
def create_category(request):
	if request.method == "POST":
		form = CategoryPanelForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("panel:categories_list")
		else:
			return HttpResponse("form isn't valid!")
	else:
		return HttpResponse("Method not allowed!")

@login_required
@permission_required("accounts.can_manage_categories", raise_exception=True,)
def update_category(request, id):
	category = get_object_or_404(Category, id=id)
	if request.method == "POST":
		form = CategoryPanelForm(request.POST, instance=category)
		if form.is_valid():
			form.save()
			return redirect("panel:categories_list")
		else:
			return HttpResponse("form isn't valid!")
	else:
		return HttpResponse("Method not allowed!")

@login_required
@permission_required("accounts.can_manage_categories", raise_exception=True,)
def delete_category(request, id):
	category = get_object_or_404(Category, id=id)
	if request.method == "POST":
		category.delete()
		return redirect("panel:categories_list")
	else:
		return HttpResponse("Method not allowed!")


@login_required
@permission_required("can_manage_website_settings", raise_exception=True,)
def website_settings(request):
	setting = Settings.objects.first()
	if request.method == "POST":
		form = SettingsPanelForm(request.POST, request.FILES, instance=setting)
		if form.is_valid():
			form.save()
	else:
		form = SettingsPanelForm(instance=setting)
	
	return render(request,
				  "panel/settings/website.html",
				  {"form": form,})

@login_required
@permission_required("can_manage_website_settings", raise_exception=True,)
def aboutus_settings(request):
	aboutus = AboutUs.objects.first()
	if request.method == "POST":
		form = AboutUsPanelForm(request.POST, instance=aboutus)
		if form.is_valid():
			form.save()
	else:
		form = AboutUsPanelForm(instance=aboutus)
	
	return render(request,
				  "panel/settings/aboutus.html",
				  {"form": form,})

@login_required
@permission_required("can_manage_website_settings", raise_exception=True,)
def contactus_settings_list(request):
	contactus_list = ContactUs.objects.all().order_by("create_at")

	return render(request,
				  "panel/settings/contactus_list.html",
				  {"contactus_list": contactus_list,})