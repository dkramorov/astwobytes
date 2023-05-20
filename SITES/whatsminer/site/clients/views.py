# -*- coding:utf-8 -*-
import os
import json
import logging
import traceback
import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core import management
from django.core.cache import cache

from apps.contractors.models import Contractor
from apps.main_functions.views_helper import (
    show_view,
    edit_view,
    search_view,
)

logger = logging.getLogger('main')

CUR_APP = 'clients'
clients_vars = {
    'singular_obj': 'Клиент',
    'plural_obj': 'Клиенты',
    'rp_singular_obj': 'клиента',
    'rp_plural_obj': 'клиентов',
    'template_prefix': 'clients_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'clients',
    'submenu': 'clients',
    'show_urla': 'show_clients',
    'create_urla': 'create_client',
    'edit_urla': 'edit_client',
    'model': Contractor,
    #'custom_model_permissions': Robots,
    #'select_related_list': ('name', ),
    'search_result_format': ('{} - {}', 'name'),
}

def api(request, action: str = 'clients'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    if action == 'clients':
        result = ApiHelper(request, clients_vars, CUR_APP)
    else:
        result = ApiHelper(request, clients_vars, CUR_APP)
    return result


@login_required
def show_clients(request, *args, **kwargs):
    """Вывод контрагентов
       :param request: HttpRequest
    """
    extra_vars = {
        'ctype_choices': Contractor.ctype_choices,
    }
    return show_view(request,
                     model_vars = clients_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_client(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование контрагентов
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    extra_vars = {
        'ctype_choices': Contractor.ctype_choices,
    }
    return edit_view(request,
                     model_vars = clients_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def clients_positions(request, *args, **kwargs):
    """Изменение позиций контрагентов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = clients_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_cleints(request, *args, **kwargs):
    """Поиск контрагентов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = clients_vars,
                       cur_app = CUR_APP,
                       sfields = None, )