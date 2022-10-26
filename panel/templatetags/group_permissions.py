from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='permissions_list')
def permissions_list(group, permission_codename):
	group = Group.objects.filter(id=group.id)
	permission = group[0].permissions.filter(codename=permission_codename)
	# permission = group.objects.filter(codename=permission_codename)

	if permission:
		return True
	return False