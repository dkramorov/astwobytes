# Generated by Django 2.2.3 on 2021-10-23 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20211021_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('tag', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('resume', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Компании - филиал', 'verbose_name_plural': 'Компании - филиалы'},
        ),
        migrations.AddField(
            model_name='company',
            name='main_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='companies.MainCompany', verbose_name='Родительская компания группы филиалов'),
        ),
    ]