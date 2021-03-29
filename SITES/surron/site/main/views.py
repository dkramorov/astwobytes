# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings

from apps.flatcontent.models import Blocks
from apps.flatcontent.views import SearchLink
from apps.flatcontent.flatcat import get_cat_for_site, get_product_for_site, get_catalogue_lvl
from apps.main_functions.views import DefaultFeedback
from apps.products.models import Products
from apps.personal.oauth import VK, Yandex
from apps.personal.utils import save_user_to_request, remove_user_from_request
from apps.personal.auth import register_from_site, login_from_site, update_profile_from_site
from apps.shop.cart import calc_cart, get_shopper, create_new_order
from apps.shop.models import Orders

from apps.site.product_colors.models import ProductColor

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
        # Если запрос по фасетному поиску,
        # отдаем отрендеренный шаблон
        if request.GET.get('ff'):
            context = {
                'plp': render_to_string('web/cat/plp.html', context),
                'my_paginator': context['my_paginator'],
            }
        return JsonResponse(context, safe=False)
    template = 'web/cat/%slist.html' % (mh_vars['template_prefix'], )

    page = SearchLink(context['q_string'], request, containers)
    if page:
        context['page'] = page
    context['containers'] = containers

    return render(request, template, context)

def cat_lvl(request):
    """Аякс запрос по рубрике и получение подрубрик этой рубрики
    """
    container_id = request.GET.get('container_id')
    cat_id = request.GET.get('node_id')
    force_new = True if request.GET.get('force_new') else False
    context = get_catalogue_lvl(request,
                                container_id=container_id,
                                cat_id=cat_id,
                                force_new=force_new)
    selected_id = request.GET.get('selected_id')
    selected = Blocks.objects.filter(pk=selected_id).first()
    if selected:
        if not selected.parents:
            for item in context:
                if selected.id == item['id']:
                    item['state']['opened'] = True
        else:
            parents = [int(parent) for parent in selected.parents.split('_') if parent]
            for item in context:
                if item['id'] in parents:
                    item['state']['opened'] = True
        for item in context:
            if selected.id == item['id']:
                item['state']['selected'] = True

    for item in context:
        item['icon'] = '/media/misc/crystall_icon.png'

    return JsonResponse(context, safe=False)

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
    colors = (
        '6', #'Зеленый',
        '1', #'Красный',
        '2', #'Черный',
        '3', #'Живые фото',
        '8', #'Серебристый',
        '7', #'Серый',
        '5', #'Синий',
        '4', #'Желтый',
    )
    live_photos_id = '3'

    mh_vars = cat_vars.copy()
    context = get_product_for_site(request, product_id)
    if not context.get('product'):
        raise Http404
    q_string = {}
    containers = {}

    photos = {}
    sorted_photos = []
    main_section = None
    z = 0

    main_color = '0'
    product_color = ProductColor.objects.filter(product=product_id).first()
    if product_color:
        main_color = product_color.color

    # Разбивка фоток
    for photo in context.get('photos', []):
        if not photo.name:
            photo.name = '0'
        if not photo.name in photos:
            photos[photo.name] = []
        photos[photo.name].append(photo)

        if photo.name in colors:
            ind = colors.index(photo.name)
            if not main_section == 0 or main_section > ind:
                main_section = z
        z += 1

    sorted_photos = [{
        'section_id': color,
        'photos': photos[color],
    } for color in colors if color in photos and color != live_photos_id]

    context['live_photos'] = photos.get(live_photos_id)
    context['photo_sections'] = sorted_photos

    if sorted_photos:
        context['photo_main_section_id'] = main_color or sorted_photos[0]['section_id']

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/cat/%sproduct.html' % (mh_vars['template_prefix'], )

    page = SearchLink(q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)

def feedback(request):
    """Страничка обратной связи"""
    kwargs = {
        'force_send': 1, # Принудительная отправка
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

def logout(request):
    """Деавторизация пользователя"""
    remove_user_from_request(request)
    return redirect(reverse('%s:%s' % (CUR_APP, 'registration')))

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

order_vars = {
    'singular_obj': 'Подтверждение заказа',
    'template_prefix': 'order_',
    'show_urla': 'cart',
}

def checkout(request):
    """Оформление заказа - Подтверждение заказа"""
    mh_vars = order_vars.copy()
    context = {}
    q_string = {}
    containers = {}
    shopper = get_shopper(request)

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/order/checkout.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=order_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Подтверждение заказа',
        'link': reverse('%s:%s' % (CUR_APP, 'checkout')),
    }]

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
