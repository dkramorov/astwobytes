# Generated by Django 2.2.3 on 2020-08-10 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0031_auto_20200809_2209'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together={('code', 'company')},
        ),
    ]
