# Generated by Django 2.2.3 on 2020-09-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0075_auto_20200923_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='project_dinc',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=9, null=True, verbose_name='D-inc по проекту'),
        ),
        migrations.AddField(
            model_name='line',
            name='project_joint_count',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Кол-во стыков по проекту'),
        ),
        migrations.AlterField(
            model_name='joint',
            name='join_type_from',
            field=models.IntegerField(blank=True, choices=[(1, 'труба'), (2, 'отвод'), (3, 'тройник'), (4, 'переход'), (5, 'заглушка'), (6, 'фланец'), (7, 'штуцер'), (8, 'бобышка'), (9, 'пробка')], db_index=True, null=True, verbose_name='Свариваемые элементы, например, тройник/переходник'),
        ),
        migrations.AlterField(
            model_name='joint',
            name='join_type_to',
            field=models.IntegerField(blank=True, choices=[(1, 'труба'), (2, 'отвод'), (3, 'тройник'), (4, 'переход'), (5, 'заглушка'), (6, 'фланец'), (7, 'штуцер'), (8, 'бобышка'), (9, 'пробка')], db_index=True, null=True, verbose_name='Свариваемые элементы, например, тройник/труба'),
        ),
    ]
