# Generated by Django 2.2.3 on 2020-07-18 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0006_auto_20200717_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='letterofguarantee',
            name='welder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weld.Welder', verbose_name='Сварщик'),
        ),
    ]