# Generated by Django 2.2.3 on 2020-01-19 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freeswitch', '0002_redirects_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='redirects',
            old_name='description',
            new_name='desc',
        ),
    ]
