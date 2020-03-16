# -*- coding: utf-8 -*-
from django.db import models

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.models import Standard

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
        super(Products, self).save(*args, **kwargs)

    def link(self):
        """Ссылка на товар/услугу"""
        link = '/product/%s/' % self.id
        if self.code and self.name:
            link = '/product/%s-%s/' % (translit(self.name), self.code)
        elif self.name:
            link = '/product/%s-%s/' % (translit(self.name), self.id)
        return link

class ProductsCats(models.Model):
    """Рубрики товаров"""
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    #container = models.ForeignKey(Containers, on_delete=models.CASCADE)
    cat = models.ForeignKey(Blocks, on_delete=models.CASCADE)

class ProductsPhotos(Standard):
    """Галереи для товаров"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


