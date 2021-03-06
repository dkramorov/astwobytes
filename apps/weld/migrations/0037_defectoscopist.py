# Generated by Django 2.2.3 on 2020-08-12 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0036_auto_20200812_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Defectoscopist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('stigma', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Номер удостоверения, например, 0048-1962')),
                ('notice', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Примечание, например, нет закл. ВИК, РК, ДЛ')),
            ],
            options={
                'verbose_name': 'Сварщики - Сварщик',
                'verbose_name_plural': 'Сварщики - Сварщики',
            },
        ),
    ]
