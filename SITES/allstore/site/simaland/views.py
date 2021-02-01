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
from apps.upload_tasks.simaland import SimaLand
from apps.site.main.views import CUR_APP

SIMALAND_KEY = 'sima-land.ru'
CODE_PREFIX = 'simaland_'
simaland_vars = {
    'singular_obj': SIMALAND_KEY,
    'plural_obj': SIMALAND_KEY,
    'rp_singular_obj': SIMALAND_KEY,
    'rp_plural_obj': SIMALAND_KEY,
    'template_prefix': 'simaland/',
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
