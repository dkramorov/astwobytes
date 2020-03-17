# Generated by Django 2.2.3 on 2020-03-16 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flatcontent', '0006_auto_20200314_1638'),
        ('products', '0003_auto_20200315_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='productscats',
            name='container',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flatcontent.Containers'),
        ),
        migrations.AlterField(
            model_name='productscats',
            name='cat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flatcontent.Blocks'),
        ),
    ]
