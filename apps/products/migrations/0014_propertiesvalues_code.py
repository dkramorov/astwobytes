# Generated by Django 2.2.3 on 2021-12-25 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_property_search_facet'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertiesvalues',
            name='code',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]