from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Projet
from ..models import UserHasProjet as Team
from ..forms import TeamForm, AddUserProjectForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from ..decorators import admin_only
@login_required(login_url='login')
# UserHasProjets views
def list(request, *args, **kwargs):
	teams = Team.objects.all()
	context = {
		'teams':teams
	}
	return render(request, 'team/index.html', context=context)

@login_required(login_url='login')
@admin_only
def create(request, *args, **kwargs):
	form = TeamForm()
	if request.POST:
		form = TeamForm(request.POST)
		if form.is_valid():
			new = form.save(commit=False)
			if (not new.projet.deleted and not new.user.deleted):
				new.save()
				# History.objects.create(content_object = new.projet, action=2, user=request.user)
				messages.success(request, f"Un nouvel élément a été enreigistré")

				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		'form': form,
	}
	return render(request, 'team/create.html', context=context)

@login_required(login_url='login')
@admin_only
def add_user(request, pk):
	form = AddUserProjectForm()
	if request.POST:
		form = AddUserProjectForm(request.POST)
		if form.is_valid():
			team = form.save(commit=False)
			team.projet = get_object_or_404(Projet, id=pk)
			# print(form)
			# print(form.cleaned_data.get('user_role'))
			team.user_role = form.cleaned_data.get('user_role')
			if (not team.projet.deleted and not team.user.deleted):
				team.save()
				# History.objects.create(content_object = team.projet, action=2, user=request.user)
				messages.success(request, f"Un nouvel élément a été enreigistré")

			next = request.POST.get('next', '/')
			return HttpResponseRedirect(next)

	context = {
		'form': form,
	}
	return render(request, 'team/create.html', context=context)

@login_required(login_url='login')
def show(request, pk):
	team = get_object_or_404(Team, id=pk)
	
	context = {
		'team':team,
	}
	return render(request, 'team/show.html', context=context)

@login_required(login_url='login')
@admin_only
def update(request, pk):
	team = get_object_or_404(Team, id=pk)
	form = TeamForm(instance=team)
	if request.POST:
		form = TeamForm(request.POST or None, instance=team)
		if form.is_valid():
			team = form.save()
			# History.objects.create(content_object = team.projet, action=2, user=request.user)
			messages.success(request, f"Un élément a été modifié")

			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		'form': form,
	}
	return render(request, 'team/update.html', context=context)

@login_required(login_url='login')
@admin_only
def destroy(request, pk):

	team = get_object_or_404(Team, id=pk)
	user = team.user
	projet = team.projet
	# History.objects.create(content_object = projet, action=2, user=request.user)
	team.delete()
	messages.success(request, f'{user} a été supprimé du projet {projet}.')

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))