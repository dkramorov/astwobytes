# Generated by Django 2.2.3 on 2020-07-30 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0012_auto_20200726_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holdingkss',
            name='material',
            field=models.IntegerField(blank=True, choices=[(1, '09Г2С'), (2, '12Х18Н10Т'), (3, '08Х18Н10Т')], db_index=True, null=True, verbose_name='Материал - сталь, например, 12Х18Н10Т'),
        ),
        migrations.AlterField(
            model_name='nax',
            name='welding_type',
            field=models.IntegerField(blank=True, choices=[(1, 'РАД'), (2, 'РД'), (3, 'РАД - РД')], db_index=True, null=True, verbose_name='Тип сварки, например, РД'),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='material',
            field=models.IntegerField(blank=True, choices=[(1, '09Г2С'), (2, '12Х18Н10Т'), (3, '08Х18Н10Т')], db_index=True, null=True, verbose_name='Материал - сталь, например, 09Г2С'),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='welding_type',
            field=models.IntegerField(blank=True, choices=[(1, 'РАД'), (2, 'РД'), (3, 'РАД - РД')], db_index=True, null=True, verbose_name='Тип сварки, например, РД'),
        ),
        migrations.DeleteModel(
            name='Material',
        ),
    ]
