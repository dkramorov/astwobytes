# Generated by Django 2.2.3 on 2021-05-16 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_auto_20200809_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='domain',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Домен для мультиязычного сайта'),
        ),
        migrations.AlterField(
            model_name='files',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='files',
            name='link',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Пользовательская ссылка на файл'),
        ),
        migrations.AlterField(
            model_name='files',
            name='mime',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Mime-type'),
        ),
        migrations.AlterField(
            model_name='files',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Название для файла'),
        ),
        migrations.AlterField(
            model_name='files',
            name='path',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Внутренняя ссылка на файл'),
        ),
    ]