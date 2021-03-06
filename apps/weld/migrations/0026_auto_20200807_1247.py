# Generated by Django 2.2.3 on 2020-08-07 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0025_auto_20200803_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='line',
            name='diameter',
        ),
        migrations.RemoveField(
            model_name='line',
            name='side_thickness',
        ),
        migrations.AddField(
            model_name='weldingjoint',
            name='diameter',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=9, null=True, verbose_name='Диаметр в мм, например, 355.6'),
        ),
        migrations.AddField(
            model_name='weldingjoint',
            name='side_thickness',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=9, null=True, verbose_name='Толщина стенки, например, 4,78'),
        ),
    ]
