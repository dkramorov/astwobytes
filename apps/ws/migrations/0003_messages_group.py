# Generated by Django 2.2.3 on 2019-12-03 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ws', '0002_auto_20191203_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ws.ConversationGroup'),
        ),
    ]