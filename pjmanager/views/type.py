from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Type, Projet
from ..forms import TypeForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from ..decorators import admin_only
# Types views
@login_required(login_url='login')
@admin_only
def list(request, *args, **kwargs):
	types = Type.objects.all().filter(deleted=False)
	projets = Projet.objects.all()

	context = {
		'types': types,
		'projets':projets,
	}
	return render(request, 'type/index.html', context=context)


@login_required(login_url='login')
@admin_only
def trash(request, *args, **kwargs):
	types   = Type.objects.all().filter(deleted=True)
	projets = Projet.objects.all()
	context = {
		'types': types,
		'projets': projets,
		'trash':True,
	}
	return render(request, 'type/trash.html', context=context)

@login_required(login_url='login')
@admin_only
def create(request, *args, **kwargs):
	form = TypeForm()
	if request.POST:
		form = TypeForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			type = f"{form.cleaned_data.get('libelle')}"
			messages.success(request, 'Un nouveau type de projet a été enreigistré ' + type)

			return redirect('listType')

	context = {
		'form': form,
	}
	return render(request, 'type/create.html', context=context)

@login_required(login_url='login')
def show(request, pk):
	type = get_object_or_404(Type, id=pk)
	
	context = {
		'type':type,
	}

	return render(request, 'type/show.html', context=context)

@login_required(login_url='login')
@admin_only
def update(request, pk):
	type = get_object_or_404(Type, id=pk)
	if request.POST:
		form = TypeForm(request.POST, instance=type)
		print(form)
		if form.is_valid():
			form.save(commit=True)
			messages.success(request, f"Le type de projet {form.cleaned_data.get('libelle')} a été modifé")
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			messages.info(request,'Entrer un libelle valide')

	form = TypeForm(instance=type)
	context = {
		'type':type,
		'form': form,
	}
	return render(request, 'type/update.html', context=context)

@login_required(login_url='login')
@admin_only
def destroy(request, pk):
	type = get_object_or_404(Type, id=pk)
	libelle = type.libelle
	type.deleted=True
	type.save()
	messages.success(request, f'Le type de projet {libelle} a été supprimé.')

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
