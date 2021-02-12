# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.addresses.models import Address

class Dealer(Standard):
    """Дилеры"""
    city_choices = (
        (1, 'Москва'),
        (2, 'Самара'),
        (3, 'Омск'),
        (4, 'Казань'),
        (5, 'Санкт-Петербург'),
        (6, 'Сочи'),
        (7, 'Белгород'),
        (8, 'Киров'),
        (9, 'Екатеринбург'),
        (10, 'Пермь'),
        (11, 'Орёл'),
        (12, 'Великий Новгород'),
        (13, 'Красноярск'),
        (14, 'Ставрополь'),
        (15, 'Тула'),
        (16, 'Севастополь'),
        (17, 'Симферополь'),
        (18, 'Уфа'),
        (19, 'Воронеж'),
        (20, 'Курган'),
        (21, 'Краснодар'),
        (22, 'Нижний Новгород'),
        (23, 'Минск (Беларусь)'),
        (24, 'Караганда (Казахстан)'),
    )
    city = models.IntegerField(blank=True, null=True, db_index=True,
        choices=city_choices,
        verbose_name='Город')
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    address = models.ForeignKey(Address,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Адрес')
    worktime = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    site = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Дилеры - Дилер'
        verbose_name_plural = 'Дилеры - Дилеры'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Dealer, self).save(*args, **kwargs)

