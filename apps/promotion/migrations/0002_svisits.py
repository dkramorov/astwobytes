# Generated by Django 2.2.3 on 2020-05-06 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SVisits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('date', models.DateField(blank=True, db_index=True, null=True)),
                ('company_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('profile', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, db_index=True, null=True)),
            ],
            options={
                'verbose_name': 'Promotion - посещение сайта',
                'verbose_name_plural': 'Promotion - посещения сайтов',
            },
        ),
    ]
