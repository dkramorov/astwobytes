# Generated by Django 2.2.3 on 2021-05-26 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatcontent', '0010_auto_20210430_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blocks',
            options={'permissions': (('seo_fields', 'Заполнение сео-полей меню'),), 'verbose_name': 'Стат.контент - Блоки', 'verbose_name_plural': 'Стат.контент - Блоки'},
        ),
    ]