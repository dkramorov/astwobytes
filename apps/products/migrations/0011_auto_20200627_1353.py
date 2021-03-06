# Generated by Django 2.2.3 on 2020-06-27 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20200623_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='max_price',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=13, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='min_price',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=13, null=True),
        ),
    ]
