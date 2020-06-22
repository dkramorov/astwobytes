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
    mh_vars = shoppers_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
            item['actions'] = row.id
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
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
def edit_shopper(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование пользователя
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = shoppers_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
    context['oauth_types'] = Shopper.oauth_choices
    row = mh.get_row(row_id)
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
        elif action == 'img' and request.FILES:
            mh.uploads()
    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.url_edit
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

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