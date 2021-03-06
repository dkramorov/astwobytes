# Generated by Django 2.2.3 on 2020-08-19 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0053_auto_20200819_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jointconclusion',
            name='welding_type',
        ),
        migrations.AlterField(
            model_name='jointconclusion',
            name='pvk_state',
            field=models.IntegerField(blank=True, choices=[(1, 'Годен'), (2, 'Ремонт'), (3, 'Вырез'), (4, 'УЗК'), (5, 'Пересвет'), (6, 'Брак')], db_index=True, null=True, verbose_name='Оценка качества'),
        ),
        migrations.AlterField(
            model_name='jointconclusion',
            name='state',
            field=models.IntegerField(blank=True, choices=[(1, 'Годен'), (2, 'Ремонт'), (3, 'Вырез'), (4, 'УЗК'), (5, 'Пересвет'), (6, 'Брак')], db_index=True, null=True, verbose_name='Результат заключения'),
        ),
        migrations.AlterField(
            model_name='jointconclusion',
            name='uzk_state',
            field=models.IntegerField(blank=True, choices=[(1, 'Годен'), (2, 'Ремонт'), (3, 'Вырез'), (4, 'УЗК'), (5, 'Пересвет'), (6, 'Брак')], db_index=True, null=True, verbose_name='Оценка качества'),
        ),
        migrations.AlterField(
            model_name='rkframes',
            name='state',
            field=models.IntegerField(blank=True, choices=[(1, 'Годен'), (2, 'Ремонт'), (3, 'Вырез'), (4, 'УЗК'), (5, 'Пересвет'), (6, 'Брак')], db_index=True, null=True, verbose_name='Заключение'),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='control_result',
            field=models.IntegerField(blank=True, choices=[(1, 'Годен'), (2, 'Ремонт'), (3, 'Вырез'), (4, 'УЗК'), (5, 'Пересвет'), (6, 'Брак')], db_index=True, null=True, verbose_name='Результат контроля, например, Вырезать'),
        ),
    ]
