# Generated by Django 2.2.3 on 2020-01-12 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spamcha', '0002_auto_20191203_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailaccount',
            name='img',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='emailblacklist',
            name='img',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='spamrow',
            name='img',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='spamtable',
            name='img',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]
