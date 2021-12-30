from django.shortcuts import render
from django.template import RequestContext

# HTTP Error 400
def bad_request(request, exception): 

	return render(request, 'errors.html', context={'code':'400', 'error': 'Mauvaise Requête'}, status=400)

def permission_denied(request, exception):
	
	return render(request, 'errors.html', context={'code':'403', 'error': 'Accès Non Autorisé'}, status=403)


def page_not_found(request, exception):
	
	return render(request, 'errors.html', context={'code':'404', 'error': 'Page Non Trouvée'}, status=404)


def server_error(request):
	
	return render(request, 'errors.html', context={'code':'500', 'error': 'Erreur Interne du serveur'}, status=500)

