# Generated by Django 2.2.3 on 2021-02-08 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20210208_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='external_number',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Внешний номер заказа от платежной системы'),
        ),
    ]