from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from simple_history.models import HistoricalRecords


# class Role(models.Model):
#   '''
#   Les rôles sont prédéfinis.
#   '''
#       DG = 1
#       COMPTABLE = 2
#       EMPLOYE = 3
#       STAGIAIRE = 4
#   ROLE_CHOICES = (
#       (Dg, 'DG'),
#       (Comptable, 'comptable'),
#       (Employe, 'employe'),
#       (Stagiaire, 'stagiaire'),
#   )
#   id          = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
#   libelle     = models.CharField(max_length=45)
#   description = models.CharField(max_length=255, blank=True, null=True)
    
#   def __str__(self):
#       return self.get_id_display()

class UserManager(BaseUserManager):
    def create_user(self,email, nom, prenom, sexe, password, **extra_fields):

        if not email:
            raise ValueError(_('Veillez entrer votre adresse mail'))
        
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, nom=nom, prenom=prenom, sexe=sexe, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, nom, prenom, sexe, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True.'))

        return self.create_user(email, nom, prenom, sexe, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    FEM = 1
    MAS = 2
    SEXE_CHOICES = [
        (FEM, 'Feminin'),
        (MAS, 'Masculin'),
    ]

    email         = models.EmailField(_('adresse email'), unique=True)
    nom           = models.CharField(max_length=150)
    prenom        = models.CharField(max_length=255)
    date_naiss    = models.DateTimeField(blank=True, null=True)
    sexe          = models.PositiveSmallIntegerField(choices=SEXE_CHOICES)
    telephone     = models.CharField(max_length=255)
    adresse       = models.CharField(max_length=255, blank=True, null=True)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True) #we can send a email for account validation(optional)
    deleted       = models.BooleanField(default=False)
    date_creation = models.DateTimeField(default=timezone.now)
    history       = HistoricalRecords(related_name='log')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'sexe']

    def __str__(self):
        return  f'{self.nom} {self.prenom}' 

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_staff

    class Meta:
        managed = True
        db_table = 'user'


class Type(models.Model): #type of project
    # id = models.IntegerField(primary_key=True)
    libelle = models.CharField(max_length=45, unique=True)
    history = HistoricalRecords(related_name='log')
    deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'type'

    def __str__(self):
        return f'{self.libelle}'


class Projet(models.Model):
    titre           = models.CharField(max_length=150)
    description     = models.CharField(max_length=255, blank=True, null=True)
    date_creation   = models.DateTimeField(auto_now_add=True)
    date_debut      = models.DateTimeField(blank=True, null=True)
    date_fin        = models.DateTimeField(blank=True, null=True)
    estvalide       = models.BooleanField(default=False)  # Field name made lowercase.
    estsatisfaisant = models.BooleanField(default=False)  # Field name made lowercase.
    type            = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True)
    statut          = models.BooleanField(default=False)  # Field name made lowercase.
    deleted         = models.BooleanField(default=False)
    history         = HistoricalRecords(related_name='log')


    class Meta:
        managed = True
        db_table = 'projet'

    def delete(self):
        self.deleted = True
        self.save()
        # self.history.first().history_type = '-'

    def __str__(self):
        return f'{self.titre}'


# class UserRole(models.Model):
#   '''
#   Les rôles sont prédéfinis.
#   '''
#   DEVELOPPEUR = 1
#   DESIGNER    = 2
#   ROLE_CHOICES = (
#       (DEVELOPPEUR, 'Developpeur'),
#       (DESIGNER, 'Designer'),
#   )
#   id          = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
#   libelle     = models.CharField(max_length=45)
#   description = models.CharField(max_length=255, blank=True, null=True)
    
#   class Meta:
#       managed = True
#       db_table = 'user_role'

#   def __str__(self):
#       return self.get_id_display()

class UserHasProjet(models.Model):
    '''
    Les rôles sont prédéfinis.
    '''
    RESPONSABLE = 1
    PARTICIPANT = 2
    SUPERVISEUR = 3
    STATUT_CHOICES = (
        (RESPONSABLE, 'Responsable'),
        (PARTICIPANT, 'Participant'),
        (SUPERVISEUR, 'Superviseur'),
    )

    DEVELOPPEUR = 1
    DESIGNER    = 2
    ROLE_CHOICES = (
        (DEVELOPPEUR, 'Developpeur'),
        (DESIGNER, 'Designer'),
    )

    projet      = models.ForeignKey(Projet, on_delete=models.DO_NOTHING, null=True)  # Field name made lowercase.
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    user_role   = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    user_statut = models.PositiveSmallIntegerField(choices=STATUT_CHOICES, default=2)
    # created_at  = models.DateTimeField(auto_now_add=True)
    created_at  = models.DateTimeField(default=timezone.now)
    history     = HistoricalRecords(related_name='log')

    class Meta:
        managed = True
        db_table = 'user_has_projet'
        unique_together = (('projet', 'user'),)
    
    def __str__(self):
        return f'{self.user} travaille sur {self.projet.titre}'


class History(object):
    CREATED = 1
    CHANGED = 2
    DELETED = 3
    ACTION_CHOICES = (
        (CREATED, 'Créé'),
        (CHANGED, 'Modifié'),
        (DELETED, 'Supprimé'),
    )
    content_type   = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id      = models.PositiveIntegerField()
    user           = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date           = models.DateTimeField(auto_now_add=True)
    action         = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)

class History(models.Model):
    CREATED = '+'
    CHANGED = '~'
    DELETED = '-'
    ACTION_CHOICES = (
        (CREATED, 'Créé'),
        (CHANGED, 'Modifié'),
        (DELETED, 'Supprimé'),
    )
    history_id      = models.IntegerField(primary_key=True) #id dans la table pjmanager_historicaltable
    history_date    = models.DateTimeField() #date modif
    history_user_id = models.IntegerField() #utilisateur ayant effectué la modif
    history_type    = models.CharField(max_length=1, choices=ACTION_CHOICES) #type de la modif
    object          = models.CharField(max_length=6) #nom de l'objet

    class Meta:
        managed = False
        db_table = "history"