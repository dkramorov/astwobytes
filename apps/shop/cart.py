# -*- coding:utf-8 -*-
import logging
from django.conf import settings

from apps.personal.models import Shopper
from apps.personal.utils import save_user_to_request
from apps.products.models import Products
from apps.flatcontent.flatcat import get_costs_types
from apps.main_functions.string_parser import get_request_ip, summa_format
from apps.main_functions.catcher import check_email, check_phone

from apps.shop.models import Orders, Purchases, PromoCodes

logger = logging.getLogger('main')

def get_purchase(pk: int,
                 shopper: Shopper,
                 is_purchase: bool = True,
                 cost_type = None):
    """Вытащить из базы покупку,
       покупка должна быть без заказа,
       принадлежать переданному пользователю
       :param pk: ид покупки или товара
       :param shopper: пользователь
       :param is_purchase: ищем ид покупки, иначе ид товара
       :param cost_type: тип цены - для доп сравнения по is_purchase=False
       :return: Purchase object
    """
    result = Purchases.objects.filter(order__isnull=True, shopper=shopper)
    if is_purchase:
        result = result.filter(pk=pk)
    else:
        result = result.filter(product_id=pk)
        if cost_type:
            result = result.filter(cost_type=cost_type)
    return result.first()

def calc_cart(shopper, min_info: bool = False):
    """Корзинка пользователя
       :param shopper: покупатель Shopper или json из сессии
       :param min_info: с товарами или без
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
    promocode = None
    if isinstance(shopper, dict):
        shopper_id = shopper.get('id')
        promocode = shopper.get('promocode')
    elif isinstance(shopper, Shopper):
        shopper_id = shopper.id
        if hasattr(shopper, 'promocode'):
            promocode = shopper.promocode
    if not shopper_id:
        return {}

    result = {}
    purchases = Purchases.objects.filter(shopper=shopper_id, order__isnull=True).order_by('position')
    if not purchases:
        return result

    total = 0
    items = 0 # Количество наименований
    items_count = 0 # Количество товаров
    discount = 0 # Скидка

    ids_products = {}
    for purchase in purchases:
        total += purchase.cost * purchase.count
        items += 1
        items_count += purchase.count
        ids_products[purchase.product_id] = None

    result = {
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
    if promocode:
        pcode = PromoCodes.objects.filter(pk=promocode, is_active=True).first()
        if pcode and pcode.is_valid(shopper_id=shopper_id):
            if pcode.percent and pcode.percent > 0 and pcode.percent < 100:
                one_percent = total / 100
                discount = int(one_percent * pcode.percent)
            elif pcode.value and total > pcode.value:
                discount = pcode.value
            result['promocode'] = pcode.code
    if discount:
        result['discount'] = discount
        result['total_with_discount'] = total - discount

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
    promocode = request.session.get('promocode')
    if not guest_enter:
        if isinstance(shopper, dict):
            user = Shopper()
            for k, v in shopper.items():
                setattr(user, k, v)
            if promocode:
                user.promocode = promocode
            return user
        if shopper:
            shopper.promocode = promocode
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
    shopper.promocode = promocode
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

def create_new_order(request, shopper, cart, comments: str = None):
    """Оформление заказа пользователем,
       нажатие кнопки на сайте Оформить заказ
       :param request: HttpRequest
       :param shopper: покупатель
       :param cart: корзинка пользователя
       :param comments: комментарий к заказу (доп инфа)
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
        promocode = None
        if cart.get('promocode'):
            promocode_id = request.session.get('promocode')
            promocode = PromoCodes.objects.filter(pk=promocode_id).first()
        new_order = Orders.objects.create(
            total=cart['total_with_discount'],
            discount=cart['discount'],
            promocode=promocode,
            shopper=shopper,
            shopper_ip=get_request_ip(request),
            shopper_name=shopper_data['name'],
            shopper_email=shopper_data['email'],
            shopper_phone=shopper_data['phone'],
            shopper_address=shopper_data['address'],
            state=2,
            comments=comments,
        )
        purchases = cart.get('purchases')
        for purchase in purchases:
            Purchases.objects.filter(pk=purchase.id).update(order=new_order)
        if 'promocode' in request.session:
            del request.session['promocode']

        scheme = 'https://' if request.is_secure() else 'http://'
        domain = '%s%s' % (scheme, request.META['HTTP_HOST'])
        notify_about_order(new_order, purchases, domain=domain)
    return {
        'order': new_order,
        'errors': errors,
        'shopper_data': shopper_data,
    }

def notify_about_order(order: Orders, purchases: list, domain: str = None):
    """Оповещение о заказе через телеграм
       :param order: экземпляр заказа
       :param purchases: покупки
       :param domain: адрес сайта
    """
    if not settings.TELEGRAM_ENABLED:
        logger.info('TELEGRAM DISABLED')
        return
    from apps.telegram.telegram import TelegramBot
    bot = TelegramBot()
    bot.send_message('%s Заказ <a href="%s/shop/admin/orders/view/%s/">№%s</a>, на сумму %s ₽ от %s' % (
        bot.get_emoji('hot'),
        domain,
        order.id,
        order.number or order.id,
        summa_format(order.total),
        order.created.strftime('%H:%M:%S %d-%m-%Y')
    ), parse_mode='html', disable_web_page_preview=True)
    msg = ''
    for i, purchase in enumerate(purchases):
        msg += '%s. <a href="%s/product/%s/">%s</a> x %s (%s ₽) = %s ₽\n' % (
            i + 1,
            domain,
            purchase.product_id,
            purchase.product_name,
            purchase.count,
            summa_format(purchase.cost),
            summa_format(purchase.total()),
        )
    msg += '\nПользователь:\n'
    if order.shopper_name:
         msg += 'Имя: %s\n' % order.shopper_name
    if order.shopper_email:
         msg += 'Email: %s\n' % order.shopper_email
    if order.shopper_phone:
         msg += 'Телефон: %s\n' % order.shopper_phone
    if order.shopper_address:
         msg += 'Адрес: %s\n' % order.shopper_address
    if order.shopper_ip:
         msg += 'ip: %s\n' % order.shopper_ip

    if order.promocode:
        msg += 'Промокод: %s\n' % order.promocode.code
    if order.discount:
        msg += 'Скидка на заказ %.2f\n' % order.disount
    if order.comments:
        msg += 'Комментарий: %s\n' % order.comments
    msg += '-------------------'
    bot.send_message(msg, parse_mode='html', disable_web_page_preview=True)
