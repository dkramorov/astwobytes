# Generated by Django 2.2.3 on 2021-02-04 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='city',
            field=models.IntegerField(blank=True, choices=[(1, 'Москва'), (2, 'Самара'), (3, 'Омск'), (4, 'Казань'), (5, 'Санкт-Петербург'), (6, 'Сочи'), (7, 'Белгород'), (8, 'Киров'), (9, 'Екатеринбург'), (10, 'Пермь'), (11, 'Орёл'), (12, 'Великий Новгород'), (13, 'Красноярск'), (14, 'Ставрополь'), (15, 'Тула'), (16, 'Севастополь'), (17, 'Симферополь'), (18, 'Уфа'), (19, 'Воронеж'), (20, 'Курган'), (21, 'Краснодар'), (22, 'Нижний Новгород'), (23, 'Минск (Беларусь)'), (24, 'Караганда (Казахстан)')], db_index=True, null=True, verbose_name='Город'),
        ),
    ]
