# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings

from django.contrib.auth.decorators import login_required

from apps.products.models import Products
from apps.shop.models import Purchases
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.models import Config
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )
from apps.shop.cart import get_shopper
from apps.addresses.models import Address
from apps.upload_tasks.simaland import SimaLand

from apps.site.simaland.models import PickupPoint

SIMALAND_KEY = 'sima-land.ru'
CODE_PREFIX = 'simaland_'

CUR_APP = 'simaland'
pickup_points_vars = {
    'singular_obj': 'Пункт вывоза',
    'plural_obj': 'Пункты вывоза',
    'rp_singular_obj': 'пункта вывоза',
    'rp_plural_obj': 'пунктов вывоза',
    'template_prefix': 'pickup_points_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'simaland',
    'submenu': 'pickup_points',
    'show_urla': 'show_pickup_points',
    'create_urla': 'create_pickup_point',
    'edit_urla': 'edit_pickup_point',
    'model': PickupPoint,
    #'custom_model_permissions': DemoModel,
    'select_related_list': ('address', 'user', 'order'),
}

def api(request, action: str = 'pickup_points'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'pickup_points':
    #    result = ApiHelper(request, pickup_points_vars, CUR_APP)
    result = ApiHelper(request, pickup_points_vars, CUR_APP)
    return result


pp_only_fields = (
    'id',
    'order__id',
    'order__created',
    'order__total',
    'shopper__id',
    'shopper__name',
    'shopper__email',
    'shopper__phone',
    'shopper__login',
    'address__id',
    'address__addressLines',
    'address__place',
)
pp_fk_keys = {
    'order': ('id',
              'created',
              'total'),
    'shopper': ('id',
                'name',
                'email',
                'phone',
                'login'),
    'address': ('id',
                'addressLines',
                'place'),
}


@login_required
def show_pickup_points(request, *args, **kwargs):
    """Вывод точек вывоза пользователей
       :param request: HttpRequest
    """
    mh_vars = pickup_points_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('shopper')
    mh.select_related_add('address')
    mh.select_related_add('order')
    context = mh.context

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        result = []
        rows = mh.standard_show(only_fields=pp_only_fields)
        for row in rows:
            item = object_fields(row,
                                 only_fields=pp_only_fields,
                                 fk_only_keys=pp_fk_keys)
            item['actions'] = row.id
            result.append(item)
        if request.GET.get('page'):
            result = {'data': result,
                      'last_page': mh.raw_paginator['total_pages'],
                      'total_records': mh.raw_paginator['total_records'],
                      'cur_page': mh.raw_paginator['cur_page'],
                      'by': mh.raw_paginator['by'], }
        return JsonResponse(result, safe=False)
    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def edit_pickup_point(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование пункта вывоза пользователя
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = pickup_points_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('shopper')
    mh.select_related_add('address')
    mh.select_related_add('order')
    row = mh.get_row(row_id)
    context = mh.context # Контекст дозаполняется в get_row

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        if action == 'create':
            mh.breadcrumbs_add({
                'link': mh.url_create,
                'name': '%s %s' % (mh.action_create, mh.rp_singular_obj),
            })
        elif action == 'edit' and row:
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
            })
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
    elif request.method == 'POST':
        pass_fields = ()
        mh.post_vars(pass_fields=pass_fields)
        if action == 'create' or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
    if mh.row:
        context['row'] = object_fields(mh.row,
                                       only_fields=pp_only_fields,
                                       fk_only_keys=pp_fk_keys)
        context['redirect'] = mh.get_url_edit()
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

simaland_vars = {
    'singular_obj': SIMALAND_KEY,
    'plural_obj': SIMALAND_KEY,
    'rp_singular_obj': SIMALAND_KEY,
    'rp_plural_obj': SIMALAND_KEY,
    'template_prefix': 'simaland_',
    'menu': 'simaland',
    'submenu': 'simaland',
    'cart_urla': 'simaland_cart',
    'cart_singular_obj': 'Корзина покупок',
    'order_singular_obj': 'Заказы',
    'credentials_urla': 'simaland_credentials',
    'credentials_singular_obj': 'Настройки аккаунта',
}

def simaland_breadcrumbs(context):
    """Заполнение хлебных крошек для sima-land.ru разделов"""
    context['breadcrumbs'] = [{
        'name': SIMALAND_KEY,
        'link': context['root_url'],
    }, {
        'name': context['singular_obj'],
        'link': context['root_url'],
    }]

@login_required
def simaland_credentials(request):
    """Настройки аккаунта sima-land.ru"""
    context = simaland_vars.copy()
    context['singular_obj'] = context['credentials_singular_obj']
    context['submenu'] = 'credentials'
    root_url = reverse('%s:%s' % (CUR_APP, context['credentials_urla']))
    context['root_url'] = root_url

    # Сохранение учетных данных для интеграции
    if request.method == 'POST':
        login = request.POST.get('login')
        passwd = request.POST.get('passwd')
        if login and passwd:
            config = Config.objects.filter(name=SIMALAND_KEY).first()
            if not config:
                config = Config(name=SIMALAND_KEY)
            simaland = SimaLand(login=login, passwd=passwd)
            try:
                jwt = simaland.get_jwt()
            except Exception:
                jwt = None
            if not jwt:
                context['error'] = 'Авторизация не прошла, данные не сохранены'
            else:
                config.attr = login
                config.value = passwd
                config.save()
                return redirect(root_url)

    simaland_breadcrumbs(context)

    row = Config.objects.filter(name=SIMALAND_KEY).first()
    if row:
        context['row'] = row
    template = '%scredentials.html' % (context['template_prefix'], )
    return render(request, template, context)

@login_required
def simaland_cart(request):
    """Апи по корзинке товаров sima-land.ru"""
    context = simaland_vars.copy()
    context['singular_obj'] = context['cart_singular_obj']
    context['submenu'] = 'cart'
    root_url = reverse('%s:%s' % (CUR_APP, context['cart_urla']))
    context['root_url'] = root_url

    simaland_breadcrumbs(context)

    row = Config.objects.filter(name=SIMALAND_KEY).first()
    simaland = None
    cart = None
    if row:
        context['row'] = row
        simaland = SimaLand(login=row.attr, passwd=row.value)
        cart = simaland.get_cart()
        new_cart = {}
        if cart:
            for k, v in cart.items():
                if k.startswith('_'):
                    new_cart[k[1:]] = v
                else:
                    new_cart[k] = v
        #print(json_pretty_print(context['cart']))
        codes = ['%s%s' % (CODE_PREFIX, item['item_id']) for item in new_cart['items']]
        products = Products.objects.filter(code__in=codes)
        ids_products = {
            int(product.code.replace(CODE_PREFIX, '')): product
            for product in products
        }
        for item in new_cart['items']:
            product = ids_products.get(item['item_id'])
            item['product'] = product
        cart = new_cart
        context['cart'] = cart
    # -----------------------
    # Перезаполнение корзинки
    # -----------------------
    if request.GET.get('refill_cart') and simaland and cart:
        cart_id = cart['cart']['cart_id']
        for item in cart['items']:
            simaland.clear_cart(item['id'])
        purchases = Purchases.objects.filter(order__state=2, product_code__startswith=CODE_PREFIX)
        multiplicity_products = {}
        accumulate = {}
        for purchase in purchases:
            code = int(purchase.product_code.replace(CODE_PREFIX, ''))
            if not code in accumulate:
                accumulate[code] = 0
            if purchase.product_multiplicity:
                multiplicity_products[code] = {
                    'mul': purchase.product_multiplicity,
                    'min': purchase.product_min_count,
                }
            accumulate[code] += purchase.count

        # Фикс на кратные товары
        for key in accumulate.keys():
            if key in multiplicity_products:
                count = accumulate[key]
                mul = multiplicity_products[key]['mul']
                min_count = multiplicity_products[key]['min']
                diff = count / mul
                int_diff = int(diff)
                # Может оказаться нехватка до минимального кол-ва,
                # поэтому добиваем до минимального
                if (int_diff * mul) < min_count:
                    accumulate[key] = min_count
                else:
                    accumulate[key] = int_diff
                    if diff - int_diff > 0:
                        accumulate[key] = (int_diff + 1) * mul

        items = [{'item_id': k, 'qty': v} for k, v in accumulate.items()]
        simaland.add2cart(cart_id=cart_id, items=items)

        return redirect(root_url)

    template = '%scart.html' % (context['template_prefix'], )
    return render(request, template, context)

@login_required
def simaland_orders(request):
    """Апи по заказам sima-land.ru"""
    context = simaland_vars.copy()
    context['singular_obj'] = context['order_singular_obj']
    context['submenu'] = 'orders'
    root_url = reverse('%s:%s' % (CUR_APP, context['cart_urla']))
    context['root_url'] = root_url

    simaland_breadcrumbs(context)

    row = Config.objects.filter(name=SIMALAND_KEY).first()
    simaland = None
    if row:
        context['row'] = row
        simaland = SimaLand(login=row.attr, passwd=row.value)
        orders = simaland.get_orders()
        context['orders'] = orders['items']
        context['pages'] = orders['_meta']

    template = '%sorders.html' % (context['template_prefix'], )
    return render(request, template, context)

def get_pickup_point(request, *args, **kwargs):
    """Получение точки вывоза для пользователя
       :param request: HttpRequest
    """
    result = {}
    shopper = get_shopper(request)
    if shopper:
        pickup_point = PickupPoint.objects.select_related('shopper', 'order', 'address').filter(order__isnull=True, shopper=shopper).first()
        if pickup_point:
            result = object_fields(pickup_point,
                                   only_fields=pp_only_fields,
                                   fk_only_keys=pp_fk_keys)
    return JsonResponse(result, safe=False)

def set_pickup_point(request, *args, **kwargs):
    """Задание точки вывоза для пользователя
       :param request: HttpRequest
    """
    result = {}
    point_id = request.GET.get('point_id')
    shopper = get_shopper(request)
    if shopper and point_id:
        address = Address.objects.filter(pk=point_id).first()
        if address:
            analog = PickupPoint.objects.filter(order__isnull=True, shopper=shopper).first()
            if analog:
                analog.address = address
            else:
                analog = PickupPoint(shopper=shopper, address=address)
            analog.save()
            result['success'] = 1
    return JsonResponse(result, safe=False)
