from django.contrib import admin
from .models import (
	Category,
	Settings,
	AboutUs,
	ContactUs,
)

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'parent', 'slug']
	prepopulated_fields = {'slug': ('name',)}
	search_fields = ('name',)
	ordering = ('updated_at',)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
	list_display = ["name", "url"]

	def has_add_permission(self, request):
		return not Settings.objects.exists()


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
	list_display = ["email", "phone", "short_text"]

	def has_add_permission(self, request):
		return not AboutUs.objects.exists()

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
	list_display = ["full_name", "email", "phone", "short_text"]
	search_fields = ('full_name', "email", "phone", "text")
	ordering = ("create_at",)