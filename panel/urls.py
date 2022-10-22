from django.urls import path
from . import views

app_name = "panel"
urlpatterns = [
	path("home/", views.index, name="home"),
	path("profile/", views.profile, name="profile"),
	path("users/", views.users_list, name="users"),
	path("users/create/", views.create_user, name="create_user"),
	path("users/update/<int:id>/", views.update_user, name="update_user"),
	path("users/delete/<int:id>/", views.delete_user, name="delete_user"),
]
