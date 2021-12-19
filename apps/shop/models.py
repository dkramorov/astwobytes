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
    state_choices = (
        (1, 'Не подтвержден'),
        (2, 'В обработке'),
        (3, 'Оформлен'),
    )
    payment_choices = (
        (1, 'Не оплачен'),
        (2, 'Частично оплачен'),
        (3, 'Оплачен'),
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
    payed = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=13, decimal_places=2,
        verbose_name='Оплаченная сумма')
    #payment_status = models.IntegerField(choices=payment_choices,
    #    blank=True, null=True, db_index=True,
    #    verbose_name='Статус оплаты')
    external_number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Внешний номер заказа от платежной системы')

    class Meta:
        verbose_name = 'Магазин - Заказ'
        verbose_name_plural = 'Магазин - Заказы'

    def save(self, *args, **kwargs):
        super(Orders, self).save(*args, **kwargs)

    def total_without_discount(self):
        """Итого без скидки"""
        result = self.total or 0
        if self.discount:
            result += self.discount
        if result < 0:
            result = 0
        return result

    def get_number(self):
        """Номер заказа"""
        return self.number or self.id

    def get_shopper(self):
        """Покупатель заказа"""
        return self.shopper.to_dict() if self.shopper else {}

    def get_promocode(self):
        """Промокод на заказ"""
        if self.promocode:
            value = ''
            if self.promocode.percent:
                value += '%'
            if not value and self.promocode.value:
                value += '₽'
            return {
                'name': self.promocode,
                'value': value,
            }
        return {}

    def get_purchases(self):
        """Получить покупки по заказу"""
        result = []
        costs_types = CostsTypes.objects.all().values('id', 'name')
        ids_costs_types = {cost_type['id']: cost_type for cost_type in costs_types}
        for purchase in self.purchases_set.all():
            cost_type = ids_costs_types.get(purchase.cost_type_id)
            result.append({
                'id': purchase.product_id,
                'name': purchase.product_name,
                'cost_type_id': cost_type['id'] if cost_type else '',
                'cost_type_name': cost_type['name'] if cost_type else '',
                'manufacturer': purchase.product_manufacturer,
                'measure': purchase.product_measure,
                'price': purchase.product_price,
                'code': purchase.product_code,
                'count': purchase.count,
                'cost': purchase.cost,
                'total': (purchase.cost * purchase.count) if purchase.cost and purchase.count else 0,
            })

        return result

class OrdersDelivery(Standard):
    """Доставка для заказа"""
    order = models.ForeignKey(Orders, blank=True, null=True,
        on_delete=models.CASCADE)
    latitude = models.DecimalField(blank=True, null=True,
        max_digits=30, decimal_places=25, db_index=True)
    longitude = models.DecimalField(blank=True, null=True,
        max_digits=30, decimal_places=25, db_index=True)
    time = models.DateTimeField(blank=True, null=True,
        db_index=True, verbose_name='Время доставки')
    address = models.CharField(max_length=255,
        blank=True, null=True,
        verbose_name='Адрес строкой')
    additional_data = models.TextField(blank=True, null=True,
        verbose_name='json ина с доп данными')

    class Meta:
        verbose_name = 'Магазин - Доставка заказа'
        verbose_name_plural = 'Магазин - Доставки заказов'

class Transactions(Standard):
    """Транзакция по онлайн оплате"""
    payment_choices = (
        (1, 'YandexKassa'),
        (2, 'Сбербанк'),
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
    product_min_count = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Минимальное кол-во товара для заказа')
    product_multiplicity = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Кратность товара (кол-во добавляемого товара в корзину)')
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



