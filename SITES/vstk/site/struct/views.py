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

from .models import (
    StructObject,
    SourceData,
)

CUR_APP = 'struct'
struct_vars = {
    'singular_obj': 'Объект',
    'plural_obj': 'Объекты',
    'rp_singular_obj': 'объекта',
    'rp_plural_obj': 'объектов',
    'template_prefix': 'struct_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'struct',
    'submenu': 'struct',
    'show_urla': 'show_struct',
    'create_urla': 'create_struct',
    'edit_urla': 'edit_struct',
    'model': StructObject,
    #'custom_model_permissions': StructObject,
}

def api(request, action: str = 'struct'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'struct':
    #    result = ApiHelper(request, struct_vars, CUR_APP)
    result = ApiHelper(request, struct_vars, CUR_APP)
    return result

@login_required
def show_struct(request, *args, **kwargs):
    """Вывод объектов
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = struct_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

    mh_vars = struct_vars.copy()
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
def edit_struct(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объекта
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = struct_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

    mh_vars = struct_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    row = mh.get_row(row_id)
    context = mh.context # Контекст дозаполняется в get_row

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
def struct_positions(request, *args, **kwargs):
    """Изменение позиций объектов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = struct_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_struct(request, *args, **kwargs):
    """Поиск объектов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = struct_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

    result = {'results': []}
    mh = ModelHelper(StructObject, request)
    mh_vars = struct_vars.copy()
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


source_data_vars = {
    'singular_obj': 'Исходные данные',
    'plural_obj': 'Исходные данные',
    'rp_singular_obj': 'исходных данных',
    'rp_plural_obj': 'исходных данных',
    'template_prefix': 'source_data/',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'struct',
    'submenu': 'source_data',
    'show_urla': 'show_source_data',
    'create_urla': 'create_source_data',
    'edit_urla': 'edit_source_data',
    'model': SourceData,
    #'custom_model_permissions': StructObject,
}

@login_required
def show_source_data(request, *args, **kwargs):
    """Вывод исходных данных
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = source_data_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_source_data(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование исходных данных
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = source_data_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def source_data_positions(request, *args, **kwargs):
    """Изменение позиций исходных данных
       :param request: HttpRequest
    """
    result = {}
    mh_vars = source_data_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_source_data(request, *args, **kwargs):
    """Поиск исходных данных
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = source_data_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

