# Generated by Django 2.2.3 on 2019-12-09 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ws', '0003_messages_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationgroup',
            name='user_id',
            field=models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Пользователь, который создал беседу'),
        ),
    ]