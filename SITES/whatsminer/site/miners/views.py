# -*- coding:utf-8 -*-
import os
import json
import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import management
from django.core.cache import cache

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.string_parser import get_request_ip

from apps.main_functions.views_helper import (
    show_view,
    edit_view,
    search_view,
)
from apps.net_tools.views import show_ip_range, edit_ip_range
from apps.site.miners.models import (
    Comp,
)

logger = logging.getLogger('main')

CUR_APP = 'miners'
comps_vars = {
    'singular_obj': 'Компьютер',
    'plural_obj': 'Компьютеры',
    'rp_singular_obj': 'компьютера',
    'rp_plural_obj': 'компьютеров',
    'template_prefix': 'comp_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'miners',
    'submenu': 'comps',
    'show_urla': 'show_comps',
    'create_urla': 'create_comp',
    'edit_urla': 'edit_comp',
    'model': Comp,
    #'custom_model_permissions': Robots,
    #'select_related_list': ('name', ),
    'search_result_format': ('{} - {}', 'name ip'),
}

def api(request, action: str = 'comps'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    if action == 'comps':
        result = ApiHelper(request, comps_vars, CUR_APP)
    else:
        result = ApiHelper(request, comps_vars, CUR_APP)
    return result

@login_required
def show_comps(request, *args, **kwargs):
    """Вывод компьютеров
       :param request: HttpRequest
    """
    mh_vars = comps_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('ip')
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
            if row.ip:
                item['ip__ip'] = row.ip.ip
                item['ip__mac'] = row.ip.mac
            result.append(item)
        if request.GET.get('page'):
            result = {'data': result,
                      'last_page': mh.raw_paginator['total_pages'],
                      'total_records': mh.raw_paginator['total_records'],
                      'cur_page': mh.raw_paginator['cur_page'],
                      'by': mh.raw_paginator['by'], }
        return JsonResponse(result, safe=False)
    template = '%stable.html' % (mh.template_prefix, )
    if kwargs.get('template_prefix'):
        template = '%s%s' % (kwargs['template_prefix'], template)
    return render(request, template, context)

@login_required
def edit_comp(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование компьютеров
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = comps_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('ip')
    row = mh.get_row(row_id)
    context = mh.context
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
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def comps_positions(request, *args, **kwargs):
    """Изменение позиций компьютеров
       :param request: HttpRequest
    """
    result = {}
    mh_vars = comps_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_comps(request, *args, **kwargs):
    """Поиск компьютеров
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = comps_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

@login_required
def scan_ips(request, *args, **kwargs):
    """Сканирование диапазона ip адресов
       :param request: HttpRequest
    """
    scan_vars = {
        'singular_obj': 'Сканирование диапазона ip адресов',
        'plural_obj': 'Сканирование диапазона ip адресов',
        'rp_singular_obj': 'Сканирование диапазона ip адресов',
        'rp_plural_obj': 'Сканирование диапазона ip адресов',
        'template_prefix': 'comp_',
        'action_create': 'Создание',
        'action_edit': 'Редактирование',
        'action_drop': 'Удаление',
        'menu': 'miners',
        'submenu': 'scan_ips',
        'show_urla': 'scan_ips',
        'model': Comp,
    }
    mh_vars = scan_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'scan_ips')
    context = mh.context
    template = '%sscan_ips.html' % (mh.template_prefix, )
    if request.method == 'POST' and request.is_ajax():
        error = ''
        is_range_error = ''
        start_ip = request.POST.get('start_ip')
        end_ip = request.POST.get('end_ip')
        result = {
            'start_ip': start_ip,
            'end_ip': end_ip,
        }
        start_ip_parts = start_ip.split('.')
        end_ip_parts = end_ip.split('.')
        if not len(start_ip_parts) == 4 or not len(end_ip_parts) == 4:
            error += 'Диапазоны не соответствуют нужной длине<br>'
        else:
            if start_ip_parts[0] > end_ip_parts[0]:
                is_range_error = True
            elif start_ip_parts[0] == end_ip_parts[0]:
                if start_ip_parts[1] > end_ip_parts[1]:
                    is_range_error = True
                elif start_ip_parts[1] == end_ip_parts[1]:
                    if start_ip_parts[2] > end_ip_parts[2]:
                        is_range_error = True
                    elif start_ip_parts[2] == end_ip_parts[2]:
                        if start_ip_parts[3] > end_ip_parts[3]:
                            is_range_error = True
                        elif start_ip_parts[3] == end_ip_parts[3]:
                            if start_ip_parts[4] > end_ip_parts[4]:
                                is_range_error = True
        if is_range_error:
            error += 'Начальный ip адрес больше конечного<br>'
        if not error:
            management.call_command('scan_ips', ip_range='%s-%s' % (start_ip, end_ip), ip_ports='4028')
            cache_key = 'scanner_ports_result'
            new_ips = cache.get(cache_key)
            result['new_ips'] = new_ips
            result['success'] = 'Сканирование диапазона адресов'
            return JsonResponse(result, safe=False)
        else:
            result['error'] = error
            return JsonResponse(result, safe=False)
    return render(request, template, context)

@login_required
def miners_show_comps(request, *args, **kwargs):
    """Вывод компьютеров
       :param request: HttpRequest
    """
    kwargs['template_prefix'] = 'miners_'
    return show_comps(request, *args, **kwargs)

@login_required
def miners_edit_comp(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование компьютеров
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    kwargs['template_prefix'] = 'miners_'
    return edit_comp(request, action, row_id, *args, **kwargs)


@login_required
def miners_show_ip_range(request, *args, **kwargs):
    """Вывод объектов
       :param request: HttpRequest
    """
    kwargs['template_prefix'] = 'miners_'
    return show_ip_range(request, *args, **kwargs)

@login_required
def miners_edit_ip_range(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объекта
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    kwargs['template_prefix'] = 'miners_'
    return edit_ip_range(request, action, row_id, *args, **kwargs)

