# Generated by Django 2.2.3 on 2021-10-24 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flatcontent', '0011_auto_20210526_2033'),
        ('addresses', '0001_initial'),
        ('companies', '0003_auto_20211023_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='addresses.Address', verbose_name='Адрес'),
        ),
        migrations.CreateModel(
            name='MainCompany2Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flatcontent.Blocks')),
                ('main_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.MainCompany')),
            ],
        ),
        migrations.CreateModel(
            name='Company2Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flatcontent.Blocks')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.Company')),
            ],
        ),
    ]