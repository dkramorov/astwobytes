# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper

from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from .models import Address

CUR_APP = 'addresses'
addresses_vars = {
    'singular_obj': 'Адрес',
    'plural_obj': 'Адреса',
    'rp_singular_obj': 'адреса',
    'rp_plural_obj': 'адресов',
    'template_prefix': 'addresses_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'addresses',
    'submenu': 'addresses',
    'show_urla': 'show_addresses',
    'create_urla': 'create_address',
    'edit_urla': 'edit_address',
    'model': Address,
    #'custom_model_permissions': Address,
}

def api(request, action: str = 'addresses'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'addresses':
    #    result = ApiHelper(request, addresses_vars, CUR_APP)
    result = ApiHelper(request, addresses_vars, CUR_APP)
    return result

@login_required
def show_addresses(request, *args, **kwargs):
    """Вывод объектов
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = addresses_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_address(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объекта
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    extra_vars = {
        'yandex_maps_api_key': settings.YANDEX_MAPS_API_KEY,
    }
    return edit_view(request,
                     model_vars = addresses_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def addresses_positions(request, *args, **kwargs):
    """Изменение позиций объектов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = addresses_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_addresses(request, *args, **kwargs):
    """Поиск объектов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = addresses_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

    result = {'results': []}
    mh = ModelHelper(Address, request)
    mh_vars = addresses_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('id', 'name')
    rows = mh.standard_show()
    for row in rows:
        result['results'].append({'text': '%s (%s)' % (row.name, row.id), 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

