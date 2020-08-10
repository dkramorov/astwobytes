# Generated by Django 2.2.3 on 2020-08-02 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weld', '0022_company_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='code',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Код объекта, например, ГФУ'),
        ),
        migrations.AlterField(
            model_name='company',
            name='code',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='Код компании, например, ТПС'),
        ),
    ]
