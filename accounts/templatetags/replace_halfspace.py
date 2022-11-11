from django import template

register = template.Library()

@register.filter(name='replace_halfspace')
def replace_halfspace(text):
	text = text.replace(u'\u200c', ' ')
	return text