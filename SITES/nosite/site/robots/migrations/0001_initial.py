# Generated by Django 2.2.3 on 2021-04-12 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('selenium_version', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('chrome_version', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('ip', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('server_name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('server_free_space', models.IntegerField(blank=True, db_index=True, null=True)),
            ],
            options={
                'verbose_name': 'Роботы - Робот',
                'verbose_name_plural': 'Роботы - Роботы',
            },
        ),
    ]
