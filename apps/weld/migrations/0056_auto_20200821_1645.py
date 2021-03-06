# Generated by Django 2.2.3 on 2020-08-21 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0055_auto_20200819_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='jointconclusion',
            name='vik_state',
            field=models.IntegerField(blank=True, choices=[(1, 'Годен'), (2, 'Ремонт'), (3, 'Вырез'), (4, 'УЗК'), (5, 'Пересвет'), (6, 'Брак')], db_index=True, null=True, verbose_name='Результат заключения ВИК'),
        ),
        migrations.AlterField(
            model_name='jointconclusion',
            name='state',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='weldingjoint',
            name='state',
            field=models.IntegerField(blank=True, choices=[(1, 'Новый'), (2, 'На контроле ЗНК'), (3, 'Годен'), (4, 'В ремонте')], db_index=True, null=True, verbose_name='Статус заявки, например, в работе'),
        ),
        migrations.AlterField(
            model_name='weldingjointstate',
            name='from_state',
            field=models.IntegerField(blank=True, choices=[(1, 'Новый'), (2, 'На контроле ЗНК'), (3, 'Годен'), (4, 'В ремонте')], db_index=True, null=True, verbose_name='Статус заявки, например, в работе'),
        ),
        migrations.AlterField(
            model_name='weldingjointstate',
            name='to_state',
            field=models.IntegerField(blank=True, choices=[(1, 'Новый'), (2, 'На контроле ЗНК'), (3, 'Годен'), (4, 'В ремонте')], db_index=True, null=True, verbose_name='Статус заявки, например, в работе'),
        ),
    ]
