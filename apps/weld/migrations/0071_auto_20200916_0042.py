# Generated by Django 2.2.3 on 2020-09-16 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0070_auto_20200916_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vik',
            name='welder',
        ),
        migrations.RemoveField(
            model_name='holdingkss',
            name='date',
        ),
        migrations.AddField(
            model_name='holdingkss',
            name='test_date',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата проведения ВИК или УЗК/РК)'),
        ),
        migrations.DeleteModel(
            name='ControlK',
        ),
        migrations.DeleteModel(
            name='Vik',
        ),
    ]
