from django.shortcuts import render, redirect
from django.apps import apps
from pprint import pprint
from ..models import *

from django.shortcuts import get_list_or_404, get_object_or_404

from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.db import models

from operator import itemgetter

def home(request, *args, **kwargs):
	context = {
	}
	return render(request, 'site/index.html', context=context)

def search(request, *args, **kwargs):
	search_query = request.GET.get('search')

	str_models = ['Projet', 'Type', 'User', 'UserHasProjet']
	search_models = [apps.get_model('pjmanager', model) for model in str_models] # Add your models here, in any way you find best.
	
	search_results = []
	for model in search_models:
		fields = [x for x in model._meta.fields if isinstance(x, models.CharField)]
		search_queries = [models.Q(**{x.name + "__contains" : search_query}) for x in fields]
		q_object = models.Q()
		for query in search_queries:
			q_object = q_object | query

	results = model.objects.filter(q_object)
	search_results.append(results)

	context = {
		'results': search_results,
	}
	return render(request, 'old/search.html', context=context)

def history(request, *args, **kwargs):
	history = History.objects.all().order_by('-history_date')

	historyDict        = {}
	i=0
	for h in history:
		current_model  = apps.get_model('pjmanager', get_historical_class(h.object))
		tmp = {
			'id':h.history_id,
			'classe':h.object,
			'date':h.history_date,
			'type':h.get_history_type_display,
			'objet':get_historical_object_display(current_model.history.get(history_id=h.history_id))
		}
		i+=1
		historyDict[i] = tmp
	# 	print(i)
	# 	current_model  = apps.get_model('pjmanager', get_historical_class(h.object))
	# 	print(current_model)
	# 	historyDict[h] = get_historical_object_display(current_model.history.get(history_id=h.history_id))
	# 	print(historyDict[h])
	# 	i+=1
	# 	print(historyDict.__len__())
	# print(historyDict)
	historyList = []
	for key, value in historyDict.items():
		tmp     = [key,value]
		historyList.append(tmp)

	paginator   = Paginator(historyList, 4)

	page_number = request.GET.get('page')

	page_obj    = paginator.get_page(page_number)
	
	context = {
		'history': page_obj,
	}
	return render(request, 'site/history.html', context=context)

def obj_history(request, classe, pk): #pk => object id
	
	current_model  = apps.get_model('pjmanager', get_historical_class(classe))
	title = f'{classe.title()} n° {pk}'

	try:
		object = current_model.objects.get(id=pk)
	except:
		return render(request, 'old/404.html', {}, status=400)
	
	history = object.history.all().order_by('-history_date')
	histories = []
	for h in history:
		if hasattr(h, 'deleted'):
			if h.prev_record==None:
				h.history_type = 'Ajouté'
			elif h.deleted:
				h.history_type = 'Supprimé'
			elif h.prev_record.deleted:
				h.history_type = 'Actualisé'
			else:
				h.history_type = get_historical_type_display(h.history_type)
		else:
			h.history_type = get_historical_type_display(h.history_type)
		histories.append(h)
		
	
	if classe=='projet':
		# for uhp in list(UserHasProjet.history.filter(projet=pk).order_by('-history_date').values()):
		# 	history.append(uhp)
		# history = sorted(history, key=itemgetter('history_date'), reverse=True)
		for team in UserHasProjet.history.filter(projet=pk).order_by('-history_date') :
			team.history_type = f'{team.user} {get_team_historical_type_display(team.history_type)}'
			for i in range(len(histories)):
				if team.history_date>=histories[i].history_date:
					histories.insert(i, team)
					break
				else:
					i=i+1
			# histories.append(team)
		# histories = sorted(histories, key=itemgetter('history_date'), reverse=True)

	elif classe=='user':
		for team in UserHasProjet.history.filter(user=pk).order_by('-history_date') :
			team.history_type = f'{get_team_historical_type_display(team.history_type)} {team.projet}'
			for i in range(len(histories)):
				if team.history_date>=histories[i].history_date:
					histories.insert(i, team)
					break
				else:
					i=i+1
	

	context = {
		'classe': classe,
		'history': histories,
		'title': title,
	}
	return render(request, 'site/obj_history.html', context=context)

def one_history(request, classe, pk):#pk => history id
	
	current_model  = apps.get_model('pjmanager', get_historical_class(classe))
	
	history        = current_model.history.get(history_id=pk)
	
	try:
		object = current_model.objects.get(id=history.id)
	except:
		return render(request, 'old/404.html', {}, status=400)

	attributes =[] #current object' values
	value, old = {}, {}
	
	if get_historical_class(classe)=="UserHasProjet":
		context = get_team_history_attr_val_old(object, history)
	
	elif get_historical_class(classe)=="Projet":
		context = get_projet_history_attr_val_old(object, history)
	
	elif get_historical_class(classe)=="Type":
		context = get_type_history_attr_val_old(object, history)
	
	elif get_historical_class(classe)=="User":
		context = get_user_history_attr_val_old(object, history)

	else:
		for n,v in vars(object).items():
			attributes.append(n)
			value[n]=v
	
		for a in attributes:
			old[a]=getattr(history, a)

		pprint(old)
		context = {
			'date': history.history_date,
			'attributes': attributes,
			'value': value,
			'old': old,
		}
	return render(request, 'site/one_history.html', context=context)

def error_404(request, exception):
		data = {}
		return render(request,'old/404.html', data)


# UTILS
def get_historical_class(obj):
	switcher = {
		'projet': 'Projet',
		'type'  : 'Type',
		'user'  : 'User',
		'team'  : 'UserHasProjet',
	}
	return switcher.get(obj)

def get_team_historical_type_display(type):
	switcher = {
		'+' : 'Ajouté au projet',
		'-' : 'Retiré du projet',
		'~' : 'Modifé sur le projet',
	}
	return switcher.get(type)

def get_historical_type_display(type):
	switcher = {
		'+' : 'Ajouté',
		'-' : 'Supprimé',
		'~' : 'Modifé',
	}
	return switcher.get(type)

def get_historical_object_display(obj):

	try:
		if isinstance(obj, type(None)):
			return obj
		elif hasattr(obj, 'projet') and hasattr(obj, 'user'):
			return {
				'user':obj.user,
				'projet':obj.projet,
				'type': get_team_historical_type_display(obj.history_type)
			}
		elif hasattr(obj, 'nom'):
			return obj.nom
		elif hasattr(obj, 'titre'):
			return obj.titre
		elif hasattr(obj, 'libelle'):
			return obj.libelle
		else:
			return obj
	except:
		return obj


def get_projet_history_attr_val_old(object, history):
	attributes = [
		'Titre',
		'Description',
		'Date de creation',
		'Date de debut',
		'Date de fin',
		'Valide',
		'Satisfaisant',
		'Type',
		'Statut',
		'Delete'
	]
	delete = False
	action = get_historical_type_display(history.history_type)
	new, old, results = {}, {}, {}
	
	# History value
	old['Titre'] = history.titre
	old['Description'] = history.description
	old['Date de creation'] = history.date_creation
	old['Date de debut'] = history.date_debut
	old['Date de fin'] = history.date_fin
	old['Type'] = history.type
	old['Delete'] = history.deleted

	if(history.estvalide):
		old['Valide'] = 'Oui'
	else:
		old['Valide'] = 'Non'
	
	if(history.estsatisfaisant):
		old['Satisfaisant'] = 'Oui'
	else:
		old['Satisfaisant'] = 'Non'

	if(history.statut):
		old['Statut'] = 'Fini'
	else:
		old['Statut'] = 'En cours'

	if history.history_type == '+' or history.history_type == '-':
		update = False
	
	elif history.history_type=='~':

		if history.deleted:
			update = False
			delete = True
			action = 'Supprimé'
		elif history.prev_record.deleted:
			update = False
			action = 'Actualisé'
		else:
			update = True
			# Current obj values
			new['Titre'] = object.titre
			new['Description'] = object.description
			new['Date de creation'] = object.date_creation
			new['Date de debut'] = object.date_debut
			new['Date de fin'] = object.date_fin	
			new['Type'] = object.type
			new['Delete'] = object.deleted
			
			if(object.estvalide):
				new['Valide'] = 'Oui'
			else:
				new['Valide'] = 'Non'
			
			if(object.estsatisfaisant):
				new['Satisfaisant'] = 'Oui'
			else:
				new['Satisfaisant'] = 'Non'

			if(object.statut):
				new['Statut'] = 'Fini'
			else:
				new['Statut'] = 'En cours'

	results = {
		'attributes': attributes,
		'delete':delete,
		'update':update,
		'value':new,
		'old':old,
		'date':history.history_date,
		'action': action,
	}
	return results

def get_type_history_attr_val_old(object, history):
	new, old, results = {}, {}, {}
	delete = False
	action = get_historical_type_display(history.history_type)
	attributes = [
		'Libelle'
	]

	old['Libelle']   = history.libelle

	if history.history_type == '+' or history.history_type == '-':
		update = False
	
	elif history.history_type=='~':

		if history.deleted:
			update = False
			delete = True
			action = 'Supprimé'
		elif history.prev_record.deleted:
			update = False
			action = 'Actualisé'

		else:
			update = True
			new['Libelle']   = object.libelle
	
	results = {
		'attributes': attributes,
		'update':update,
		'value':new,
		'old':old,
		'date':history.history_date,
		'delete':delete,
		'action': action,
	}
	return results


def get_user_history_attr_val_old(object, history):
	attributes = [
		'Email',
		'Nom',
		'Prenom',
		'Date de naissance',
		'Sexe',
		'Telephone',
		'Adresse',
		'Staff',
		'Active',
		'Date de creation',
	]
	delete = False
	action = get_historical_type_display(history.history_type)
	new, old, results = {}, {}, {}

	old['Email'] = history.email
	old['Nom'] = history.nom
	old['Prenom'] = history.prenom
	old['Date de naissance'] = history.date_naiss
	old['Sexe'] = history.get_sexe_display()
	old['Telephone'] = history.telephone
	old['Adresse'] = history.adresse
	old['Date de creation'] = history.date_creation

	if(history.is_staff):
		old['Staff'] = 'Oui'
	else:
		old['Staff'] = 'Non'
	
	if(history.is_active):
		old['Active'] = 'Oui'
	else:
		old['Active'] = 'Non'

	if history.history_type == '+' or history.history_type == '-':
		update = False
	
	elif history.history_type=='~':

		if history.deleted:
			update = False
			delete = True
			action = 'Supprimé'
		elif history.prev_record.deleted:
			update = False
			action = 'Actualisé'
		else:
			update = True

			new['Email'] = object.email
			new['Nom'] = object.nom
			new['Prenom'] = object.prenom
			new['Date de naissance'] = object.date_naiss
			new['Sexe'] = object.get_sexe_display()
			new['Telephone'] = object.telephone
			new['Adresse'] = object.adresse
			new['Date de creation'] = object.date_creation

			if(object.is_staff):
				new['Staff'] = 'Oui'
			else:
				new['Staff'] = 'Non'
			
			if(object.is_active):
				new['Active'] = 'Oui'
			else:
				new['Active'] = 'Non'
			

	results = {
		'attributes': attributes,
		'update':update,
		'value':new,
		'old':old,
		'date':history.history_date,
		'delete':delete,
		'action': action,
	}
	return results

def get_team_history_attr_val_old(object, history):
	attributes = [
		'Utilisateur',
		'Projet',
		'Role',
		'Statut'
	]
	delete = False
	action = get_historical_type_display(history.history_type)
	new, old, results = {}, {}, {}
	
	old['Utilisateur']   = history.user
	old['Projet'] = history.projet
	old['Role']   = history.get_user_role_display()
	old['Statut'] = history.get_user_statut_display()
	
	if history.history_type == '+' or history.history_type == '-':
		update = False
	
	elif history.history_type=='~':
		if history.deleted:
			update = False
			delete = True
			action = 'Supprimé'
		elif history.prev_record.deleted:
			update = False
			action = 'Actualisé'
		else:
			update = True
			new['Utilisateur']   = object.user
			new['Projet'] = object.projet
			new['Role']   = object.get_user_role_display()
			new['Statut'] = object.get_user_statut_display()


	results = {
		'attributes': attributes,
		'update':update,
		'value':new,
		'old':old,
		'date':history.history_date,
		'delete':delete,
		'action': action,
	}
	return results
