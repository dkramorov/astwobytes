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
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )
from apps.contractors.services import get_info_by_inn
from apps.contractors.models import Contractor

CUR_APP = 'contractors'
contractors_vars = {
    'singular_obj': 'Контрагент',
    'plural_obj': 'Контрагенты',
    'rp_singular_obj': 'контрагента',
    'rp_plural_obj': 'контрагентов',
    'template_prefix': 'contractors_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'contractors',
    'submenu': 'contractors',
    'show_urla': 'show_contractors',
    'create_urla': 'create_contractor',
    'edit_urla': 'edit_contractor',
    'model': Contractor,
    #'custom_model_permissions': Contractor,
    'select_related_list': ('address', 'legal_address', 'bank_address'),
}

def api(request, action: str = 'contractors'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'contractors':
    #    result = ApiHelper(request, contractors_vars, CUR_APP)
    result = ApiHelper(request, contractors_vars, CUR_APP)
    return result

def import_xlsx(request, action: str = 'contractors'):
    """Апи-метод для сохранения данных из excel-файла
                     удаления данных по excel-файлу
       :param request: HttpRequest
       :param action: какую модель использовать
    """
    #if action == 'contractors':
    #    result = XlsxHelper(request, users_vars, CUR_APP)
    result = XlsxHelper(request, contractors_vars, CUR_APP,
                        cond_fields = ['code'])
    return result

@login_required
def show_contractors(request, *args, **kwargs):
    """Вывод контрагентов
       :param request: HttpRequest
    """
    extra_vars = {
        'ctype_choices': Contractor.ctype_choices,
        'import_xlsx_url': reverse('%s:%s' % (CUR_APP, 'import_xlsx'),
                                   kwargs={'action': 'contractors'}),
    }
    return show_view(request,
                     model_vars = contractors_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_contractor(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование контрагентов
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    extra_vars = {
        'ctype_choices': Contractor.ctype_choices,
    }
    return edit_view(request,
                     model_vars = contractors_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def contractors_positions(request, *args, **kwargs):
    """Изменение позиций контрагентов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = contractors_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_contractors(request, *args, **kwargs):
    """Поиск контрагентов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = contractors_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

@login_required
def info_by_inn(request, *args, **kwargs):
    """Изменение позиций контрагентов
       :param request: HttpRequest
    """
    method = request.GET if request.method == 'GET' else request.POST
    result = get_info_by_inn(method.get('inn'))
    return JsonResponse(result, safe=False)
