# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.addresses.models import Address
from apps.personal.models import Shopper
from apps.shop.models import Orders

class PickupPoint(Standard):
    """Модель для сохранения адреса пользователя для заказа
    """
    address = models.ForeignKey(Address,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Пункт самовывоза пользователя')
    shopper = models.ForeignKey(Shopper,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Пользователь')
    order = models.ForeignKey(Orders,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Заказ пользователя')

    class Meta:
        verbose_name = 'Simaland - Пункт вывоза'
        verbose_name_plural = 'Simaland - Пункты вывоза'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(PickupPoint, self).save(*args, **kwargs)

