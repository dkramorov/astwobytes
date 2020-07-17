# Generated by Django 2.2.3 on 2020-07-13 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('field', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('show_in_table', models.BooleanField(blank=True, db_index=True, default=False, null=True, verbose_name='Показывать в таблице принудительно')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExtraValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('field', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExtraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='login.ExtraFields')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
