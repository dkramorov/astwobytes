# Generated by Django 2.2.3 on 2020-05-06 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0002_svisits'),
    ]

    operations = [
        migrations.AddField(
            model_name='svisits',
            name='ip',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
