# Generated by Django 2.2.3 on 2020-02-12 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('freeswitch', '0007_auto_20200206_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personalusers',
            options={'verbose_name': 'Freeswitch - Пользователи сайта', 'verbose_name_plural': 'Freeswtich - Пользователи сайта'},
        ),
        migrations.AddField(
            model_name='fsuser',
            name='personal_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='freeswitch.PersonalUsers'),
        ),
    ]