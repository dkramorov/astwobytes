# -*- coding:utf-8 -*-
from apps.personal.models import Shopper
from apps.personal.utils import save_user_to_request
from apps.products.models import Products
from apps.main_functions.string_parser import get_request_ip
from apps.main_functions.catcher import check_email, check_phone

from .models import Orders, Purchases

PRODUCT_FIELDS = (
    'name',
    'manufacturer',
    'measure',
    'old_price',
    'price',
    'code',
)

def get_purchase(pk: int, shopper: Shopper, is_purchase: bool = True):
    """Вытащить из базы покупку,
       покупка должна быть без заказа,
       принадлежать переданному пользователю
       :param pk: ид покупки или товара
       :param shopper: пользователь
       :param is_purchase: ищем ид покупки, иначе ид товара
       :return: Purchase object
    """
    if is_purchase:
        return Purchases.objects.filter(pk=pk, order__isnull=True, shopper=shopper).first()
    return Purchases.objects.filter(product_id=pk, order__isnull=True, shopper=shopper).first()

def calc_cart(shopper, min_info: bool = False):
    """Корзинка пользователя
       :param shopper: покупатель Shopper или json из сессии
       :param min_info: с товарами или без
    """
    shopper_id = None
    if isinstance(shopper, dict):
        shopper_id = shopper.get('id')
    elif isinstance(shopper, Shopper):
        shopper_id = shopper.id
    if not shopper_id:
        return {}

    result = {}
    purchases = Purchases.objects.filter(shopper=shopper_id, order__isnull=True).order_by('position')
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

def get_shopper(request, guest_enter: bool = False):
    """Пользователь из сессии
       :param request: HttpRequest
       :param guest_enter: гостевой вход (завести виртуального юзера)
       :return: Shopper, не надо возвращать dict
    """
    shopper = request.session.get('shopper')
    if not guest_enter:
        if isinstance(shopper, dict):
            user = Shopper()
            for k, v in shopper.items():
                setattr(user, k, v)
            return user
        return shopper

    # Создаем виртуального пользователя
    ip = get_request_ip(request)
    if not shopper:
        shopper = Shopper(name='Гость', ip=ip)
        request.session['shopper'] = shopper.to_dict()
    else:
        shopper = Shopper.objects.filter(pk=shopper.id).first()
        if not shopper:
            shopper = Shopper(name='Гость', ip=ip)
            request.session['shopper'] = shopper.to_dict()
    return shopper

def create_shopper(request):
    """Создание пользователя
       :param request: HttpRequest
       :param shopper: словарь пользователя
    """
    shopper = get_shopper(request, guest_enter=True)
    shopper = Shopper.objects.create(ip=shopper.ip, name=shopper.name)
    request.session['shopper'] = shopper.to_dict()
    return shopper

def create_new_order(request, shopper, cart):
    """Оформление заказа пользователем,
       нажатие кнопки на сайте Оформить заказ
       :param request: HttpRequest
       :param shopper: покупатель
       :param cart: корзинка пользователя
    """
    if not shopper or not cart or not shopper.id:
        return {}

    fields = ('name',
              'first_name',
              'last_name',
              'middle_name',
              'email',
              'phone',
              'address', )

    if not request.method == 'POST':
        return {
            'shopper_data': {
                field: getattr(shopper, field) for field in fields
                if getattr(shopper, field)
            }
        }

    new_order = None
    errors = []

    # Подтверждение заказа
    shopper_data = {}
    for field in fields:
        value = request.POST.get(field)
        shopper_value = getattr(shopper, field)
        if not value and shopper_value:
            value = shopper_value
        elif value and not shopper_value:
            Shopper.objects.filter(pk=shopper.id).update(**{field: value})
            setattr(shopper, field, value)
        shopper_data[field] = value

    save_user_to_request(request, shopper)

    email = check_email(shopper_data['email'])
    if not email:
        errors.append('Неправильно указан email')
    phone = check_phone(shopper_data['phone'])
    if not phone:
        errors.append('Неправильно указан телефон')
    if not shopper_data['name']:
        errors.append('Укажите как к вам обращаться')
    if not errors:
        # Оформление заказа
        purchases = cart.get('purchases')
        new_order = Orders.objects.create(
            total=cart['total'],
            shopper=shopper,
            shopper_ip=get_request_ip(request),
            shopper_name=shopper_data['name'],
            shopper_email=shopper_data['email'],
            shopper_phone=shopper_data['phone'],
            shopper_address=shopper_data['address'],
            state=2,
        )
        for purchase in purchases:
            Purchases.objects.filter(pk=purchase.id).update(order=new_order)
    return {
        'order': new_order,
        'errors': errors,
        'shopper_data': shopper_data,
    }
