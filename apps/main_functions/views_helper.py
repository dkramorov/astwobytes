# -*- coding:utf-8 -*-
import json
import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, ModelHelper

logger = logging.getLogger('main')

def special_model_vars(mh, mh_vars, context):
    """Вспомогательная функция на show_view, edit_view
       Обработка специфических ключей в model_vars
       :param mh: ModelHelper
       :param mh_vars: словарь со всеми ключами для работы
       :param context: словарь контекста из mh
    """
    # ----------------------
    # Права от другой модели
    # ----------------------
    if 'custom_model_permissions' in mh_vars:
        mh.get_permissions(mh_vars['custom_model_permissions'])
        del context['custom_model_permissions']
    # -------------------
    # select_related_list
    # -------------------
    if 'select_related_list' in mh_vars:
        for sr in mh_vars['select_related_list']:
            mh.select_related_add(sr)
        if 'select_related_list' in context:
            del context['select_related_list']
    # ------------------
    # insert_breadcrumbs
    # ------------------
    if 'insert_breadcrumbs' in context:
        for i, crumb in enumerate(context['insert_breadcrumbs']):
            mh.breadcrumbs.insert(i, crumb)
        del context['insert_breadcrumbs']

def show_view(request,
              model_vars: dict,
              cur_app: str,
              extra_vars: dict = None):
    """Вывод в таблицу записей модели
       :param request: HttpRequest
       :param model_vars: словарь с данными для модели,
           например,
               costs_vars = {
                   'singular_obj': 'Тип цены',
                   'plural_obj': 'Типы цен',
                   'rp_singular_obj': 'типа цены',
                   'rp_plural_obj': 'типов цен',
                   'template_prefix': 'costs_',
                   'action_create': 'Создание',
                   'action_edit': 'Редактирование',
                   'action_drop': 'Удаление',
                   'menu': 'products',
                   'submenu': 'costs',
                   'show_urla': 'show_costs',
                   'create_urla': 'create_cost',
                   'edit_urla': 'edit_cost',
                   'model': CostsTypes,
                   'custom_model_permissions': Products,
                   'select_related_list': ('user', ),
               }
       :param cur_app: CUR_APP во view.py,
           например,
               CUR_APP='products'
    """
    if not extra_vars:
        extra_vars = {}
    mh_vars = model_vars.copy()
    mh = create_model_helper(mh_vars, request, cur_app)
    context = mh.context
    if extra_vars:
        context.update(extra_vars)
    special_model_vars(mh, mh_vars, context)
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

def edit_view(request,
              model_vars: dict,
              cur_app: str,
              action: str,
              row_id: int = None,
              extra_vars: dict = None):
    """Создание/редактирование записи для для модели
       :param request: HttpRequest
       :param model_vars: словарь с данными для модели
       :param cur_app: CUR_APP во view.py
    """
    if not extra_vars:
        extra_vars = {}
    mh_vars = model_vars.copy()
    mh = create_model_helper(mh_vars, request, cur_app, action)
    context = mh.context
    if extra_vars:
        context.update(extra_vars)
    special_model_vars(mh, mh_vars, context)
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
        pass_fields = []
        mh.post_vars(pass_fields=pass_fields)
        if action == 'create' or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    if mh.error:
                        context['error'] = mh.error
                    else:
                        context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    if mh.error:
                        context['error'] = mh.error
                    else:
                        context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'

        elif not mh.error and action == 'img' and request.FILES:
            mh.uploads()
    if not mh.error and mh.row:
        mh.url_edit = reverse('%s:%s' % (cur_app, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.url_edit
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

def positions_view(request,
                   model_vars: dict,
                   cur_app: str):
    """Изменение позиций записей модели
       :param request: HttpRequest
       :param model_vars: словарь с данными для модели
       :param cur_app: CUR_APP во view.py
    """
    result = {}
    mh_vars = model_vars.copy()
    mh = create_model_helper(mh_vars, request, cur_app, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def get_deep_attr(row, field):
    """Получение поля модели,
       нужно если значение поля находится
       во вложенной модели foreign_key
       :param row: экземелпяр модели
       :param field: поле модели
    """
    if '__' in field:
        subrow = row
        subfields = field.split('__')
        for subfield in subfields:
            if hasattr(subrow, subfield):
                subrow = getattr(subrow, subfield)
        if subrow:
            return subrow
    return getattr(row, field)

def search_view(request,
                model_vars: dict,
                cur_app: str,
                sfields: list = None):
    """Поиск записей модели
       :param request: HttpRequest
       :param model_vars: словарь с данными для модели
       :param cur_app: CUR_APP во view.py
       :param sfields: список полей для поиска

       search_result_format, например, ('{} (id={})', 'name id')
       указывается в model_vars
       шаблон для вывода результатов, например,
       результат будет такой '{} ({})'.format(row.name, row.id)
    """
    result = {'results': []}
    model = model_vars['model']
    mh = ModelHelper(model, request)
    mh_vars = model_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)

    # Общие поля для поиска
    if not sfields:
        sfields = ('name', 'tag', 'code')
    exists_fields = ['id']
    for sfield in sfields:
        if hasattr(model, sfield):
            exists_fields.append(sfield)
    mh.search_fields = (sfield)

    voca = None
    search_result_format = mh_vars.get('search_result_format')
    if search_result_format:
        voca = [field for field in search_result_format[1].split()]
        mh.search_fields = voca

    special_model_vars(mh, mh_vars, {})

    rows = mh.standard_show()

    for row in rows:
        if voca:
            name = search_result_format[0].format(*[get_deep_attr(row, field) for field in voca])
            result['results'].append({'text': name, 'id': row.id})
        else:
            name = []
            for field in exists_fields:
                value = getattr(row, field)
                if value:
                    name.append(str(value))
            result['results'].append({'text': ', '.join(name), 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

