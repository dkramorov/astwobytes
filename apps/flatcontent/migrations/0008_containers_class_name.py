# Generated by Django 2.2.3 on 2020-06-04 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatcontent', '0007_auto_20200402_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='containers',
            name='class_name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Класс css'),
        ),
    ]
