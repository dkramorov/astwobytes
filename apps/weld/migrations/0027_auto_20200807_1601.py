# Generated by Django 2.2.3 on 2020-08-07 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0026_auto_20200807_1247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='base',
            options={'verbose_name': 'Структура - Установка', 'verbose_name_plural': 'Структура - Установки'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Структура - Компания', 'verbose_name_plural': 'Структура - Компании'},
        ),
        migrations.AlterModelOptions(
            name='joint',
            options={'verbose_name': 'Структура - Стык', 'verbose_name_plural': 'Структура - Стыки'},
        ),
        migrations.AlterModelOptions(
            name='line',
            options={'verbose_name': 'Структура - Линия', 'verbose_name_plural': 'Структура - Линии'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'Структура - Объект', 'verbose_name_plural': 'Структура - Объекты'},
        ),
        migrations.AlterModelOptions(
            name='titul',
            options={'verbose_name': 'Структура - Титул', 'verbose_name_plural': 'Структура - Титулы'},
        ),
    ]