# -*- coding:utf-8 -*-
import json
import datetime
import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from apps.flatcontent.models import Blocks
from apps.flatcontent.views import SearchLink
from apps.flatcontent.flatcat import get_cat_for_site, get_product_for_site
from apps.main_functions.string_parser import kill_quotes, GenPasswd
from apps.main_functions.views import DefaultFeedback
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.date_time import str_to_date

from apps.personal.models import Shopper, get_personal_user as get_shopper
from apps.personal.oauth import VK, Yandex
from apps.personal.utils import save_user_to_request, remove_user_from_request
from apps.personal.auth import register_from_site, login_from_site, update_profile_from_site, phone_confirmed

from apps.site.phones.models import Phones
from apps.site.phones.flatcat import get_phones_for_site

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
        #'force_send': 1, # Принудительная отправка
        #'fv': [],
        #'dummy': 1, # Не возвращаем HttpResponse
        #'do_not_send': 1, # Не отправляем письмо
        'fields':[
            {'name': 'test_field', 'value': 'Тестовое поле'},
            {'name': 'qq', 'value': 'QQ'},
            {'name': 'contacts', 'value': 'Название компании и контакты'},
            {'name': 'description', 'value': 'Описание проекта'},
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
    context = {
      'fs_server': settings.FREESWITCH_DOMAIN,
      'tab': request.GET.get('tab'),
    }
    q_string = {}
    containers = {}
    shopper = get_shopper(request)
    if not shopper:
        return redirect(reverse('%s:%s' % (CUR_APP, 'login')))

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
    #context['orders'] = Orders.objects.filter(shopper=shopper).order_by('-created')[:50]
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
    template = 'web/login/login.html'

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=reg_vars['singular_obj'])
    context['breadcrumbs'] = [{
        'name': 'Регистрация',
        'link': reverse('%s:%s' % (CUR_APP, 'login')),
    }]
    context['page'] = page
    context['containers'] = containers
    context['vk_link'] = VK().get_auth_user_link()
    context['yandex_link'] = Yandex().get_auth_user_link()

    return render(request, template, context)

def logout(request):
    """Деавторизация пользователя"""
    remove_user_from_request(request)
    return redirect(reverse('%s:%s' % (CUR_APP, 'login')))

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

    return render(request, template, context)

@csrf_exempt
def test(request):
    """Апи-метод для получения ip-адреса"""
    method = request.GET if request.method == 'GET' else request.POST
    result = {
        'ip': method.get('REMOTE_ADDR'),
        'ip_forwarded': request.META.get('HTTP_X_FORWARDED_FOR'),
    }
    # на случай, если надо посмотреть тело json запроса
    if hasattr(request, 'body') and request.body:
        print(json_pretty_print(json.loads(request.body)))
        result = {
            'apiVersion': '1',
            'error': {
                'code':400,
                'message': 'bad request',
                'errors': [{
                    'reason': 'requiredFieldMissing',
                    'message': 'pickup: required field pointOfServiceId missing',
                }]
            },
        }
        return JsonResponse(result, safe=False, status=400)
    return JsonResponse(result, safe=False)

def confirm_phone(request):
    """Запрос на подтверждение телефона,
       проверка кода подтверждения телефона
    """
    result = {}
    shopper = get_shopper(request)
    if not shopper:
        # Упрощенная регистрация по телефону
        if request.GET.get('digits'):
            if request.session.get('confirm_phone') and request.GET['digits'] == request.session['confirm_phone']:
                new_user = Shopper.objects.create(
                    phone=request.session['phone'],
                    name='Гость',
                )
                save_user_to_request(request, new_user)
                if phone_confirmed(request): # Тел подтвержден
                    result['success'] = 1
                    fs_shopper(request)
                return JsonResponse(result, safe=False)
        result = prepare_session(request, request.GET.get('phone'))
        return JsonResponse(result, safe=False)
    if request.GET.get('digits'):
        if request.session.get('confirm_phone') and request.GET['digits'] == request.session['confirm_phone']:
            if phone_confirmed(request): # Тел подтвержден
                result['success'] = 1
                fs_shopper(request)
        return JsonResponse(result, safe=False)
    result = prepare_session(request)
    return JsonResponse(result, safe=False)

def prepare_session(request, phone: str = None):
    """Подготовить сессию для регистрации/обновления
       профиля с подтверждением по обратному звонку
       :param request: HttpRequest
       :param phone: Телефон (если нет пользователя)
    """
    result = {}
    shopper = get_shopper(request)
    if request.method == 'GET' and (shopper or phone):
        if shopper:
            phone = shopper.phone
        phone = kill_quotes(phone, 'int')
        request.session['confirm_phone'] = GenPasswd(4, '1234567890')
        request.session['phone'] = phone
        request.session.save()
        # Скрипт отправляет на свич телефон
        # и код и свич звонит и диктует
        params = {
            'phone': phone,
            'digit': request.session['confirm_phone'],
        }
        r = requests.get('%s/freeswitch/sms_service/say_code/' % settings.FREESWITCH_DOMAIN, params=params)

        result = r.json()
    return result

def calls_history(request):
    """Загрузить историю звонков по пользователю"""
    result = {}
    shopper = get_shopper(request)
    if request.method == 'GET' and shopper:
        date = str_to_date(request.GET.get('date'))
        if not date:
            date = datetime.date.today()
        start_date = '%s-%s-%s 00:00:00' % (date.year, date.month, date.day)
        end_date = '%s-%s-%s 23:59:59' % (date.year, date.month, date.day)
        params = {
            'page': request.GET.get('page', 0),
            'filter__created__lte': end_date,
            'filter__created__gte': start_date,
            'order__created': 'desc',
            'only_fields': 'dest,created,duration,billing,state,client_name',
        }
        headers = {
            'token': '%s-%s' % (settings.FS_USER, shopper.id),
        }
        r = requests.get('%s/freeswitch/cdr_csv/api/' % settings.FREESWITCH_DOMAIN, params=params, headers=headers)
        result = r.json()

    return JsonResponse(result, safe=False)

def fs_shopper(request):
    """После регистрации и/или подтверждения номера,
       надо на свиче синхануть пользователя
       Пользователи сайта /freeswitch/admin/personal_users/
       :param request: HttpRequest
    """
    shopper = get_shopper(request)
    token = '0_o'
    endpoint = '/freeswitch/personal_users/sync/'
    params = {
        'userkey': '%s-%s' % (settings.FS_USER, shopper.id),
        'username': shopper.login,
        'phone': shopper.phone,
        'phone_confirmed': 1 if shopper.phone_confirmed else 0,
    }
    headers = {
        'token': token,
    }
    r = requests.post('%s%s' % (settings.FREESWITCH_DOMAIN, endpoint), data=params, headers=headers)

phones_vars = {
    'singular_obj': 'Телефоны 8800',
    'template_prefix': 'phones_',
    'show_urla': 'phones',
}

def phones_cat(request, link: str = None):
    """Странички каталога телефонов
       :param link: ссылка на рубрику (без /phones/ префикса)
    """
    mh_vars = cat_vars.copy()
    kwargs = {
        'q_string': {
            'by': 10,
        },
    }
    context = get_phones_for_site(request, link, **kwargs)
    containers = {}

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/phones/%slist.html' % (mh_vars['template_prefix'], )

    page = SearchLink(context['q_string'], request, containers)
    if page:
        context['page'] = page
    context['containers'] = containers

    return render(request, template, context)
