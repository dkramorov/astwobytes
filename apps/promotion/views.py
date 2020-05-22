# -*- coding:utf-8 -*-
import json
import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from apps.main_functions.functions import object_fields
from apps.main_functions.date_time import str_to_date
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.tabulator import tabulator_filters_and_sorters

from apps.flatcontent.seo import check_titles_and_metatags
from .models import Vocabulary, SVisits, SeoReport

logger = logging.getLogger('main')

CUR_APP = 'promotion'
vocabulary_vars = {
    'singular_obj': 'Запрос',
    'plural_obj': 'Запросы',
    'rp_singular_obj': 'запроса',
    'rp_plural_obj': 'запросов',
    'template_prefix': 'promotion_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'promotion',
    'submenu': 'vocabulary',
    'show_urla': 'show_vocabulary',
    'create_urla': 'create_vocabulary',
    'edit_urla': 'edit_vocabulary',
    'model': Vocabulary,
}

def api(request, action: str = 'vocabulary'):
    """Апи-метод для получения всех данных"""
    #if action == 'promotion':
    #    result = ApiHelper(request, vocabulary_vars, CUR_APP)
    result = ApiHelper(request, vocabulary_vars, CUR_APP)
    return result

def import_xlsx(request, action: str = 'vocabulary'):
    """Апи-метод для сохранения данных из excel-файла
                     удаления данных по excel-файлу
       :param request: HttpRequest
       :param action: какую модель использовать
    """
    #if action == 'promotion':
    #    result = XlsxHelper(request, vocabulary_vars, CUR_APP)
    result = XlsxHelper(request, vocabulary_vars, CUR_APP,
                        cond_fields = ['name'])
    return result

@login_required
def show_vocabulary(request, *args, **kwargs):
    """Вывод словаря"""
    mh_vars = vocabulary_vars.copy()
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
    context['import_xlsx_url'] = reverse('%s:%s' % (CUR_APP, 'import_xlsx'),
                              kwargs={'action': 'vocabulary'})
    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def edit_vocabulary(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование словаря"""
    mh_vars = vocabulary_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
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
def vocabulary_positions(request, *args, **kwargs):
    """Изменение позиций в словаре"""
    result = {}
    mh_vars = vocabulary_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_vocabulary(request, *args, **kwargs):
    """Поиск в словаре"""
    result = {'results': []}
    mh = ModelHelper(Vocabulary, request)
    mh_vars = vocabulary_vars.copy()
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

svisits_vars = {
    'singular_obj': 'Посещение сайта',
    'plural_obj': 'Посещения сайтов',
    'rp_singular_obj': 'посещения сайта',
    'rp_plural_obj': 'посещений сайтов',
    'template_prefix': 'svisits_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'promotion',
    'submenu': 'svisits',
    'show_urla': 'show_svisits',
    'create_urla': 'create_svisit',
    'edit_urla': 'edit_svisit',
    'model': SVisits,
}

@login_required
def show_svisits(request, *args, **kwargs):
    """Вывод визитов"""
    mh_vars = svisits_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, disable_fas=True)
    context = mh.context
    # -----------------------
    # Фильтрация и сортировка
    # -----------------------
    filters_and_sorters = tabulator_filters_and_sorters(request)
    if not filters_and_sorters['sorters']:
        filters_and_sorters['params']['sorters']['date'] = 'desc'

    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    for rsorter in filters_and_sorters['sorters']:
        mh.order_by_add(rsorter)
    context['fas'] = filters_and_sorters['params']

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
def edit_svisit(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование визита"""
    mh_vars = svisits_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
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
        context['redirect'] = mh.url_edit
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def svisits_positions(request, *args, **kwargs):
    """Изменение позиций визитов"""
    result = {}
    mh_vars = svisits_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

@csrf_exempt
def svisits_import(request, *args, **kwargs):
    """Импорт визитов"""
    result = {}
    # TODO Сделать через сервис-аккаунт
    obj = json.loads(request.body)
    date = str_to_date(obj.get('date'))
    ip = obj.get('ip')
    rows = obj.get('rows')
    if not date or not rows:
        return JsonResponse(result, safe=False)

    # Неоптимально, но точно
    for row in rows:
        for name, ids in row.items():
            for pk in ids:
                analog = SVisits.objects.filter(
                    company_id=pk,
                    profile=name,
                    date=date,
                    ip=ip,
                ).first()
                if not analog:
                    analog = SVisits()
                analog.company_id = pk
                analog.profile = name
                analog.date = date
                analog.ip = ip
                analog.count = ids.count(pk)
                analog.save()
    return JsonResponse(result, safe=False)


seo_report_vars = {
    'singular_obj': 'Проблема сео',
    'plural_obj': 'Проблемы сео',
    'rp_singular_obj': 'проблему сео',
    'rp_plural_obj': 'проблем сео',
    'template_prefix': 'seo_report_',
    'action_create': 'Анализ',
    'action_edit': 'Решение',
    'action_drop': 'Удаление',
    'menu': 'promotion',
    'submenu': 'seo_report',
    'show_urla': 'show_seo_report',
    'model': SeoReport,
}

@login_required
def show_seo_report(request, *args, **kwargs):
    """Вывод проблем сео"""
    result = []

    if request.method == 'POST':
        result = check_titles_and_metatags()
        return JsonResponse(result, safe=False)

    mh_vars = seo_report_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, disable_fas=True)
    context = mh.context
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        for row in rows:
            item = object_fields(row)
            item['actions'] = row.id
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
