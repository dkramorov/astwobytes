# Generated by Django 2.2.3 on 2020-08-12 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0039_auto_20200812_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='jointconclusion',
            name='pvk_active',
            field=models.BooleanField(blank=True, db_index=True, null=True, verbose_name='Проведен ПВК (показываем в таблице, что проведен)'),
        ),
        migrations.AddField(
            model_name='jointconclusion',
            name='pvk_defects',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Выявленные дефекты ПВК'),
        ),
        migrations.AddField(
            model_name='jointconclusion',
            name='rk_active',
            field=models.BooleanField(blank=True, db_index=True, null=True, verbose_name='Проведен РК (показываем в таблице, что проведен)'),
        ),
        migrations.AddField(
            model_name='jointconclusion',
            name='uzk_active',
            field=models.BooleanField(blank=True, db_index=True, null=True, verbose_name='Проведен УЗК (показываем в таблице, что проведен)'),
        ),
        migrations.AddField(
            model_name='jointconclusion',
            name='uzk_defects',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Выявленные дефекты УЗК'),
        ),
        migrations.CreateModel(
            name='RKFrames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('number', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Номер снимка, координаты мерного пояса')),
                ('sensitivity', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=6, null=True, verbose_name='Чувствительность снимка в мм или %')),
                ('defects', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Выявленные дефекты')),
                ('notice', models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Примечание')),
                ('state', models.IntegerField(blank=True, choices=[(1, 'Годен'), (2, 'Исправить'), (3, 'Вырезать')], db_index=True, null=True, verbose_name='Заключение')),
                ('joint_conclusion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weld.JointConclusion', verbose_name='Акт/заключение по заявке на стык')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
