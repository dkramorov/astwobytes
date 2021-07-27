# Generated by Django 2.2.3 on 2021-07-17 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_orders_external_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('position', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('state', models.IntegerField(blank=True, db_index=True, null=True)),
                ('parents', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('latitude', models.DecimalField(blank=True, db_index=True, decimal_places=25, max_digits=30, null=True)),
                ('longitude', models.DecimalField(blank=True, db_index=True, decimal_places=25, max_digits=30, null=True)),
                ('time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Время доставки')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес строкой')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Orders')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
