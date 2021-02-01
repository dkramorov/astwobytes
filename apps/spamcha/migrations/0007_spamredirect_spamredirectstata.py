# Generated by Django 2.2.3 on 2020-12-08 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spamcha', '0006_auto_20201208_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamRedirect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('our_link', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('ext_link', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Рассылка - Таблица переадресаций',
                'verbose_name_plural': 'Рассылка - Таблица переадресаций',
            },
        ),
        migrations.CreateModel(
            name='SpamRedirectStata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Email получателя')),
                ('client_id', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Ид получателя (для связи с CRM)')),
                ('spam_redirect', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spamcha.SpamRedirect', verbose_name='Переадресация')),
            ],
            options={
                'verbose_name': 'Рассылка - Таблица переадресаций',
                'verbose_name_plural': 'Рассылка - Таблица переадресаций',
            },
        ),
    ]