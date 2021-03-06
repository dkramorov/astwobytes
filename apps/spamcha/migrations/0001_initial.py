# Generated by Django 2.2.3 on 2019-09-07 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(blank=True, db_index=True, default=True, null=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('passwd', models.CharField(blank=True, max_length=255, null=True)),
                ('smtp_server', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('smtp_port', models.IntegerField(blank=True, db_index=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailBlackList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(blank=True, db_index=True, default=True, null=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('reason', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpamTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(blank=True, db_index=True, default=True, null=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('tag', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('msg', models.TextField(blank=True, null=True, verbose_name='Сообщение для отправки')),
                ('html_msg', models.TextField(blank=True, null=True, verbose_name='Сообщение, созданное в конструкторе')),
                ('reply_to', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Адрес для ответа')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpamRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(blank=True, db_index=True, default=True, null=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('dest', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Получатель')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spamcha.EmailAccount')),
                ('spam_table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spamcha.SpamTable')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
