from django.db import models
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel 

# Create your models here.
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