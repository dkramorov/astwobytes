# -*- coding:utf-8 -*-
import json
import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings

from apps.flatcontent.models import Blocks
from apps.flatcontent.views import SearchLink
from apps.flatcontent.flatcat import get_cat_for_site, get_product_for_site
from apps.main_functions.views import DefaultFeedback
from apps.products.models import Products
from apps.personal.oauth import VK, Yandex
from apps.personal.utils import save_user_to_request, remove_user_from_request
from apps.personal.auth import register_from_site, login_from_site, update_profile_from_site
from apps.shop.cart import calc_cart, get_shopper, create_new_order
from apps.shop.models import Orders
from apps.shop.sbrf import SberPaymentProvider

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
        return JsonResponse(context, safe=False)
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
                sber = SberPaymentProvider()
                order_status = sber.get_order_status(order.external_number, order.id)
                context['order_status'] = order_status
    # -----------------------------------------
    # Если пользователь пытается оплатить заказ
    # -----------------------------------------
    if 'order' in context and request.GET.get('pay') == 'sbrf':
        order = context['order']
        scheme = 'http://'
        if request.is_secure():
            scheme = 'https://'
        host = '%s%s' % (scheme, request.META['HTTP_HOST'])
        env = ''
        if settings.DEBUG:
            env = 'test_%s' % str(time.time())
        params = {
            'amount': int(order.total * 100),
            'orderNumber': '%s%s' % (env, order.id),
            'returnUrl': '%s/payment/sbrf/success/' % host,
            'failUrl': '%s/payment/sbrf/fail/' % host,
            #'description': 'Тестовый заказ',
            'clientId': shopper.id,
            'email': shopper.email,
            'phone': shopper.phone,
        }
        sber = SberPaymentProvider()
        register_order = sber.register_do(**params)
        context.update(register_order)
        # ------------------------
        # Переадресация на форму и
        # запись номера заказа
        # ------------------------
        if 'formUrl' in register_order:
            Orders.objects.filter(pk=order.id).update(external_number=register_order['orderId'])
            return redirect(register_order['formUrl'])
    return render(request, template, context)


payment_vars = {
    'singular_obj': 'Оплата заказа',
    'template_prefix': 'order_',
    'show_urla': 'payment',
}

def payment(request, provider: str, action: str):
    """Оплата заказа
       :param request: HttpRequest
       :param provider: sbrf/
       :param action: success/fail
    """
    mh_vars = payment_vars.copy()
    context = {
        'provider': provider,
        'action': action,
    }
    q_string = {}
    containers = {}
    shopper = get_shopper(request)

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/order/payment.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=order_vars['singular_obj'])
    kwargs = {
      'provider': provider,
      'action':action,
    }
    context['breadcrumbs'] = [{
        'name': 'Оплата заказа',
        'link': reverse('%s:%s' % (CUR_APP, 'payment'), kwargs=kwargs),
    }]

    context['page'] = page
    context['containers'] = containers

    if request.GET.get('orderId'):
        order_id = request.GET['orderId']
        order = Orders.objects.filter(shopper=shopper, external_number=order_id).first()
        if order:
            sber = SberPaymentProvider()
            order_status = sber.get_order_status(order.external_number, order.id)
            context['order_status'] = order_status
            context['order'] = order

    return render(request, template, context)
