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

from apps.weld.material_model import Material
from apps.weld.views import CUR_APP

materials_vars = {
    'singular_obj': 'Материал',
    'plural_obj': 'Материалы',
    'rp_singular_obj': 'материала',
    'rp_plural_obj': 'материалов',
    'template_prefix': 'materials_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'directories',
    'submenu': 'materials',
    'show_urla': 'show_materials',
    'create_urla': 'create_material',
    'edit_urla': 'edit_material',
    'model': Material,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_materials(request, *args, **kwargs):
    """Вывод материалов"""
    return show_view(request,
                     model_vars = materials_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_material(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование материалов"""
    return edit_view(request,
                     model_vars = materials_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def materials_positions(request, *args, **kwargs):
    """Изменение позиций материалов"""
    result = {}
    mh_vars = materials_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_materials(request, *args, **kwargs):
    """Поиск материалов"""
    return search_view(request,
                       model_vars = materials_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

