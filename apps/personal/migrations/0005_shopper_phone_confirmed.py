# Generated by Django 2.2.3 on 2021-03-26 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0004_shopper_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopper',
            name='phone_confirmed',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Телефон подтвержден'),
        ),
    ]
