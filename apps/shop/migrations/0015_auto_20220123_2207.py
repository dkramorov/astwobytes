# Generated by Django 2.2.3 on 2022-01-23 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_ordersdelivery_additional_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersdelivery',
            name='cost',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Цена доставки'),
        ),
        migrations.AlterField(
            model_name='ordersdelivery',
            name='additional_data',
            field=models.TextField(blank=True, null=True, verbose_name='jsonина с доп данными'),
        ),
    ]