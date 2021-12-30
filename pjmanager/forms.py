from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import *

class UserForm(UserCreationForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'nom', 'prenom', 'sexe',)

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user
	
	# def clean_password(self):
	# 	password = self.cleaned_data.get('password1')
	# 	password1 = self.cleaned_data.get('password2')

	# 	if password1 and password2 and password1 != password2:
	# 		raise forms.ValidationError('Passwords don\'t match')
	# 	return password2

	# def save(self, commit=True):
	# 	user = super(UserForm, self).save(commit=False)
		
	# 	if commit:
	# 		user.set_password(self.cleaned_data['password2'])
	# 		user.save()
	# 	return user

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows':'2'}),
        }

class UserGroupForm(forms.ModelForm):
	groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=True)
	class Meta(object):
		model = User
		fields = ('groups',)

class LoginForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta(object):
		model = User
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']

class TypeForm(forms.ModelForm):
	class Meta():
		model = Type
		fields = ['libelle',]
			
class ProjetForm(forms.ModelForm):
	dte_deb = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=False)
	dte_fin = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=False)
	class Meta():
		model = Projet
		fields = '__all__'
		exclude = ['date_creation', 'date_debut', 'date_fin']


class TeamForm(forms.ModelForm):
	class Meta():
		model = UserHasProjet
		fields = '__all__'

class AddUserProjectForm(forms.ModelForm):
	class Meta():
		model = UserHasProjet
		fields = ['user', 'user_role']