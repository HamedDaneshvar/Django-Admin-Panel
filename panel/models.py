import os
from django.db import models
from django.core.validators import MinLengthValidator
from django.template.defaultfilters import truncatechars
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel 

def get_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'logo.{ext}'
    return os.path.join(f'logo/', filename)

def get_favicon_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'favicon.{ext}'
    return os.path.join(f'logo/', filename)


class Category(GeneralModel):
	name = models.CharField(
		max_length=250,
		verbose_name=_("Name"),)
	slug = models.SlugField(
		max_length=250,
		unique=True,
		verbose_name=_("Slug"),)
	parent = models.ForeignKey(
		'self',
		on_delete=models.SET_NULL,
		default=None,
		null=True,
		blank=True,
		related_name="children",
		verbose_name=_("Parent"),)

	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")

	def __str__(self):
		return self.name


class Settings(GeneralModel):
	name = models.CharField(
		default="admin panel",
		max_length=250,
		verbose_name=_("Name"),)
	url = models.URLField(
		null=True,
		blank=True,
		default="site.com",
		verbose_name=_("website url"),)
	logo = models.ImageField(
		upload_to=get_logo_path,
		default="static/assets/img/brand/logo.png",
		null=True,
		blank=True,
		verbose_name=_("Logo"),)
	favicon = models.ImageField(
		upload_to=get_favicon_path,
		default="static/assets/img/brand/favcion.ico",
		null=True,
		blank=True,
		verbose_name=_("Favicon"),)
	slug = models.SlugField(
		max_length=250,
		unique=True,
		default="settings",
		verbose_name=_("Slug"),)

	class Meta:
		verbose_name = _("Setting")
		verbose_name_plural = _("Settings")

	def __str__(self):
		return self.name


class AboutUs(GeneralModel):
	text = models.TextField(
		verbose_name=_("Text"))
	email = models.EmailField(
		default="info@site.com",
		null=True,
		blank=True,
		verbose_name=_("Email"),)
	phone = models.CharField(
		max_length=13,
		default="+989121231234",
		null=True,
		blank=True,
		verbose_name=_("Phone"),)
	slug = models.SlugField(
		max_length=250,
		unique=True,
		default="aboutus",
		verbose_name=_("Slug"),)
	


	class Meta:
		verbose_name = _("About Us")
		verbose_name_plural = _("About Us")

	def __str__(self):
		return "About Us"

	@property
	def short_text(self):
		return truncatechars(self.text, 100)


class ContactUs(GeneralModel):
	full_name = models.CharField(max_length=128,
								 verbose_name=_("Full name"),)
	email = models.EmailField(
		verbose_name=_("Email"),)
	text = models.TextField(
		verbose_name=_("Text"))
	phone = models.CharField(max_length=13,
							 validators=[MinLengthValidator(10)],
							 blank=True,
							 null=True,
							 verbose_name=_("Phone"),)

	class Meta:
		verbose_name = _("Contact Us")
		verbose_name_plural = _("Contact Us")

	def __str__(self):
		return f"{self.full_name} -> {self.email}"

	@property
	def short_text(self):
		return truncatechars(self.text, 100)