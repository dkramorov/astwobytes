# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from apps.weld.company_model import Company
from apps.weld.views import CUR_APP

companies_vars = {
    'singular_obj': 'Объект',
    'plural_obj': 'Объекты',
    'rp_singular_obj': 'объекта',
    'rp_plural_obj': 'объектов',
    'template_prefix': 'companies_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'directories',
    'submenu': 'companies',
    'show_urla': 'show_companies',
    'create_urla': 'create_company',
    'edit_urla': 'edit_company',
    'model': Company,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_companies(request, *args, **kwargs):
    """Вывод объектов"""
    return show_view(request,
                     model_vars = companies_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_company(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объектов"""
    return edit_view(request,
                     model_vars = companies_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def companies_positions(request, *args, **kwargs):
    """Изменение позиций объектов"""
    result = {}
    mh_vars = companies_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_companies(request, *args, **kwargs):
    """Поиск объектов"""
    return search_view(request,
                       model_vars = companies_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )
