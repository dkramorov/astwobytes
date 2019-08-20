from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import migrations


def create_superuser(apps, schema_editor):
    superuser = User()
    superuser.is_active = True
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.username = 'jocker'
    superuser.email = 'dkramorov@mail.ru'
    superuser.set_password('reabhxbr')
    superuser.save()


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
