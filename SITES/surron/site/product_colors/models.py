# -*- coding: utf-8 -*-
from django.db import models

from apps.products.models import Products

class ProductColor(models.Model):
    """Основной цвет для фото товара"""
    product = models.ForeignKey(Products,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Адрес')
    color = models.IntegerField(blank=True, null=True,
        verbose_name='Цвет для фото товара')

    class Meta:
        verbose_name = 'Товары - Цвет'
        verbose_name_plural = 'Товары - Цвета'

        default_permissions = []

