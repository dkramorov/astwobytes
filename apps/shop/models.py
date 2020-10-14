# -*- coding: utf-8 -*-
import datetime

from django.db import models

from apps.main_functions.models import Standard
from apps.personal.models import Shopper
from apps.products.models import Products, CostsTypes

class PromoCodes(Standard):
    """Промокоды"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Название промокода')
    percent = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Процентная скидка по промо-коду')
    value = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Скидка на сумму')
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Промокод')
    start_date = models.DateTimeField(blank=True, null=True, db_index=True,
        verbose_name='Начало действия')
    end_date = models.DateTimeField(blank=True, null=True, db_index=True,
        verbose_name='Окончание действия')
    use_count = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Ограничение на кол-во применений')
    personal = models.ForeignKey(Shopper,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Промокод для конкретного пользователя (персональный)')
# TODO: 1) на рубрику товаров
#       2) на группу товаров или 1 товар
#       3) не более чем %x от суммы заказа
#       4) время проставить в форме точное
#       5) действует при минимальной/максимальной сумме корзинки
    class Meta:
        verbose_name = 'Магазин - Промокод'
        verbose_name_plural = 'Магазин - Промокоды'
        #default_permissions = []

    def is_valid(self, shopper_id = None):
        """Проверка, что промокод действует
           :param shopper_id: если промокод персональный,
                              должен быть привязан к этому пользователю
        """
        now = datetime.datetime.today()
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        if self.use_count and self.use_count <= 0:
            return False
        if self.personal_id:
            if not self.personal_id == shopper_id:
                return False
        return True

class Orders(Standard):
    """Заказы пользователя"""
    status_choices = (
        (1, 'Не подтвержден'),
        (2, 'Офомрлен'),
    )
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер заказа')
    total = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=13, decimal_places=2) # 99 000 000 000,00
    promocode = models.ForeignKey(PromoCodes,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Примененный промокод')
    discount = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=13, decimal_places=2,
        verbose_name='Скидка, включенная в total, например, по промокоду')
    comments = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Комментарий к заказу')
    # Информация о покупателе к заказу
    shopper = models.ForeignKey(Shopper,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Покупатель')
    shopper_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    shopper_email = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    shopper_phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    shopper_address = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    shopper_ip = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Магазин - Заказ'
        verbose_name_plural = 'Магазин - Заказы'

    def save(self, *args, **kwargs):
        super(Orders, self).save(*args, **kwargs)

class Transactions(Standard):
    """Транзакция по онлайн оплате"""
    payment_choices = (
        (1, 'YandexKassa'),
    )
    uuid = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    order = models.ForeignKey(Orders,
        on_delete=models.SET_NULL,
        blank=True, null=True)
    ptype = models.IntegerField(choices=payment_choices,
        blank=True, null=True, db_index=True)
    success = models.BooleanField(default=False, db_index=True)
    body = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Магазин - Транзакция'
        verbose_name_plural = 'Магазин - Транзакции'
        #default_permissions = []

class Purchases(Standard):
    """Товар/услуга, выбранная пользователем для покупки"""
    product_id = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Ид товара')
    product_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование товара')
    product_manufacturer = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Производитель')
    product_measure = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Единица измерения')
    product_price = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=13, decimal_places=2,
        verbose_name='Оригинальная цена без скидок') # 99 000 000 000,00
    product_code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Код товара')
    cost_type = models.ForeignKey(CostsTypes,
        on_delete=models.SET_NULL,
        blank=True, null=True)
    count = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Количество товара')
    cost = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=13, decimal_places=2,
        verbose_name='Цена за единицу') # 99 000 000 000,00
    discount_info = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Информация по скидке')
    shopper = models.ForeignKey(Shopper,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Покупатель')
    order = models.ForeignKey(Orders,
        on_delete=models.CASCADE,
        blank=True, null=True)

    class Meta:
        verbose_name = 'Магазин - Покупки'
        verbose_name_plural = 'Магазин - Покупки'
        #default_permissions = []

    def total(self):
        """Общая сумма"""
        return self.cost * self.count

class WishList(Standard):
    status_choices = (
        (1, 'Избранное'),
        (2, 'Сравнить'),
    )
    product = models.ForeignKey(Products,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Товар в избранном')
    shopper = models.ForeignKey(Shopper,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Покупатель')

    class Meta:
        verbose_name = 'Магазин - Избранное'
        verbose_name_plural = 'Магазин - Избранное'
        default_permissions = []



