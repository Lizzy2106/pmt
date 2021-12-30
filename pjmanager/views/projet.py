from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Projet, Type, User
from ..models import UserHasProjet as Team

from ..forms import ProjetForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from ..decorators import admin_only

# Types views
@login_required(login_url='login')
def list(request, *args, **kwargs):
	projets = Projet.objects.all().filter(deleted=False)
	context = {
		'projets': projets,
	}
	return render(request, 'projet/index.html', context=context)

@login_required(login_url='login')
@admin_only
def trash(request, *args, **kwargs):
	projets = Projet.objects.all().filter(deleted=True)
	context = {
		'projets': projets,
		'trash':True,
	}
	return render(request, 'projet/index.html', context=context)

@login_required(login_url='login')
@admin_only
def trash(request, *args, **kwargs):
	projets = Projet.objects.all().filter(deleted=True)
	print(projets)
	context = {
		'trash':True,
		'projets': projets,
	}
	return render(request, 'projet/index.html', context=context)

@login_required(login_url='login')
@admin_only
def create(request, *args, **kwargs):
	types  = Type.objects.all().filter(deleted=False)
	form = ProjetForm()
	if request.POST:
		form = ProjetForm(request.POST)
		if form.is_valid():
			new = form.save(commit=False)
			new.date_debut=form.cleaned_data['dte_deb']
			new.date_fin=form.cleaned_data['dte_fin']
			if new.date_debut<=new.date_fin:
				new.save()
				# History.objects.create(content_object = projet, action=2, user=request.user)
				messages.success(request, f"Le projet {form.cleaned_data.get('titre')} a été modifié")

				return redirect('showProjet', pk=new.id)
			else:
				form.add_error('dte_fin', 'Date de fin du projet inférieure à la date de début')

	context = {
		'form': form,
		'types':types,
	}
	return render(request, 'projet/create.html', context=context)

@login_required(login_url='login')
def show(request, pk):
	projet = get_object_or_404(Projet, id=pk)
	team   = Team.objects.filter(projet=projet)
	types  = Type.objects.all().filter(deleted=False)
	users  = User.objects.all().filter(deleted=False).exclude(id__in=[t.user.id for t in team.filter(projet__deleted=False)])
	form = ProjetForm(instance=projet)

	context = {
		'projet':projet,
		'team':team,
		'types':types,
		'users':users,
		'form': form,
	}
	return render(request, 'projet/show.html', context=context)

@login_required(login_url='login')
@admin_only
def update(request, pk):
	projet = get_object_or_404(Projet, id=pk)
	form = ProjetForm(instance=projet)
	if request.POST:
		form = ProjetForm(request.POST or None, instance=projet)
		if form.is_valid():
			projet = form.save(commit=False)
			projet.date_debut=form.cleaned_data['dte_deb']
			projet.date_fin=form.cleaned_data['dte_fin']
			if projet.date_debut<=projet.date_fin:
				projet.save()
				# History.objects.create(content_object = projet, action=2, user=request.user)
				messages.success(request, f"Le projet {form.cleaned_data.get('titre')} a été modifié")

				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
			else:
				form.add_error('dte_fin', 'Date de fin du projet inférieure à la date de début')
				team   = Team.objects.filter(projet=projet)
				types  = Type.objects.all().filter(deleted=False)
				users  = User.objects.all().filter(deleted=False).exclude(id__in=[t.user.id for t in team.filter(projet__deleted=False)])
				
				context = {
					'projet':projet,
					'team':team,
					'types':types,
					'users':users,
					'form': form,
				}
				return render(request, 'projet/show.html', context=context)		

	context = {
		'form': form,
	}
	return redirect('showProjet', pk=projet.id)

@login_required(login_url='login')
@admin_only
def destroy(request, pk):

	projet = get_object_or_404(Projet, id=pk)
	projet.delete()
	# projet.deleted=True
	# projet.save()
	# projet.history.all().first().history_type = '-'
	# print(projet.history.all().first().history_type)
	# History.objects.create(content_object = projet, action=3, user=request.user)
	messages.success(request, f'Le projet {projet.titre} a été supprimé.')

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))