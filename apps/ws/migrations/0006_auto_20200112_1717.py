# Generated by Django 2.2.3 on 2020-01-12 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ws', '0005_auto_20200102_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bcastmessages',
            name='img',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='conversationgroup',
            name='img',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='conversations',
            name='img',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='img',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]