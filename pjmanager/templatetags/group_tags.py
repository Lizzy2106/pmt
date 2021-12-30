from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
	# Check if user has group
	group = Group.objects.filter(name=group_name)
	if group:
		group = group.first()
		return group in user.groups.all()
	else:
		return False

@register.filter(name='has_user') 
def has_user(group_name):
	# Get all user of a group
	users = User.objects.filter(groups__name=group_name)
	
	return users

@register.filter(name='perms_list') 
def perms_list(group):
	return group.permissions.all()