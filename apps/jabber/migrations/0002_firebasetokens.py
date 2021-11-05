# Generated by Django 2.2.3 on 2021-07-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jabber', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirebaseTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('login', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Логин (телефон) пользователя')),
                ('token', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Токен приложения пользователя')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
