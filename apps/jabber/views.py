# -*- coding:utf-8 -*-
import os
import json
import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.string_parser import kill_quotes, GenPasswd

from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from apps.jabber.models import Registrations

CUR_APP = 'jabber'
registrations_vars = {
    'singular_obj': 'Регистрация',
    'plural_obj': 'Регистрации',
    'rp_singular_obj': 'регистрации',
    'rp_plural_obj': 'регистраций',
    'template_prefix': 'jabber_registrations_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'jabber',
    'submenu': 'registrations',
    'show_urla': 'show_registrations',
    'create_urla': 'create_registration',
    'edit_urla': 'edit_registration',
    'model': Registrations,
    #'custom_model_permissions': Registrations,
}

@login_required
def show_registrations(request, *args, **kwargs):
    """Вывод регистраций
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = registrations_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_registration(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование регистрации
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = registrations_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def registrations_positions(request, *args, **kwargs):
    """Изменение позиций регистраций
       :param request: HttpRequest
    """
    result = {}
    mh_vars = registrations_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_registrations(request, *args, **kwargs):
    """Поиск регистраций
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = registrations_vars,
                       cur_app = CUR_APP,
                       sfields = ('phone', ), )

def register_user(request):
    """Апи-метод для регистрации нового пользователя
       1) Приложение отправляет нам телефон пользователя
       2) Мы запоминаем телефон, генерируем код подтверждения, вносим в таблицу
       3) Делаем звонок, сообщаем код подтверждения, пользователь вносит код
       4) Приложени отправляет код и если код подходит, выполняем регистрацию
    """
    result = {}
    method = request.GET if request.method == 'GET' else request.POST
    action = method.get('action')
    phone = method.get('phone')
    if phone:
        phone = kill_quotes(phone, 'int')
    if action == 'registration' and phone:
        if len(phone) == 11 and phone[0] == '8' and phone[1] == '9':

            code = '0000'
            for i in range(10):
                code = GenPasswd(4, '1234567890')
                if not code.startswith('0'):
                    break

            platform = method.get('platform')
            version = method.get('version')
            passwd = method.get('passwd')

            # TODO: state=1 - ошибка, уже зарегистрирован
            analog = Registrations.objects.filter(phone=phone).exclude(is_active=False).first()
            if not analog:
                analog = Registrations()
            analog.phone = phone
            analog.code = code
            analog.platform = platform
            analog.version = version
            analog.passwd = passwd
            analog.save()
            # Код передаем на свич - поэтому, он секретная инфа как паролька
            result = object_fields(analog, pass_fields=('passwd', 'code'))

            # Скрипт отправляет на свич телефон и код,
            # свич звонит и диктует
            params = {
                'phone': phone,
                'digit': code,
            }
            uri = '%s/freeswitch/sms_service/say_code/' % settings.FREESWITCH_DOMAIN
            if not uri.startswith('https://'):
                uri = 'https://%s' % uri
            r = requests.get(uri, params=params)
    elif action == 'confirm' and phone:
        code = method.get('code')
        analog = Registrations.objects.filter(phone=phone).exclude(is_active=False).first()
        if analog:
            result = object_fields(analog, pass_fields=('passwd', 'code'))
            # Делаем запрос на реальную регистрацию пользователя
            r = requests.post('https://127.0.0.1:5443/api/register', json={'user': analog.phone, 'host': settings.JABBER_DOMAIN, 'password': analog.passwd}, verify=False)
            result['result'] = r.text
    return JsonResponse(result, safe=False)
