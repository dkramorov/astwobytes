# Generated by Django 2.2.3 on 2020-05-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_property_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='measure',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Единица измерения'),
        ),
    ]
