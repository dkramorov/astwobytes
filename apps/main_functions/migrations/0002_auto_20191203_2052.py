# Generated by Django 2.2.3 on 2019-12-03 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_functions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='config',
            options={'verbose_name': 'Админка - Настрока', 'verbose_name_plural': 'Админка - Настройки'},
        ),
        migrations.AlterModelOptions(
            name='tasks',
            options={'verbose_name': 'Админка - Задача', 'verbose_name_plural': 'Админка - Задачи'},
        ),
    ]