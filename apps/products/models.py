# -*- coding: utf-8 -*-
from django.db import models

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.models import Standard
from apps.main_functions.string_parser import translit

class Products(Standard):
    """Товары/услуги"""
    currency_choices = (
        (1, '₽'),
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    altname = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    measure = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    currency = models.IntegerField(choices=currency_choices, blank=True, null=True, db_index=True)
    old_price = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, db_index=True) # 99 000 000 000,00
    price = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, db_index=True) # 99 000 000 000,00
    dj_info = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    mini_info = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    count = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Товары - товар/услуга'
        verbose_name_plural = 'Товары - товары/услуги'

    def save(self, *args, **kwargs):
        if self.old_price and self.old_price > 99999999999:
            self.old_price = None
        if self.price and self.price > 99999999999:
            self.price = None
        super(Products, self).save(*args, **kwargs)

    def link(self):
        """Ссылка на товар/услугу"""
        link = '/product/%s/' % self.id
        if self.code and self.name:
            link = '/product/%s-%s/' % (translit(self.name), self.code)
        elif self.name:
            link = '/product/%s-%s/' % (translit(self.name), self.id)
        return link

class Property(Standard):
    """Свойство для товара"""
    ptype_choices = (
        (1, 'Выпадающий список select'),
        (2, 'Выпадающий список с множественным выбором multiselect'),
        (3, 'Выбор из вариантов radio'),
        (4, 'Множественный выбор из вариантов checkbox'),
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    code = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    ptype = models.IntegerField(choices=ptype_choices, blank=True, null=True, db_index=True)

class PropertiesValues(Standard):
    """Свойства для товаров/услуг
       это точные свойства, то есть, не текст от балды,
       а именно конкретное свойство с конкретным значением
    """
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    str_value = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    digit_value = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=4, db_index=True) # 990 000 000,0000

    def save(self, *args, **kwargs):
        if self.digit_value and self.digit_value > 999999999:
            self.digit_value = None
        super(PropertiesValues, self).save(*args, **kwargs)

class ProductsProperties(models.Model):
    """Линковка значения свойства к товару"""
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    prop = models.ForeignKey(PropertiesValues, on_delete=models.CASCADE)

class ProductsCats(models.Model):
    """Рубрики товаров"""
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    container = models.ForeignKey(Containers, blank=True, null=True, on_delete=models.CASCADE)
    cat = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.CASCADE)

class ProductsPhotos(Standard):
    """Галереи для товаров"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

