# Generated by Django 2.2.3 on 2020-07-22 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20200714_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='function',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Должность'),
        ),
    ]