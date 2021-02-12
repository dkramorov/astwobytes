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

from .models import Dealer

CUR_APP = 'dealers'
dealers_vars = {
    'singular_obj': 'Дилер',
    'plural_obj': 'Дилеры',
    'rp_singular_obj': 'дилера',
    'rp_plural_obj': 'дилеров',
    'template_prefix': 'dealers_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'dealers',
    'submenu': 'dealers',
    'show_urla': 'show_dealers',
    'create_urla': 'create_dealer',
    'edit_urla': 'edit_dealer',
    'model': Dealer,
    #'custom_model_permissions': Dealer,
    'select_related_list': ('address', ),
}

def api(request, action: str = 'dealers'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'dealers':
    #    result = ApiHelper(request, dealers_vars, CUR_APP)
    result = ApiHelper(request, dealers_vars, CUR_APP)
    return result

@login_required
def show_dealers(request, *args, **kwargs):
    """Вывод дилеров
       :param request: HttpRequest
    """
    mh_vars = dealers_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('address')
    context = mh.context
    context['city_choices'] = Dealer.city_choices
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
            if row.address:
                item['address'] = row.address.address_str()
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
def edit_dealer(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование дилеров
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = dealers_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('address')
    row = mh.get_row(row_id)
    context = mh.context
    context['city_choices'] = Dealer.city_choices
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
            if row.address:
                context['address'] = row.address
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
def dealers_positions(request, *args, **kwargs):
    """Изменение позиций дилеров
       :param request: HttpRequest
    """
    result = {}
    mh_vars = dealers_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_dealers(request, *args, **kwargs):
    """Поиск дилеров
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = dealers_vars,
                       cur_app = CUR_APP,
                       sfields = None, )
