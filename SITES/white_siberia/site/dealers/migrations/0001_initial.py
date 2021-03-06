# Generated by Django 2.2.3 on 2021-02-04 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer',
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
                ('worktime', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('site', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='addresses.Address', verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Дилеры - Дилер',
                'verbose_name_plural': 'Дилеры - Дилеры',
            },
        ),
    ]
