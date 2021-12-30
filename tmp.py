# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PjmanagerHistoricalprojet(models.Model):
    id = models.IntegerField()
    titre = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_creation = models.DateTimeField()
    date_debut = models.DateTimeField(blank=True, null=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    estvalide = models.IntegerField()
    estsatisfaisant = models.IntegerField()
    statut = models.IntegerField()
    deleted = models.IntegerField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjmanager_historicalprojet'


class PjmanagerHistoricaltype(models.Model):
    id = models.IntegerField()
    libelle = models.CharField(max_length=45)
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjmanager_historicaltype'


class PjmanagerHistoricaluser(models.Model):
    id = models.IntegerField()
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    email = models.CharField(max_length=254)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=255)
    date_naiss = models.DateTimeField(blank=True, null=True)
    sexe = models.PositiveSmallIntegerField()
    telephone = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    deleted = models.IntegerField()
    date_creation = models.DateTimeField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjmanager_historicaluser'


class PjmanagerHistoricaluserhasprojet(models.Model):
    id = models.IntegerField()
    user_role = models.PositiveSmallIntegerField(blank=True, null=True)
    user_statut = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    projet_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjmanager_historicaluserhasprojet'


class Projet(models.Model):
    titre = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_creation = models.DateTimeField()
    date_debut = models.DateTimeField(blank=True, null=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    estvalide = models.IntegerField()
    estsatisfaisant = models.IntegerField()
    type = models.ForeignKey('Type', models.DO_NOTHING, blank=True, null=True)
    statut = models.IntegerField()
    deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'projet'


class Type(models.Model):
    libelle = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'type'


class User(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    email = models.CharField(unique=True, max_length=254)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=255)
    date_naiss = models.DateTimeField(blank=True, null=True)
    sexe = models.PositiveSmallIntegerField()
    telephone = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_creation = models.DateTimeField()
    deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'


class UserGroups(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_groups'
        unique_together = (('user', 'group'),)


class UserHasProjet(models.Model):
    user_role = models.PositiveSmallIntegerField(blank=True, null=True)
    user_statut = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField()
    projet = models.ForeignKey(Projet, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_has_projet'
        unique_together = (('projet', 'user'),)


class UserUserPermissions(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_user_permissions'
        unique_together = (('user', 'permission'),)
