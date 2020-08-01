# Generated by Django 2.2.3 on 2020-07-19 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200719_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='discount',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=13, null=True, verbose_name='Скидка, включенная в total, например, по промокоду'),
        ),
        migrations.AddField(
            model_name='orders',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.PromoCodes', verbose_name='Примененный промокод'),
        ),
    ]
