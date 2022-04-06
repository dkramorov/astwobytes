# Generated by Django 2.2.3 on 2022-03-01 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polis', '0002_auto_20220225_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='polis',
            name='ptype',
            field=models.IntegerField(blank=True, choices=[(1, 'Хоккей'), (2, 'Круиз')], db_index=True, null=True, verbose_name='Тип полиса (для формы)'),
        ),
    ]
