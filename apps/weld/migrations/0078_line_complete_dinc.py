# Generated by Django 2.2.3 on 2020-10-02 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0077_auto_20200928_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='complete_dinc',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=9, null=True, verbose_name='Выполнено D-inc'),
        ),
    ]
