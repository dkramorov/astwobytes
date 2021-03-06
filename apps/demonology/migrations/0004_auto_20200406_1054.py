# Generated by Django 2.2.3 on 2020-04-06 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demonology', '0003_auto_20200406_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='timetable',
        ),
        migrations.AddField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Завершение события'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='demonology.Event'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Начало события'),
        ),
    ]
