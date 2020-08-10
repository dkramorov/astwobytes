# Generated by Django 2.2.3 on 2020-08-02 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0023_auto_20200802_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jointwelder',
            name='actually',
            field=models.BooleanField(blank=True, db_index=True, default=False, null=True, verbose_name='Фактический сварщик (тот, кто проводит работы), другие сващики могут быть указаны в заявках, потому что у фактических нет допуска'),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='control_type',
            field=models.IntegerField(blank=True, choices=[(1, 'РК'), (2, 'УЗК'), (3, 'ВИК'), (4, 'РК-УЗК-ЦД'), (5, 'РК-УЗК'), (6, 'УК'), (7, 'ПВК'), (8, 'МК'), (9, 'ВК'), (10, 'СР')], db_index=True, null=True, verbose_name='Вид контроля, например, РК'),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='cutout',
            field=models.BooleanField(blank=True, db_index=True, default=False, null=True, verbose_name='Вырез'),
        ),
    ]
