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

from .models import (WeldingJoint,
                     Base,
                     Contract,
                     Titul,
                     Line,
                     Scheme,
                     Joint,
                     Material,
                     JoinType,
                     Welder, )

CUR_APP = 'welding'
welding_vars = {
    'singular_obj': 'Заявка на стык',
    'plural_obj': 'Заявки на стыки',
    'rp_singular_obj': 'заявки на стык',
    'rp_plural_obj': 'заявок на стыки',
    'template_prefix': 'welding_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'welding',
    'show_urla': 'show_welding',
    'create_urla': 'create_welding',
    'edit_urla': 'edit_welding',
    'model': WeldingJoint,
    #'custom_model_permissions': WeldingJoint,
}

def api(request, action: str = 'welding'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'welding':
    #    result = ApiHelper(request, welding_vars, CUR_APP)
    result = ApiHelper(request, welding_vars, CUR_APP)
    return result

@login_required
def show_welding(request, *args, **kwargs):
    """Вывод бланк-заявок
       :param request: HttpRequest
    """
    mh_vars = welding_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('base')
    mh.select_related_add('contract')
    mh.select_related_add('titul')
    mh.select_related_add('joint')
    mh.select_related_add('joint__line')
    mh.select_related_add('scheme')
    mh.select_related_add('material')
    mh.select_related_add('join_type')

    context = mh.context
    context['workshift_choices'] = mh.model.workshift_choices
    context['control_choices'] = mh.model.control_choices
    context['welding_conn_view_choices'] = mh.model.welding_conn_view_choices
    context['welding_type_choices'] = mh.model.welding_type_choices
    context['category_choices'] = mh.model.category_choices
    context['control_result_choices'] = mh.model.control_result_choices

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
            item['workshift'] = row.get_workshift_display()
            item['control_type'] = row.get_control_type_display()
            item['welding_conn_view'] = row.get_welding_conn_view_display()
            item['welding_type'] = row.get_welding_type_display()
            item['category'] = row.get_category_display()
            item['control_result'] = row.get_control_result_display()
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
def edit_welding(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование бланк-заявок
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = welding_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('base')
    mh.select_related_add('contract')
    mh.select_related_add('titul')
    mh.select_related_add('joint')
    mh.select_related_add('scheme')
    mh.select_related_add('material')
    mh.select_related_add('join_type')

    context = mh.context
    context['workshift_choices'] = mh.model.workshift_choices
    context['control_choices'] = mh.model.control_choices
    context['welding_conn_view_choices'] = mh.model.welding_conn_view_choices
    context['welding_type_choices'] = mh.model.welding_type_choices
    context['category_choices'] = mh.model.category_choices
    context['control_result_choices'] = mh.model.control_result_choices

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
def welding_positions(request, *args, **kwargs):
    """Изменение позиций бланк-заявок
       :param request: HttpRequest
    """
    result = {}
    mh_vars = welding_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_welding(request, *args, **kwargs):
    """Поиск бланк-заявок
       :param request: HttpRequest
    """
    result = {'results': []}
    mh = ModelHelper(WeldingJoint, request)
    mh_vars = welding_vars.copy()
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

bases_vars = {
    'singular_obj': 'Установка',
    'plural_obj': 'Установки',
    'rp_singular_obj': 'установки',
    'rp_plural_obj': 'установок',
    'template_prefix': 'bases_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'bases',
    'show_urla': 'show_bases',
    'create_urla': 'create_base',
    'edit_urla': 'edit_base',
    'model': Base,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_bases(request, *args, **kwargs):
    """Вывод установок"""
    return show_view(request,
                     model_vars = bases_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_base(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование установок"""
    return edit_view(request,
                     model_vars = bases_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def bases_positions(request, *args, **kwargs):
    """Изменение позиций установок"""
    result = {}
    mh_vars = bases_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_bases(request, *args, **kwargs):
    """Поиск установок"""
    return search_view(request,
                       model_vars = bases_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

contracts_vars = {
    'singular_obj': 'Договор',
    'plural_obj': 'Договоры',
    'rp_singular_obj': 'договора',
    'rp_plural_obj': 'договоров',
    'template_prefix': 'bases_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'contracts',
    'show_urla': 'show_contracts',
    'create_urla': 'create_contract',
    'edit_urla': 'edit_contract',
    'model': Contract,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_contracts(request, *args, **kwargs):
    """Вывод контрактов"""
    return show_view(request,
                     model_vars = contracts_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_contract(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование контрактов"""
    return edit_view(request,
                     model_vars = contracts_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def contracts_positions(request, *args, **kwargs):
    """Изменение позиций контрактов"""
    result = {}
    mh_vars = contracts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_contracts(request, *args, **kwargs):
    """Поиск контрактов"""
    return search_view(request,
                       model_vars = contracts_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

tituls_vars = {
    'singular_obj': 'Титул',
    'plural_obj': 'Титулы',
    'rp_singular_obj': 'титула',
    'rp_plural_obj': 'титулов',
    'template_prefix': 'tituls_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'tituls',
    'show_urla': 'show_tituls',
    'create_urla': 'create_titul',
    'edit_urla': 'edit_titul',
    'model': Titul,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_tituls(request, *args, **kwargs):
    """Вывод титулов"""
    return show_view(request,
                     model_vars = tituls_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_titul(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование титулов"""
    return edit_view(request,
                     model_vars = tituls_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def tituls_positions(request, *args, **kwargs):
    """Изменение позиций титулов"""
    result = {}
    mh_vars = tituls_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_tituls(request, *args, **kwargs):
    """Поиск титулов"""
    return search_view(request,
                       model_vars = tituls_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

lines_vars = {
    'singular_obj': 'Линия',
    'plural_obj': 'Линии',
    'rp_singular_obj': 'линии',
    'rp_plural_obj': 'линий',
    'template_prefix': 'lines_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'lines',
    'show_urla': 'show_lines',
    'create_urla': 'create_line',
    'edit_urla': 'edit_line',
    'model': Line,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_lines(request, *args, **kwargs):
    """Вывод линий"""
    return show_view(request,
                     model_vars = lines_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_line(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование линий"""
    return edit_view(request,
                     model_vars = lines_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def lines_positions(request, *args, **kwargs):
    """Изменение позиций линий"""
    result = {}
    mh_vars = lines_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_lines(request, *args, **kwargs):
    """Поиск линий"""
    return search_view(request,
                       model_vars = lines_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

schemes_vars = {
    'singular_obj': 'Изом. схема',
    'plural_obj': 'Изом. схемы',
    'rp_singular_obj': 'изом. схемы',
    'rp_plural_obj': 'изом. схем',
    'template_prefix': 'schemes_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'schemes',
    'show_urla': 'show_schemes',
    'create_urla': 'create_scheme',
    'edit_urla': 'edit_scheme',
    'model': Scheme,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_schemes(request, *args, **kwargs):
    """Вывод изометрических схем"""
    return show_view(request,
                     model_vars = schemes_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_scheme(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование изометрических схем"""
    return edit_view(request,
                     model_vars = schemes_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def schemes_positions(request, *args, **kwargs):
    """Изменение позиций изометрических схем"""
    result = {}
    mh_vars = schemes_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_schemes(request, *args, **kwargs):
    """Поиск изометрических схем"""
    return search_view(request,
                       model_vars = schemes_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

joints_vars = {
    'singular_obj': 'Стык',
    'plural_obj': 'Стыки',
    'rp_singular_obj': 'стыка',
    'rp_plural_obj': 'стыков',
    'template_prefix': 'joints_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'joints',
    'show_urla': 'show_joints',
    'create_urla': 'create_joint',
    'edit_urla': 'edit_joint',
    'model': Joint,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('line', ),
}

@login_required
def show_joints(request, *args, **kwargs):
    """Вывод стыков"""
    return show_view(request,
                     model_vars = joints_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_joint(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование стыков"""
    return edit_view(request,
                     model_vars = joints_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def joints_positions(request, *args, **kwargs):
    """Изменение позиций стыков"""
    result = {}
    mh_vars = joints_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_joints(request, *args, **kwargs):
    """Поиск стыков"""
    return search_view(request,
                       model_vars = joints_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', 'line__name'), )


materials_vars = {
    'singular_obj': 'Материал',
    'plural_obj': 'Материалы',
    'rp_singular_obj': 'материала',
    'rp_plural_obj': 'материалов',
    'template_prefix': 'materials_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
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

join_types_vars = {
    'singular_obj': 'Тип соединения',
    'plural_obj': 'Типы соединений',
    'rp_singular_obj': 'типа соединения',
    'rp_plural_obj': 'типов соединений',
    'template_prefix': 'join_types_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'join_types',
    'show_urla': 'show_join_types',
    'create_urla': 'create_join_type',
    'edit_urla': 'edit_join_type',
    'model': JoinType,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_join_types(request, *args, **kwargs):
    """Вывод типов соединений"""
    return show_view(request,
                     model_vars = join_types_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_join_type(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование типов соединений"""
    return edit_view(request,
                     model_vars = join_types_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def join_types_positions(request, *args, **kwargs):
    """Изменение позиций типов соединений"""
    result = {}
    mh_vars = join_types_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_join_types(request, *args, **kwargs):
    """Поиск типов соединений"""
    return search_view(request,
                       model_vars = join_types_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )


welders_vars = {
    'singular_obj': 'Сварщик',
    'plural_obj': 'Сварщики',
    'rp_singular_obj': 'сварщика',
    'rp_plural_obj': 'сварщиков',
    'template_prefix': 'welders_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'welders',
    'show_urla': 'show_welders',
    'create_urla': 'create_welder',
    'edit_urla': 'edit_welder',
    'model': Welder,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_welders(request, *args, **kwargs):
    """Вывод сварщиков"""
    return show_view(request,
                     model_vars = welders_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_welder(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование сварщиков"""
    return edit_view(request,
                     model_vars = welders_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def welders_positions(request, *args, **kwargs):
    """Изменение позиций сварщиков"""
    result = {}
    mh_vars = welders_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_welders(request, *args, **kwargs):
    """Поиск сварщиков"""
    return search_view(request,
                       model_vars = welders_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', 'stigma'), )

