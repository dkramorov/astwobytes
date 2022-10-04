# Generated by Django 2.2.3 on 2022-04-18 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatcontent', '0011_auto_20210526_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='containers',
            name='custom_font',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True, verbose_name='Название своего шрифта (например, для иконок)'),
        ),
        migrations.AlterField(
            model_name='containers',
            name='class_name',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True, verbose_name='Класс css'),
        ),
        migrations.AlterField(
            model_name='containers',
            name='tag',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='containers',
            name='template_position',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True),
        ),
    ]