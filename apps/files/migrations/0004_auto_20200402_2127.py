# Generated by Django 2.2.3 on 2020-04-02 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_auto_20200112_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
