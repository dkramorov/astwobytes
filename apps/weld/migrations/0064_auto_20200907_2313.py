# Generated by Django 2.2.3 on 2020-09-07 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0063_auto_20200901_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('number', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Номер удостоверения')),
                ('welding_type', models.IntegerField(blank=True, choices=[(1, 'РАД'), (2, 'РД'), (3, 'РАД - РД')], db_index=True, null=True, verbose_name='Способ сварки')),
            ],
            options={
                'verbose_name': 'Сварщики - Удостоверение',
                'verbose_name_plural': 'Сварщики - Удостоверения',
                'default_permissions': [],
            },
        ),
        migrations.AddField(
            model_name='welder',
            name='first_name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='welder',
            name='last_name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='welder',
            name='middle_name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='welder',
            name='stigma2',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Клеймо по приказу, например, 9SZN'),
        ),
        migrations.CreateModel(
            name='CertSections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('group', models.IntegerField(blank=True, choices=[(1, 'ПАО "Транснефть"'), (2, 'ПАО "Газпром"'), (3, 'ГДО Горнодобывающее оборудование'), (4, 'ГО Газовое оборудование'), (5, 'КО Котельное оборудование'), (6, 'КСМ Конструкции стальных мостов'), (7, 'МО Металлургическое оборудование'), (8, 'НГДО Нефтегазодобывающее оборудование'), (9, 'ОТОГ Оборудование для транспортировки опасных грузов'), (10, 'ОХНВП Оборудование химических, нефтехимических, нефтеперерабатывающих и взрывопожароопасных производств'), (11, 'ПТО Подъемно-транспортное оборудование'), (12, 'СК Строительные конструкции')], db_index=True, null=True, verbose_name='Группы технических устройств опасных производственных объектов, например, "ПАО "Газпром" "')),
                ('points', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Пункты технических устройств опасных производственных объектов, например, 1,3')),
                ('certification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weld.Certification', verbose_name='Удостоверение сварщика')),
            ],
            options={
                'verbose_name': 'Сварщики - Тех. устройство',
                'verbose_name_plural': 'Сварщики - Тех. устройства',
                'default_permissions': [],
            },
        ),
        migrations.AddField(
            model_name='certification',
            name='welder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weld.Welder', verbose_name='Сварщик'),
        ),
    ]
