# Generated by Django 2.2.3 on 2023-04-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comp',
            name='token_data',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]