# Generated by Django 2.2.3 on 2021-03-29 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0013_property_search_facet'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.IntegerField(blank=True, null=True, verbose_name='Цвет для фото товара')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Products', verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Товары - Цвет',
                'verbose_name_plural': 'Товары - Цвета',
                'default_permissions': [],
            },
        ),
    ]
