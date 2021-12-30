from django import template
from django.contrib.auth.models import Group 

register = template.Library() 


@register.filter(name='isinstance') 
def isinstance(object, classe):
	if object.__class__.__name__ == classe.title():
		return True
	elif classe=='team' and type(object)=='UserHasProjet':
		return True
	else:
		return False


@register.filter(name='isHistoryinstance') 
def isHistoryinstance(object, classe):
	if object.__class__.__name__ == f'Historical{classe.title()}':
		return True
	elif classe=='team' and object.__class__.__name__=='HistoricalUserHasProjet':
		return True
	else:
		return False

@register.filter
def classname(obj):
	return obj.__class__.__name__