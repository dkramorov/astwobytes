# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect

from apps.flatcontent.models import Blocks
from apps.flatcontent.views import SearchLink
from apps.flatcontent.flatcat import get_cat_for_site, get_product_for_site
from apps.main_functions.views import DefaultFeedback
from apps.main_functions.api_helper import open_wb, search_header
from apps.main_functions.catcher import check_email
from apps.products.models import Products
from apps.personal.oauth import VK, Yandex
from apps.personal.utils import remove_user_from_request
from apps.shop.cart import calc_cart, get_shopper, create_new_order
from apps.shop.models import Transactions

from .yandex_kassa import YandexKassa

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
    if not context.get('catalogue'):
        raise Http404
    containers = {}

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/cat/%slist.html' % (mh_vars['template_prefix'], )

    page = SearchLink(context['q_string'], request, containers)
    if page:
        context['page'] = page
    context['containers'] = containers

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
    containers = {}

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
    'singular_obj': 'Регистрация',
    'template_prefix': 'main_',
    'show_urla': 'registration',
}

def registration(request):
    """Страничка для регистрации"""
    mh_vars = reg_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/login/registration.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=mh_vars['singular_obj'])
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
    comments = None
    wrist_size = request.POST.get('wrist_size')
    birthday = request.POST.get('birthday')
    if wrist_size or birthday:
        comments = []
        if wrist_size:
            comments.append('Размер запястья %s' % wrist_size)
        if birthday:
            comments.append('День рождения %s' % birthday)
        comments = ', '.join(comments)

    context.update(**create_new_order(request, shopper, cart, comments))
    if 'order' in context and context['order']:
        template = 'web/order/confirmed.html'
        payment = YandexKassa().create_payment(
            domain = '%s%s' % ('https://' if request.is_secure() else 'http://',
                               request.META['HTTP_HOST']),
            summa = '%s' % context['order'].total,
            desc = 'Оплата заказа №%s' % context['order'].id,
        )
        if 'confirmation' in payment:
            context['yandex_payment_link'] = payment['confirmation']['confirmation_url']
            Transactions.objects.create(order=context['order'], uuid=payment['id'], ptype=1)

    return render(request, template, context)

def transaction_success(request):
    """Оформление заказа - Успешная оплата"""
    mh_vars = order_vars.copy()
    context = {}
    q_string = {}
    containers = {}
    shopper = get_shopper(request)

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=order_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Заказ оплачен',
        'link': reverse('%s:%s' % (CUR_APP, 'transaction_success')),
    }]

    context['page'] = page
    context['containers'] = containers
    template = 'web/order/transaction_success.html'

    return render(request, template, context)

def promocode_by_email(request):
    """Промокод по емайлу из эксель файла
       :param request: HttpRequest
    """
    context = {}

    method = request.GET
    if request.method == 'POST':
        method = request.POST
    search_email = check_email(method.get('email'))
    if not search_email:
        return JsonResponse(context, safe=False)

    wb = open_wb('promocodes.xlsx')
    sheet = wb.active

    i, row = search_header(sheet.rows, symbols='email')
    icode = None
    iemail = None
    j = 0
    for cell in row:
        if cell.value == 'code':
            icode = j
        elif cell.value == 'email':
            iemail = j
        j += 1
    for row in sheet.rows:
       code = row[icode].value
       email = row[iemail].value
       if not code and not email:
           break
       if email == search_email:
           context['code'] = code

    return JsonResponse(context, safe=False)
