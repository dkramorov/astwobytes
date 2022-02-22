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
from apps.site.passport.models import Passport

CUR_APP = 'passport'
passport_vars = {
    'singular_obj': 'Паспортные данные',
    'plural_obj': 'Паспортные данные',
    'rp_singular_obj': 'паспортных данных',
    'rp_plural_obj': 'паспортных данных',
    'template_prefix': 'passport_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'passport',
    'submenu': 'passport',
    'show_urla': 'show_passports',
    'create_urla': 'create_passport',
    'edit_urla': 'edit_passport',
    'model': Passport,
    #'custom_model_permissions': Phones,
    'select_related_list': ('shopper', ),
}

def api(request, action: str = 'passport'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'phones':
    #    result = ApiHelper(request, passport_vars, CUR_APP)
    result = ApiHelper(request, passport_vars, CUR_APP)
    return result

@login_required
def show_passports(request, *args, **kwargs):
    """Вывод паспортных данных
       :param request: HttpRequest
    """
    mh_vars = passport_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('shopper')
    context = mh.context
    special_model_vars(mh, mh_vars, context)
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'shopper__name',
            'shopper__phone',
            'birthday',
            'series',
            'number',
            'issued',
            'issued_date',
            'registration',
        )
        fk_keys = {
            'shopper': ('name',
                        'phone'),
        }
        rows = mh.standard_show(only_fields=only_fields)
        result = []
        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys)
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
def edit_passport(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование паспортных данных
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = passport_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def passports_positions(request, *args, **kwargs):
    """Изменение позиций паспортных данных
       :param request: HttpRequest
    """
    result = {}
    mh_vars = passport_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_passports(request, *args, **kwargs):
    """Поиск паспортных данных
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = passport_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

