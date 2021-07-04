# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, tabulator_filters_and_sorters
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.views_helper import (
    show_view,
    edit_view,
    search_view,
    special_model_vars,
)
from apps.site.phones.models import Phones

CUR_APP = 'phones'
phones_vars = {
    'singular_obj': 'Телефон 8800',
    'plural_obj': 'Телефоны 8800',
    'rp_singular_obj': 'телефона 8800',
    'rp_plural_obj': 'телефонов 8800',
    'template_prefix': 'phones_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'phones',
    'submenu': 'phones',
    'show_urla': 'show_phones',
    'create_urla': 'create_phone',
    'edit_urla': 'edit_phone',
    'model': Phones,
    #'custom_model_permissions': Phones,
    'select_related_list': ('menu', ),
}

def api(request, action: str = 'phones'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'phones':
    #    result = ApiHelper(request, phones_vars, CUR_APP)
    result = ApiHelper(request, phones_vars, CUR_APP)
    return result

def get_phones_menus(ids_phones: dict):
    """Получение менюшек по списку телефонов
       :param ids_phones: словарь идентификаторов телефонов
    """
    menus = Phones.objects.select_related('menu').filter(pk__in=ids_phones).values('id', 'menu__id', 'menu__link', 'menu__name')
    for menu in menus:
        if not ids_phones[menu['id']]:
            ids_phones[menu['id']] = []
        ids_phones[menu['id']].append({
            'id': menu['menu__id'],
            'link': menu['menu__link'],
            'name': menu['menu__name'],
        })

@login_required
def show_phones(request, *args, **kwargs):
    """Вывод телефонов 8800
       :param request: HttpRequest
    """
    mh_vars = phones_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, disable_fas=True)

    filters_and_sorters = tabulator_filters_and_sorters(request)
    for rsorter in filters_and_sorters['sorters']:
        if not rsorter in ('cat', '-cat'):
            mh.order_by_add(rsorter)
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)

    mh.context['fas'] = filters_and_sorters['params']
    # Чтобы получить возможность модифицировать фильтры и сортировщики
    mh.filters_and_sorters = filters_and_sorters

    context = mh.context

    # Условие под выборку определенной категории
    menu_filter = filters_and_sorters['params'].get('filters', {})
    if 'cat' in menu_filter:
        ids_phones = Phones.objects.filter(menu=menu_filter['cat']).values_list('id', flat=True)
        ids_phones = list(ids_phones)
        mh.filter_add(Q(pk__in = ids_phones))

    special_model_vars(mh, mh_vars, context)
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'name',
            'phone',
            'img',
            'is_active',
            'position',
        )
        rows = mh.standard_show()

        ids_phones = {row.id: None for row in rows}
        get_phones_menus(ids_phones)

        result = []
        for row in rows:
            item = object_fields(row, only_fields=only_fields)
            item['actions'] = row.id
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            if ids_phones[row.id]:
                item['cat'] = ids_phones[row.id]
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
def edit_phone(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование телефона
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = phones_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def phones_positions(request, *args, **kwargs):
    """Изменение позиций контрагентов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = phones_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_phones(request, *args, **kwargs):
    """Поиск телефонов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = phones_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

