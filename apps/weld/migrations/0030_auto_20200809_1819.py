# Generated by Django 2.2.3 on 2020-08-09 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0029_weldingjointstate'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='complete_joints',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Количество выполненных заявок на стык'),
        ),
        migrations.AddField(
            model_name='line',
            name='in_progress_joints',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Количество заявок на стык, находящихся в работе у лаборатории'),
        ),
        migrations.AddField(
            model_name='line',
            name='new_joints',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Количество новых заявок на стык'),
        ),
        migrations.AddField(
            model_name='line',
            name='repair_joints',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Количество заявок на стык на ремонт'),
        ),
    ]