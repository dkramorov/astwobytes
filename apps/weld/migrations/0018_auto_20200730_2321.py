# Generated by Django 2.2.3 on 2020-07-30 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0017_auto_20200730_2246'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='base',
            unique_together={('name', 'titul')},
        ),
        migrations.AlterUniqueTogether(
            name='joint',
            unique_together={('name', 'line')},
        ),
        migrations.AlterUniqueTogether(
            name='line',
            unique_together={('name', 'titul')},
        ),
        migrations.AlterUniqueTogether(
            name='titul',
            unique_together={('name', 'subject')},
        ),
    ]