# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.personal.models import Shopper
from apps.products.models import Products

class Orders(Standard):
    """Заказы пользователя"""
    status_choices = (
        (1, 'Не подтвержден'),
        (2, 'Офомрлен'),
    )
    number = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Номер заказа')
    total = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2) # 99 000 000 000,00
    comments = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Комментарий к заказу')
    user = models.ForeignKey(Shopper, blank=True, null=True, verbose_name='Покупатель', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Магазин - Заказ'
        verbose_name_plural = 'Магазин - Заказы'

    def save(self, *args, **kwargs):
        super(Orders, self).save(*args, **kwargs)

class Purchases(Standard):
    """Товар/услуга, выбранная пользователем для покупки"""
    product_id = models.IntegerField(blank=True, null=True, db_index=True, verbose_name='Ид товара')
    product_name = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Наименование товара')
    product_manufacturer = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Производитель')
    product_measure = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Единица измерения')
    product_price = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, verbose_name='Оригинальная цена без скидок') # 99 000 000 000,00
    product_code = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Код товара')
    count = models.IntegerField(blank=True, null=True, db_index=True, verbose_name='Количество товара')
    cost = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, verbose_name='Цена за единицу') # 99 000 000 000,00
    discount_info = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Информация по скидке')
    user = models.ForeignKey(Shopper, blank=True, null=True, verbose_name='Покупатель', on_delete=models.SET_NULL)
    order = models.ForeignKey(Orders, blank=True, null=True, on_delete=models.CASCADE)

    def total(self):
        """Общая сумма"""
        return self.cost * self.count

class WishList(Standard):
    status_choices = (
        (1, 'Избранное'),
        (2, 'Сравнить'),
    )
    product = models.ForeignKey(Products, blank=True, null=True, verbose_name='Товар в избранном', on_delete=models.SET_NULL)
    user = models.ForeignKey(Shopper, blank=True, null=True, verbose_name='Покупатель', on_delete=models.CASCADE)

