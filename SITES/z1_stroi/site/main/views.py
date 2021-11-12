# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings

from apps.flatcontent.models import Containers, Blocks
from apps.flatcontent.views import SearchLink
from apps.flatcontent.flatcat import (get_cat_for_site,
                                      get_product_for_site,
                                      get_catalogue_lvl,
                                      get_props_for_products, )
from apps.main_functions.string_parser import q_string_fill
from apps.main_functions.views import DefaultFeedback
from apps.products.models import Products
from apps.products.views import get_products_cats
from apps.personal.oauth import VK, Yandex
from apps.personal.utils import save_user_to_request, remove_user_from_request
from apps.personal.auth import register_from_site, login_from_site, update_profile_from_site
from apps.shop.cart import calc_cart, get_shopper, create_new_order
from apps.shop.order import get_order
from apps.shop.models import Orders, WishList

CUR_APP = 'main'
main_vars = {
    'singular_obj': 'Главная',
    'template_prefix': 'main_',
    'show_urla': 'home',
}

def home(request):
    """Главная страничка сайта"""
    mh_vars = main_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/main.html'

    page = SearchLink(q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)

demo_vars = {
    'singular_obj': 'Демо-страничка',
    'template_prefix': 'demo_',
    'show_urla': 'demo',
}

def demo(request):
    """Страничка для разработки"""
    mh_vars = demo_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/demo.html'

    page = SearchLink(q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)

cat_vars = {
    'singular_obj': 'Каталог',
    'template_prefix': 'cat_',
    'show_urla': 'cat',
}


def main_rubrics(request):
    """Страничка с рубриками каталога
    """
    mh_vars = cat_vars.copy()
    context = {}
    containers = {}
    q_string = {}
    breadcrumbs = []

    q_string_fill(request, q_string)

    root_catalogue = Containers.objects.filter(tag='catalogue').first()
    breadcrumbs.append({'name': 'Все категории', 'link': '/rubrics/'})
    top_level = root_catalogue.blocks_set.filter(parents='')

    ids_top_level = {'_%s' % item.id: item for item in top_level}
    sub_levels = root_catalogue.blocks_set.filter(parents__in=ids_top_level)
    for sub_level in sub_levels:
        parent = ids_top_level[sub_level.parents]
        if not hasattr(parent, 'sub'):
            parent.sub = []
        parent.sub.append(sub_level)


    context['catalogue'] = root_catalogue
    context['top_level'] = top_level
    context['breadcrumbs'] = breadcrumbs

    page = SearchLink(q_string, request, containers)
    if page:
        context['page'] = page
    else:
        context['page'] = Blocks(name='Каталог товаров')
    context['containers'] = containers
    template = 'web/cat/%srubrics.html' % (mh_vars['template_prefix'], )
    return render(request, template, context)

def cat_on_site(request, link: str = None):
    """Странички каталога
       :param link: ссылка на рубрику (без /cat/ префикса)
    """
    mh_vars = cat_vars.copy()
    kwargs = {
        'q_string': {
            'by': 30,
        },
    }

    context = get_cat_for_site(request, link, **kwargs)
    if not context.get(settings.DEFAULT_CATALOGUE_TAG):
        raise Http404
    containers = {}

    if request.is_ajax():
        return JsonResponse(context, safe=False)

    page = context['page']
    if not page.parents:
        context['subcats'] = Blocks.objects.filter(parents='_%s' % page.id)

    template = 'web/cat/%slist.html' % (mh_vars['template_prefix'], )

    page = SearchLink(context['q_string'], request, containers)
    if page:
        context['page'] = page
    context['containers'] = containers

    return render(request, template, context)

def product_by_link(request, link: str):
    """Вытаскиваем код товара по ссылке и возвращаем товар
       :param request: HttpRequest
       :param link: ссылка на товар по транслит-названию-код
    """
    code = link.split('-')[-1]
    code = code.replace('/', '')
    product = Products.objects.filter(code=code).only('id').first()
    if product:
        return product_on_site(request, product.id)
    raise Http404

def product_on_site(request, product_id: int):
    """Страничка товара/услуги
       :param product_id: ид товара/услуги
    """
    mh_vars = cat_vars.copy()
    context = get_product_for_site(request, product_id)
    if not context.get('product'):
        raise Http404
    q_string = {}
    containers = {'main': None, 'services2': None, 'products_tabs': None}

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/cat/%sproduct.html' % (mh_vars['template_prefix'], )

    page = SearchLink(q_string, request, containers)
    context['page'] = page
    if not page:
        context['page'] = Blocks()
        context['page'].containers = containers.values()
    context['containers'] = containers

    return render(request, template, context)

def feedback(request):
    """Страничка обратной связи"""
    kwargs = {
        #'force_send': 1, # Принудительная отправка
        #'fv': [],
        #'dummy': 1, # Не возвращаем HttpResponse
        #'do_not_send': 1, # Не отправляем письмо
        'fields':[
          {'name': 'test_field', 'value': 'Тестовое поле'},
        ],
    }
    return DefaultFeedback(request, **kwargs)

reg_vars = {
    'singular_obj': 'Вход/Регистрация',
    'template_prefix': 'main_',
    'show_urla': 'registration',
}

def registration(request):
    """Страничка для регистрации"""
    mh_vars = reg_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    shopper = get_shopper(request)
    if shopper:
        return redirect(reverse('%s:%s' % (CUR_APP, 'show_profile')))
    # -----------
    # регистрация
    # -----------
    if request.method == 'POST':
        result = register_from_site(request)
        if isinstance(result, list):
             context['errors'] = result;
        else:
             save_user_to_request(request, result)
             context['shopper'] = result.to_dict()
             context['redirect'] = reverse('%s:%s' % (CUR_APP, 'show_profile'))

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/login/registration.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=reg_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': mh_vars['singular_obj'],
        'link': reverse('%s:%s' % (CUR_APP, 'registration')),
    }]
    context['page'] = page
    context['containers'] = containers
    context['vk_link'] = VK().get_auth_user_link()
    context['yandex_link'] = Yandex().get_auth_user_link()

    return render(request, template, context)

profile_vars = {
    'singular_obj': 'Ваш аккаунт',
    'template_prefix': 'main_',
    'show_urla': 'profile',
}

def show_profile(request):
    """Личный кабинет пользователя"""
    mh_vars = profile_vars.copy()
    context = {}
    q_string = {}
    containers = {}
    shopper = get_shopper(request)
    if not shopper:
        return redirect(reverse('%s:%s' % (CUR_APP, 'registration')))

    if request.method == 'POST':
        result = update_profile_from_site(request)
        if isinstance(result, list):
             context['errors'] = result;
        else:
             save_user_to_request(request, result)
             context['shopper'] = result.to_dict()
             context['redirect'] = reverse('%s:%s' % (CUR_APP, 'show_profile'))

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/login/profile.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=mh_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Ваш аккаунт',
        'link': reverse('%s:%s' % (CUR_APP, 'show_profile')),
    }]

    context['page'] = page
    context['containers'] = containers
    context['shopper'] = shopper

    return render(request, template, context)

def show_orders(request):
    """История заказов пользователя"""
    mh_vars = profile_vars.copy()
    context = {}
    q_string = {}
    containers = {}
    shopper = get_shopper(request)
    if not shopper:
        return redirect(reverse('%s:%s' % (CUR_APP, 'registration')))

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/login/orders.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=mh_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Ваш аккаунт',
        'link': reverse('%s:%s' % (CUR_APP, 'show_profile')),
    }, {
        'name': 'История заказов',
        'link': reverse('%s:%s' % (CUR_APP, 'show_orders')),
    }]

    context['page'] = page
    context['containers'] = containers
    context['shopper'] = shopper
    context['orders'] = Orders.objects.filter(shopper=shopper).order_by('-created')[:50]
    return render(request, template, context)

def login(request):
    """Авторизация пользователя"""
    context = {}
    q_string = {}
    containers = {}
    result = login_from_site(request)
    if isinstance(result, list):
        context['errors'] = result
    else:
        save_user_to_request(request, result)
        context['shopper'] = result.to_dict()
        context['redirect'] = reverse('%s:%s' % (CUR_APP, 'show_profile'))

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/login/registration.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=reg_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Регистрация',
        'link': reverse('%s:%s' % (CUR_APP, 'registration')),
    }]
    context['page'] = page
    context['containers'] = containers
    context['vk_link'] = VK().get_auth_user_link()
    context['yandex_link'] = Yandex().get_auth_user_link()

    return render(request, template, context)

def logout(request):
    """Деавторизация пользователя"""
    remove_user_from_request(request)
    return redirect(reverse('%s:%s' % (CUR_APP, 'registration')))

cart_vars = {
    'singular_obj': 'Корзина',
    'template_prefix': 'cart_',
    'show_urla': 'cart',
}

def show_cart(request):
    """Оформление заказа - Корзинка"""
    mh_vars = cart_vars.copy()
    context = {}
    q_string = {}
    containers = {}
    shopper = get_shopper(request)

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/order/cart.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=mh_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Корзина',
        'link': reverse('%s:%s' % (CUR_APP, 'show_cart')),
    }]

    context['page'] = page
    context['containers'] = containers
    context['cart'] = calc_cart(shopper, min_info=False)

    return render(request, template, context)

checkout_vars = {
    'singular_obj': 'Подтверждение заказа',
    'template_prefix': 'order_',
    'show_urla': 'cart',
}

def checkout(request):
    """Оформление заказа - Подтверждение заказа"""
    mh_vars = checkout_vars.copy()
    context = {}
    q_string = {}
    containers = {}
    shopper = get_shopper(request)

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/order/checkout.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=checkout_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Корзина',
        'link': reverse('%s:%s' % (CUR_APP, 'show_cart')),
    }, {
        'name': 'Подтверждение заказа',
        'link': reverse('%s:%s' % (CUR_APP, 'checkout')),
    }]

    context['yandex_maps_api_key'] = settings.YANDEX_MAPS_API_KEY
    context['page'] = page
    context['containers'] = containers
    cart = calc_cart(shopper, min_info=False)
    context['cart'] = cart

    # Оформление заказа
    context.update(**create_new_order(request, shopper, cart))
    if 'order' in context and context['order']:
        template = 'web/order/confirmed.html'

    # Если пользователь вернулся
    # на страничку оформленного заказа,
    # например, для оплаты
    if request.GET.get('order_id'):
        order_id = request.GET['order_id']
        if order_id.isdigit():
            order = Orders.objects.filter(pk=order_id, shopper=shopper).first()
            if order:
                template = 'web/order/confirmed.html'
                context['order'] = order

    return render(request, template, context)

order_vars = {
    'singular_obj': 'Заказ',
    'template_prefix': 'order_',
    'show_urla': 'show_order',
}

def show_order(request, order_id: int):
    """Просмотр оформленного заказа"""
    mh_vars = order_vars.copy()
    context = {}
    q_string = {}
    containers = {}
    shopper = get_shopper(request)

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/order/order.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=mh_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Ваш аккаунт',
        'link': reverse('%s:%s' % (CUR_APP, 'show_profile')),
    }, {
        'name': 'История заказов',
        'link': reverse('%s:%s' % (CUR_APP, 'show_orders')),
    }, {

        'name': 'Заказ',
        'link': reverse('%s:%s' % (CUR_APP, 'show_order'),
                        kwargs={'order_id': order_id}),
    }]

    context['page'] = page
    context['containers'] = containers
    result = get_order(shopper, order_id)
    context['cart'] = result.get('cart', {})
    context['cart']['purchases'] = result.get('purchases', [])
    context['order'] = result.get('order')

    return render(request, template, context)

compare_vars = {
    'singular_obj': 'Сравнение товаров',
    'template_prefix': 'compare_',
    'show_urla': 'compare',
}

def compare(request):
    """Сравнение товаров"""
    mh_vars = compare_vars.copy()
    context = {}
    q_string = {}
    containers = {}
    shopper = get_shopper(request)
    state = 2

    if shopper:
        compare_list = WishList.objects.select_related('product').filter(shopper=shopper, state=state)
        compare_list = [item.product for item in compare_list if item.product]
        context['products'] = compare_list

        ids_products = {item.id: [] for item in compare_list}
        get_products_cats(ids_products, 'catalogue')
        get_props_for_products(compare_list)
        all_props = {}
        for item in compare_list:
            if item.id in ids_products:
                item.cats = ids_products[item.id]
            if not hasattr(item, 'props'):
                continue
            for prop in item.props:
                if not prop['prop']['id'] in all_props:
                    all_props[prop['prop']['id']] = prop['prop']['name']
        context['all_props'] = all_props

    template = 'web/cat/compare.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=mh_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Сравнение товаров',
        'link': reverse('%s:%s' % (CUR_APP, 'compare')),
    }]

    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)
