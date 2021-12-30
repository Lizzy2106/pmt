from django.shortcuts import render, redirect
from ..models import User
from ..models import UserHasProjet as Team
from ..forms import UserGroupForm
from ..admin import CustomUserCreationForm, UserChangeForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

from django.contrib.auth.models import Group

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from ..decorators import admin_only

from django.db.models import Prefetch

from pprint import pprint

# Users views
@login_required(login_url='login')
@admin_only
def list(request, *args, **kwargs):
	users = User.objects.all().filter(deleted=False).order_by('-date_creation')
	context = {
		'users': users,
	}
	return render(request, 'user/index.html', context=context)

@login_required(login_url='login')
@admin_only
def trash(request, *args, **kwargs):
	users = User.objects.all().filter(deleted=True)
	users.prefetch_related(Prefetch(
		'history', 
		queryset=User.history.order_by('-history_date'),)
	)

	context = {
		'users': users,
		'trash':True,
	}
	return render(request, 'user/index.html', context=context)


def register(request, *args, **kwargs):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CustomUserCreationForm()
		form_groups = UserGroupForm()
		if request.method == 'POST':
			form = CustomUserCreationForm(request.POST)

			if form.is_valid():
				user =  form.save(commit=True)
				id = user.id
				# login(request, user)
				# form.save()
				user = f"{form.cleaned_data.get('email')} {form.cleaned_data.get('password2')}"
				messages.success(request, 'Un compte a été créé pour ' + user)
				# tajinu@mailinator.com

				return redirect('profile', pk=id)
		context = {
			'form': form,
			'form_groups': form_groups,
		}
		return render(request, 'user/register.html', context=context)

def loginUser(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			email = request.POST.get('email')
			password =request.POST.get('password')

			try:
				user = User.objects.get(email=email)
				if check_password(password, user.password):
					if user.is_active:
						login(request, user)
						messages.success(request, f'{user} log')
						return redirect('home')
					else:
						messages.info(request, "Merci d'activer ce compte")
				else:
					messages.error(request, 'Incorrect password')
			#   if user is not None:
			#       print(authenticate(email='cavic@mailinator.com',  password='Pa$$w0rd!'))
			#       user = authenticate(email='cavic@mailinator.com', password='Pa$$w0rd!')
			#       if user is not None:
			#           login(request, user)
			#           return redirect('home')
			#       else:
			#           messages.info(request, 'Incorrect password')
			#   else:
			#       messages.info(request, 'Email does not exist')
			except Exception as e:
				messages.error(request, 'Email does not exist')      
			

		context = {}
		return render(request, 'user/login.html', context)
		
@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def show(request, pk):
	groups = Group.objects.all()
	user = get_object_or_404(User, id=pk)
	form = UserChangeForm(instance=user)
	teams = Team.objects.filter(user=user)
	if request.POST:
		form = UserChangeForm(request.POST or None, instance=user)
		pprint(form.errors.as_data())
		if form.is_valid():
			form.save()
			messages.success(request, f"L'utilisateur {form.cleaned_data.get('nom')} {form.cleaned_data.get('prenom')} a été modifié")

			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		'user':user,
		'groups':groups,
		'teams':teams,
		'form': form,
	}
	return render(request, 'user/profile1.html', context=context)

# def update(request, pk):

#   context = {}
#   return render(request, 'user/update.html', context=context)

@login_required(login_url='login')
@admin_only
def destroy(request, pk):

	user = get_object_or_404(User, id=pk)
	user.deleted = True
	user.save()
	messages.success(request, f"L'utilisateur {user.nom} {user.prenom} a été supprimé.")

	return redirect('userList')


# Groups managment

@login_required(login_url='login')
@admin_only
def add_groups(request, pk):
	user = get_object_or_404(User, id=pk)
	form = UserGroupForm()
	if request.POST:
		form = UserGroupForm(request.POST)
		if form.is_valid():
			user.groups.clear()
			groups = form.cleaned_data['groups']
			print(groups)
			for group in groups:
				group.user_set.add(user)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))