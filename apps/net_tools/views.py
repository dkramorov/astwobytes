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

from .models import IPAddress, IPRange

CUR_APP = 'net_tools'
ip_address_vars = {
    'singular_obj': 'IP адрес',
    'plural_obj': 'IP адреса',
    'rp_singular_obj': 'IP адреса',
    'rp_plural_obj': 'IP адресов',
    'template_prefix': 'ip_address_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'net_tools',
    'submenu': 'ip_address',
    'show_urla': 'show_ip_address',
    'create_urla': 'create_ip_address',
    'edit_urla': 'edit_ip_address',
    'model': IPAddress,
    'search_result_format': ('#{}, {} {}, ({})', 'id name ip mac'),
    #'custom_model_permissions': IPAddress,
}

def api(request, action: str = 'ip_address'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    if action == 'ip_range':
        return ApiHelper(request, ip_range_vars, CUR_APP)
    return ApiHelper(request, ip_address_vars, CUR_APP)

@login_required
def show_ip_address(request, *args, **kwargs):
    """Вывод объектов
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = ip_address_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_ip_address(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объекта
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = ip_address_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def ip_address_positions(request, *args, **kwargs):
    """Изменение позиций объектов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = ip_address_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_ip_address(request, *args, **kwargs):
    """Поиск объектов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = ip_address_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

ip_range_vars = {
    'singular_obj': 'Диапазон ip',
    'plural_obj': 'Диапазоны ip',
    'rp_singular_obj': 'диапазона ip',
    'rp_plural_obj': 'диапазонов ip',
    'template_prefix': 'ip_range_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'net_tools',
    'submenu': 'ip_range',
    'show_urla': 'show_ip_range',
    'create_urla': 'create_ip_range',
    'edit_urla': 'edit_ip_range',
    'model': IPRange,
    'search_result_format': ('{} (id={})', 'name id'),
    #'custom_model_permissions': IpRange,
}

@login_required
def show_ip_range(request, *args, **kwargs):
    """Вывод объектов
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = ip_range_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

    mh_vars = ip_range_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context

@login_required
def edit_ip_range(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объекта
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = ip_range_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def ip_range_positions(request, *args, **kwargs):
    """Изменение позиций объектов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = ip_range_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_ip_range(request, *args, **kwargs):
    """Поиск объектов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = ip_range_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

    result = {'results': []}
    mh = ModelHelper(IpRange, request)
    mh_vars = ip_range_vars.copy()
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

