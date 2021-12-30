# Generated by Django 3.1.7 on 2021-04-08 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pjmanager', '0014_historicalprojet_historicaltype_historicaluser_historicaluserhasprojet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhasprojet',
            name='projet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pjmanager.projet'),
        ),
        migrations.AlterField(
            model_name='userhasprojet',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
