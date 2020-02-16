# Generated by Django 2.2.3 on 2020-02-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Daemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(blank=True, db_index=True, default=True, null=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('token', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('exec_path', models.CharField(blank=True, choices=[('binary_bot/binary_bot.py', 'Бинарные опционы')], db_index=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Сервисы - Демон',
                'verbose_name_plural': 'Сервисы - Демон',
            },
        ),
    ]