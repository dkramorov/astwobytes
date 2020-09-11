# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import ModelHelper, create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from .oauth import VK, Yandex
from .models import Shopper
from .utils import save_user_to_request

CUR_APP = 'personal'
shoppers_vars = {
    'singular_obj': 'Посетитель',
    'plural_obj': 'Посетители',
    'rp_singular_obj': 'посетителя',
    'rp_plural_obj': 'посетителей',
    'template_prefix': 'shoppers_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'personal',
    'submenu': 'shoppers',
    'show_urla': 'show_shoppers',
    'create_urla': 'create_shopper',
    'edit_urla': 'edit_shopper',
    'model': Shopper,
}

def api(request, action: str = 'shoppers'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'personal':
    #    result = ApiHelper(request, personal_vars, CUR_APP)
    result = ApiHelper(request, personal_vars, CUR_APP)
    return result

@login_required
def show_shoppers(request, *args, **kwargs):
    """Вывод пользователей
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = shoppers_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_shopper(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование пользователя
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    extra_vars = {'oauth_types': Shopper.oauth_choices}
    return edit_view(request,
                     model_vars = shoppers_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def shoppers_positions(request, *args, **kwargs):
    """Изменение позиций пользователей
       :param request: HttpRequest
    """
    result = {}
    mh_vars = shoppers_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_shoppers(request, *args, **kwargs):
    """Поиск пользователей
       :param request: HttpRequest
    """
    result = {'results': []}
    mh = ModelHelper(Shopper, request)
    mh_vars = shoppers_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('id', 'name', 'first_name', 'last_name', 'middle_name', 'phone', 'login')
    rows = mh.standard_show()
    for row in rows:
        result['results'].append({'text': '%s #%s' % (row, row.id), 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

oauth_vars = {
    'singular_obj': 'Проверка OAuth',
    'plural_obj': 'Проверка OAuth',
    'rp_singular_obj': 'Проверка OAuth',
    'rp_plural_obj': 'Проверка OAuth',
    'template_prefix': 'personal_',
    'action_create': 'Авторизация',
    'action_edit': '',
    'action_drop': '',
    'menu': 'personal',
    'submenu': 'oauth',
    'show_urla': 'oauth_test',
    'model': Shopper,
}
@login_required
def oauth_test(request, *args, **kwargs):
    """Тестирование oauth авторизации
       :param request: HttpRequest
    """
    mh_vars = oauth_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context

    context.update({
        'VK_OAUTH_LINK': VK().get_auth_user_link(),
        'YANDEX_OAUTH_LINK': Yandex().get_auth_user_link(),
    })
    template = '%soauth_test.html' % mh.template_prefix
    return render(request, template, context)

def oauth_vk(request, *args, **kwargs):
    """После авторизации пользователя на vk,
       он будет перенаправлен на эту страничку с кодом
       ?code=7a6fa4df...
       :param request: HttpRequest
    """
    result = {}
    if request.method == 'GET':
        code = request.GET.get('code')
        result['code'] = code
        error = request.GET.get('error')
        result['error'] = error
        if error:
            result['error_description'] = request.GET.get('error_description')
        else:
            vk = VK()
            access_token = vk.get_access_token(code)
            result['get_access_token'] = access_token
            user_info = vk.api_request(method = 'users.get', **{
                'user_ids': vk.user_id,
                'fields': vk.user_fields(),
            })
            email = access_token.get('email')
            user_info['email'] = email
            result['user_info'] = user_info
            if 'id' in user_info:
                user = save_vk_user(user_info)
                save_user_to_request(request, user)
                return redirect('/registration/')
    return JsonResponse(result, safe=False)

def save_vk_user(user_info: dict):
    """Сохранение пользователя VK
       :param user_info: словарь с данными ответа от апи
       :return: Shopper
    """
    login = 'vk_%s' % user_info['id']
    user = Shopper.objects.filter(login=login).first()
    if not user:
        user = Shopper(login=login)
    if not user.state:
        user.state = 1
    user.first_name = user_info.get('first_name')
    user.last_name = user_info.get('last_name')
    user.passwd = ''
    phone = user_info.get('mobile_phone')
    if phone:
        user.phone = phone
    else:
        phone = user_info.get('home_phone')
        if phone:
            user.phone = phone
    email = user_info.get('email')
    if email:
        user.email = email
    user.oauth = 2
    user.save()
    if not user.img and user_info.get('photo_max'):
        user.upload_img(user_info['photo_max'])
    return user

def oauth_yandex(request, *args, **kwargs):
    """После авторизации пользователя на yandex,
       он будет перенаправлен на эту страничку с кодом
       ?code=7a6fa4df...
       :param request: HttpRequest
    """
    result = {}
    if request.method == 'GET':
        code = request.GET.get('code')
        result['code'] = code
        error = request.GET.get('error')
        result['error'] = error
        if error:
            result['error_description'] = request.GET.get('error_description')
        else:
            yandex = Yandex()
            access_token = yandex.get_access_token(code)
            result['get_access_token'] = access_token
            user_info = yandex.passport_request()
            result['user_info'] = user_info
            if 'id' in user_info:
                user = save_yandex_user(user_info)
                save_user_to_request(request, user)
                return redirect('/registration/')
    return JsonResponse(result, safe=False)

def save_yandex_user(user_info: dict):
    """Сохранение пользователя Yandex
       :param user_info: словарь с данными ответа от апи
       :return: Shopper
    """
    login = 'ya_%s' % user_info['id']
    user = Shopper.objects.filter(login=login).first()
    if not user:
        user = Shopper(login=login)
    if not user.state:
        user.state = 1
    user.first_name = user_info.get('first_name')
    user.last_name = user_info.get('last_name')
    user.passwd = ''
    email = user_info.get('default_email')
    if email:
        user.email = email
    user.oauth = 3
    if user_info.get('is_avatar_empty') is False:
        avatar_url = 'https://avatars.yandex.net/get-yapic/'
        avatar_path = '%s/islands-200' % user_info.get('default_avatar_id')
        avatar = '%s%s' % (avatar_url, avatar_path)
        user.img = avatar
    user.save()
    return user
