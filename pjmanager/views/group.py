from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.models import Group, Permission
from ..forms import GroupForm

from django.contrib import messages# Groups and permissions views

from django.contrib.auth.decorators import login_required
from ..decorators import admin_only

from pprint import pprint

@login_required(login_url='login')
def list(request, *args, **kwargs):
	groups = Group.objects.all()
	perms  = Permission.objects.all()
	context = {
		'groups': groups,
		'perms':perms,
	}
	return render(request, 'group/index.html', context=context)

@login_required(login_url='login')
@admin_only
def create(request, *args, **kwargs):
	form = GroupForm()
	if request.POST:
		form = GroupForm(request.POST)
		pprint(form['permissions'])
		if form.is_valid():
			group = form.save(commit=True)
			# History.objects.create(content_object = group, action=1, user=request.user)
			messages.success(request, f"Un nouveau groupe {form.cleaned_data.get('name')}")

			return redirect('listGroup')

	context = {
		'form': form,
	}
	return render(request, 'group/create.html', context=context)

def show(request, pk):
	group = get_object_or_404(Group, id=pk)
	
	context = {
		'group':group,
	}
	return render(request, 'group/show.html', context=context)

@login_required(login_url='login')
@admin_only
def update(request, pk):
	group = get_object_or_404(Group, id=pk)
	print(group)
	form = GroupForm(instance=group)
	if request.POST:
		form = GroupForm(request.POST or None, instance=group)
		pprint(form['name'])
		if form.is_valid():
			form.save()
			# History.objects.create(content_object = group, action=2, user=request.user)
			messages.success(request, f"Le group {form.cleaned_data.get('name')} a été modifié")

			return redirect('listGroup')

	context = {
		'form': form,
	}
	return render(request, 'group/update.html', context=context)

@login_required(login_url='login')
@admin_only
def destroy(request, pk):

	group = get_object_or_404(Group, id=pk)
	name = group.name
	group.delete()
	# History.objects.create(content_object = group, action=3, user=request.user)
	messages.success(request, f'Le group {name} a été supprimé.')

	return redirect('listGroup')

# Permissions managment

# user.user_permissions.set([permission_list])
# user.user_permissions.add(permission, permission, ...)
# user.user_permissions.remove(permission, permission, ...)
# user.user_permissions.clear()

@login_required(login_url='login')
@admin_only
def add_permissions(request, group, perm): #perms = list of permissions id
	group = get_object_or_404(Group, id=group)
	perm = Permission.objects.get(id=perm)
	print(perm)
	group.permissions.add(perm)
	# for id in perms:
	# 	perm = Permission.objects.get(id=id)
	# 	group.permissions.add(perm)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
@admin_only
def rmv_permissions(request, group, perm): #perms = list of permissions id
	group = get_object_or_404(Group, id=group)
	perm = Permission.objects.get_object_or_404(id=perm)
	# print(perm)
	group.permissions.remove(perm)
	print(perm)
	# for id in perms:
	# 	perm = Permission.objects.get(id=id)
	# 	group.permissions.remove(perm)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
@admin_only
def clear_permissions(request, group):
	group = get_object_or_404(Group, id=group)
	group.permissions.clear()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
	context = {
		'group':group,
	}
	return render(request, 'group/show.html', context=context)



# Permissions managment

@login_required(login_url='login')
@admin_only
def add_users(request, group, user): #perms = list of permissions id
	user = get_object_or_404(User, id=user)
	print(user)
	group = Group.objects.get(id=group)
	print(group)
	my_group.user_set.add(user)
	# for id in perms:
	# 	perm = Permission.objects.get(id=id)
	# 	group.permissions.add(perm)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))