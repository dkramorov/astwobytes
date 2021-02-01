# -*- coding:utf-8 -*-
import logging
from django.conf import settings

from apps.personal.models import Shopper
from apps.products.models import Products

from apps.shop.models import Orders, Purchases

logger = logging.getLogger('main')

def get_order(shopper: dict, order_id: int):
    """Заказ пользователя
       :param shopper: покупатель Shopper или json из сессии
       :param order_id: ид заказа
    """
    PRODUCT_FIELDS = (
        'name',
        'manufacturer',
        'measure',
        'old_price',
        'price',
        'code',
    )

    shopper_id = None
    if isinstance(shopper, dict):
        shopper_id = shopper.get('id')
    elif isinstance(shopper, Shopper):
        shopper_id = shopper.id

    if not shopper_id:
        return {}

    order = Orders.objects.filter(pk=order_id, shopper=shopper_id).first()
    if not order:
        return {}

    result = {
        'order': order,
    }
    purchases = Purchases.objects.filter(shopper=shopper_id, order=order).order_by('position')
    if not purchases:
        return result

    total = 0
    items = 0 # Количество наименований
    items_count = 0 # Количество товаров
    discount = order.discount if order.discount else 0 # Скидка (по промокоду)

    ids_products = {}
    for purchase in purchases:
        total += purchase.cost * purchase.count
        items += 1
        items_count += purchase.count
        ids_products[purchase.product_id] = None

    result['cart'] = {
        'total': total,
        'discount': discount,
        'total_with_discount': total - discount,
        'items': items,
        'items_count': items_count,
        # окончания через шаблон лучше
        #'ends': analyze_digit(items, end=('наименование', 'наименований', 'наименования')),
        #'ends_count': analyze_digit(items_count, end=('товар', 'товаров', 'товара'))
    }

    # -------------------
    # Скидка по промокоду
    # -------------------
    if order.promocode:
        pcode = PromoCodes.objects.filter(pk=promocode, is_active=True).first()
        result['promocode'] = pcode.code

    # Достаем товары,
    # актуализируем информацию
    absent = []
    products = Products.objects.filter(pk__in=ids_products.keys())

    for product in products:
        ids_products[product.id] = product
    for purchase in purchases:
        product = ids_products.get(purchase.product_id)
        if not product:
            absent.append(purchase.id)
            continue
        purchase.thumb = product.thumb()
        purchase.link = product.link()
        for field in PRODUCT_FIELDS:
            value = getattr(product, field)
            setattr(purchase, 'product_%s' % field, value)
    result['purchases'] = [purchase for purchase in purchases if not purchase.id in absent]
    return result
