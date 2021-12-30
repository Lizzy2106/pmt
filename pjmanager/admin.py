from .models import *
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from simple_history.admin import SimpleHistoryAdmin


class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
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


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'nom', 'prenom', 'date_naiss', 'adresse', 'telephone')

class UserAdmin(BaseUserAdmin):
	
	ordering = ('-date_creation',)
	search_fields = (
		'email',
		'nom',
		'prenom',
		'sexe',
		'deleted',
	)
	list_filter = (
		'sexe',
		'deleted',
		'date_creation',
		'is_staff',
		'is_active',
		'is_superuser',
	)
	list_display = (
		'email',
		'nom',
		'prenom',
		'date_naiss',
		'sexe',
		'telephone',
		'adresse',
		'last_login',
		# 'date_creation',
		'deleted',
		'is_staff',
		'is_active',
	)
	fieldsets = (
		(None, {
			'fields': (
				'email',
				'nom',
				'prenom',
				'last_login',
			)
		}),
		('Personnel', {
			'fields': (
				'date_naiss',
				'sexe',
				'telephone',
				'adresse',
				'password',
			)
		}),
		('Rôles et Permissions', {
			'fields': (
				'is_staff',
				'is_active',
				'deleted',
				'groups',
			)
		}),
	)
	add_fieldsets= (
		(None, {
			'fields': (
				'email',
				'nom',
				'prenom',
				'password1',
				'password2'
			)
		}),
		('Personnel', {
			'fields': (
				'date_naiss',
				'sexe',
				'telephone',
				'adresse',
			)
		}),
		('Rôles et Permissions', {
			'fields': (
				'is_staff',
				# 'is_active',
				'groups',
			)
		}),
	)


class PollHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "titre", "statut"]
    history_list_display = ["statut"]
    search_fields = ['titre', 'user__nom']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Type, SimpleHistoryAdmin)
admin.site.register(Projet, SimpleHistoryAdmin)
# admin.site.register(UserRole)
admin.site.register(UserHasProjet, SimpleHistoryAdmin)
# admin.site.register(History)
# admin.site.unregister(Group)