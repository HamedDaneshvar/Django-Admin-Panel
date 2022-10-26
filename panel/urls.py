from django.urls import path
from . import views

app_name = "panel"
urlpatterns = [
	path("home/", views.index, name="home"),
	path("profile/", views.profile, name="profile"),

	# users
	path("users/", views.users_list, name="users_list"),
	path("users/create/", views.create_user, name="create_user"),
	path("users/update/<int:id>/", views.update_user, name="update_user"),
	path("users/delete/<int:id>/", views.delete_user, name="delete_user"),

	# management
	path("admin/users/", views.management_users_list, name="management_users_list"),
	path("admin/users/create/", views.create_staff_user, name="create_staff_user"),
	path("admin/users/update/<int:id>/", views.update_staff_user, name="update_staff_user"),
	path("admin/users/delete/<int:id>/", views.delete_staff_user, name="delete_staff_user"),
	path("admin/roles/", views.roles_list, name="roles_list"),
	path("admin/roles/create/", views.create_role, name="create_role"),
	path("admin/roles/update/<int:id>/", views.update_role, name="update_role"),
	path("admin/roles/delete/<int:id>/", views.delete_role, name="delete_role"),
]
