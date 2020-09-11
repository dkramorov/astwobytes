# Generated by Django 2.2.3 on 2020-09-01 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0060_auto_20200826_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='jointconclusion',
            name='repair',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Номер ремонта'),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='welding_conn_view',
            field=models.IntegerField(blank=True, choices=[(1, 'С17'), (2, 'У19'), (3, 'У20'), (4, 'С17/У20'), (5, 'У18')], db_index=True, null=True, verbose_name='Вид сварного соединения, например, C17'),
        ),
    ]
