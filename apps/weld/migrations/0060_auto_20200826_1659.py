# Generated by Django 2.2.3 on 2020-08-26 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0059_auto_20200825_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='jointconclusion',
            name='uzk_sensitivity2',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Условная чувствительность зарубка в мм'),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='control_type',
            field=models.IntegerField(blank=True, choices=[(1, 'РК'), (2, 'УЗК'), (3, 'ВИК'), (4, 'РК-ВИК'), (5, 'УК'), (6, 'УЗК-ЦД'), (7, 'РК-УЗК'), (8, 'РК-УЗК-ЦД'), (9, 'ПВК'), (10, 'МК'), (11, 'ВК'), (12, 'СР')], db_index=True, null=True, verbose_name='Вид контроля, например, РК'),
        ),
    ]