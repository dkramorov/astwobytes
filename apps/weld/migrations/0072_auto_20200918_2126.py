# Generated by Django 2.2.3 on 2020-09-18 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0071_auto_20200916_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weldingjoint',
            name='diameter',
        ),
        migrations.RemoveField(
            model_name='weldingjoint',
            name='dinc',
        ),
        migrations.RemoveField(
            model_name='weldingjoint',
            name='side_thickness',
        ),
        migrations.RemoveField(
            model_name='weldingjoint',
            name='welding_date',
        ),
        migrations.AddField(
            model_name='joint',
            name='diameter',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=9, null=True, verbose_name='Диаметр в мм, например, 355.6'),
        ),
        migrations.AddField(
            model_name='joint',
            name='dinc',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=9, null=True, verbose_name='D-inc, например, 6.30, нужен для отчетов, рассчитывается динамически, например, диаметр(160)/константа(25.4)=6.30'),
        ),
        migrations.AddField(
            model_name='joint',
            name='side_thickness',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=9, null=True, verbose_name='Толщина стенки, например, 4,78'),
        ),
        migrations.AddField(
            model_name='joint',
            name='welding_date',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата сварки, например, 12.03.2020'),
        ),
    ]
