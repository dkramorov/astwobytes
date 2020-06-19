# -*- coding:utf-8 -*-
from apps.personal.models import Shopper
from apps.products.models import Products
from apps.main_functions.string_parser import get_request_ip

from .models import Orders, Purchases

PRODUCT_FIELDS = (
    'name',
    'manufacturer',
    'measure',
    'old_price',
    'price',
    'code',
)

def calc_cart(shopper, min_info: bool = False):
    """Корзинка пользователя"""
    result = {}
    purchases = Purchases.objects.filter(user=shopper, order__isnull=True).order_by('position')
    if not purchases:
        return result

    total = 0
    items = 0 # Количество наименований
    items_count = 0 # Количество товаров

    ids_products = {}
    for purchase in purchases:
        total += purchase.cost * purchase.count
        items += 1
        items_count += purchase.count
        ids_products[purchase.product_id] = None

    result = {
        'total': total,
        'items': items,
        'items_count': items_count,
        # окончания через шаблон лучше
        #'ends': analyze_digit(items, end=('наименование', 'наименований', 'наименования')),
        #'ends_count': analyze_digit(items_count, end=('товар', 'товаров', 'товара'))
    }
    # Достаем товары,
    # актуализируем информацию
    # в базу обновление не производим, удаление тоже
    # будем делать удаление/обновление в базе при оформлении заказа
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

def get_shopper(request):
    """Пользователь из сессии"""
    shopper = request.session.get('shopper')
    # Создаем виртуального пользователя
    ip = get_request_ip(request)
    if not shopper:
        shopper = Shopper(name='Гость', ip=ip)
        request.session['shopper'] = shopper.to_dict()
    else:
        shopper = Shopper.objects.filter(pk=shopper['id']).first()
        if not shopper:
            shopper = Shopper(name='Гость', ip=ip)
            request.session['shopper'] = shopper.to_dict()
    return shopper

def create_shopper(request):
    """Создание пользователя
       :param request: HttpRequest
       :param shopper: словарь пользователя
    """
    shopper = get_shopper(request)
    shopper = Shopper.objects.create(ip=shopper.ip, name=shopper.name)
    request.session['shopper'] = shopper.to_dict()
    return shopper


