# -*- coding:utf-8 -*-
import json
import time
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

from apps.flatcontent.models import Blocks
from apps.flatcontent.views import SearchLink
from apps.flatcontent.flatcat import get_cat_for_site, get_product_for_site, get_catalogue_lvl
from apps.main_functions.date_time import date_plus_days, weekdayToStr, monthToStr
from apps.main_functions.views import DefaultFeedback
from apps.main_functions.date_time import str_to_date
from apps.main_functions.files import full_path, open_file
from apps.personal.models import Shopper
from apps.shop.cart import calc_cart, get_shopper, create_new_order, create_shopper
from apps.shop.models import Orders, Purchases
from apps.products.models import Products
from apps.products.views import show_products
from apps.shop.sbrf import SberPaymentProvider
from apps.main_functions.pdf_helper import render_pdf

from apps.site.passport.models import Passport
from apps.site.polis.models import Polis

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

    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        context['product_id'] = product_id

    return render(request, template, context)


@login_required
def custom_show_products(request):
    return show_products(request, **{
        'only_fields': (
            'id',
            'name',
            'code',
            'price',
            'img',
            'is_active',
            'position',
            # Доп поля
            'min_count', # Страховая выплата
            'stock_info', # Стараховая программа
            'count', # Период страхования (в мес)
        ), })

def pdf_order(request, order_id, write2file: bool = False):
    context = {}
    order = Orders.objects.select_related('polis').filter(pk=order_id).first()
    context.update({
        'logo': full_path('misc/soglasie_logo.png'),
        'stamp': full_path('misc/soglasie_stamp.png'),
        'polis': order.polis,
    })

    template = 'web/order/pdf/order.html'
    return render_pdf(
        request,
        template = template,
        context = context,
        download = False,
        fname = 'insurance_%s' % (
            order.id,
        ),
        write2file = write2file,
    )

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
    mh_vars = cat_vars.copy()
    context = get_product_for_site(request, product_id)
    if not context.get('product'):
        raise Http404
    q_string = {}
    containers = {}

    photos = {}
    # Разбивка фоток
    for photo in context.get('photos', []):
        if not photo.name:
            photo.name = "0"
        if not photo.name in photos:
            photos[photo.name] = []
        photos[photo.name].append(photo)
    context['photo_sections'] = photos

    if photos:
        context['photo_main_section_id'] = list(photos.keys())[0]

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/cat/%sproduct.html' % (mh_vars['template_prefix'], )

    page = SearchLink(q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)


def feedback(request):
    """Страничка обратной связи"""
    mh_vars = main_vars.copy()
    context = {}
    q_string = {}
    containers = {}

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


def order_form(request):
    """Страничка оформления заказа"""
    mh_vars = main_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    kwargs = {
        'force_send': 1, # Принудительная отправка
        #'fv': [],
        #'dummy': 1, # Не возвращаем HttpResponse
        #'do_not_send': 1, # Не отправляем письмо
        'fields':[
          {'name': 'test_field', 'value': 'Тестовое поле'},
          {'name': 'insurance_type', 'value': 'Тип страховки'},

          {'name': 'birthday', 'value': 'Дата рождения'},
          {'name': 'started', 'value': 'Дата начала программы'},

          {'name': 'passport_series', 'value': 'Паспорт, серия'},
          {'name': 'passport_number', 'value': 'Паспорт, номер'},
          {'name': 'passport_issued', 'value': 'Паспорт, кем выдан'},
          {'name': 'passport_issued_date', 'value': 'Паспорт, когда выдан'},
          {'name': 'passport_registration', 'value': 'Паспорт, место регистрации'},

        ],
    }

    if request.method == 'POST':
        order_id = None
        # Заполняем паспортные данные, по ним найдем пользователя
        passport_fields = {
            'series': '',
            'number': '',
            'issued': '',
            'issued_date': '',
            'registration': '',
            'birthday': '',
        }
        for key in passport_fields.keys():
            passport_fields[key] = request.POST.get('passport_%s' % key)
        passport = Passport.objects.select_related('shopper').filter(
            series=passport_fields['series'],
            number=passport_fields['number'],
        ).first()
        if not passport:
            passport = Passport()
        for key, value in passport_fields.items():
            if not value:
                continue
            if key in ('birthday', 'issued_date'):
                value = str_to_date(value)
            setattr(passport, key, value)
        passport.save()
        # Заполняем пользователя
        if passport.shopper:
            shopper = passport.shopper
        else:
            shopper = Shopper()
        shopper_fields = {
            'name': '',
            'phone': '',
            'email': '',
        }
        for key in shopper_fields.keys():
            shopper_fields[key] = request.POST.get(key)
            if not shopper_fields[key]:
                continue
            setattr(shopper, key, shopper_fields[key])
        shopper.save()
        request.session['shopper'] = shopper.to_dict()

        passport.shopper = shopper
        passport.save()
        # Заполняем заказ
        product = Products.objects.filter(pk=request.POST.get('product')).first()

        birthday = passport.birthday.strftime('%Y-%m-%d') if passport.birthday else None
        started = str_to_date(request.POST.get('started'))

        if product:
            order = Orders.objects.create(
                total=product.price,
                shopper=shopper,
                shopper_name=shopper.name,
                shopper_email=shopper.email,
                shopper_phone=shopper.phone,
                shopper_address=passport.registration,
                comments='Паспорт: \nСерия: %s, номер: %s \nДата рождения: %s \nКем выдан: %s, когда выдан: %s' % (
                    passport.series,
                    passport.number,
                    birthday,
                    passport.issued,
                    passport.issued_date.strftime('%Y-%m-%d') if passport.issued_date else None,
                )
            )
            order_id = order.id
            purchase = Purchases.objects.create(
                product_id=product.id,
                product_name=product.name,
                product_price=product.price,
                product_code=product.code,
                count=1,
                cost=product.price,
                shopper=shopper,
                order=order,
            )

            ended = None
            if started and product.count:
                ended = date_plus_days(started, product.count * 30) 

            polis = Polis.objects.create(
                order = order,
                number = order_id,
                name = shopper.name,
                birthday = birthday,
                insurance_sum = product.min_count,
                insurance_program = product.stock_info,
                from_date = started,
                to_date = ended)

        DefaultFeedback(request, **kwargs)

        return redirect('/shop/checkout/?order_id=%s' % order_id)
    template = 'web/thanks.html'

    page = SearchLink(q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)


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

    delivery_additional_fields = [
        'up2floor',
        'floor',
        'elevator1',
        'elevator2',
        'elevator3',
        'loaders',
        'distance',
    ]

    # Оформление заказа
    context.update(**create_new_order(request, shopper, cart, delivery_additional_fields=delivery_additional_fields))
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

            if action == 'success' and order.polis.state != 1:
                Polis.objects.filter(pk=order.polis.id).update(state=1)
                msg = 'Онлайн оплата прошла успешно. В приложении ваш полис.'
                host = request.META['HTTP_HOST'].encode('idna').decode('idna')
                mail = EmailMessage('%s полис' % host, msg, settings.EMAIL_HOST_USER, [shopper.email])
                mail.content_subtype = 'html'
                pdf_order(request, order.id, write2file=True)
                fname = 'insurance_%s.pdf' % order.id
                with open_file(fname, 'rb') as f:
                    mail.attach('polis%s.pdf' % order.id, f.read(), 'application/pdf')
                try:
                    mail.send()
                except Exception as e:
                    context['error'] = str(e)

    return render(request, template, context)


def orders_report(request):
    """Отчет по заказам (страховкам)
       :param request: HttpRequest
    """
    context = {}
    template = 'web/order/xlsx/orders_report.html'
    return render(request, template, context)
