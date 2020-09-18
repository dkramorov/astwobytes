# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Sum

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view,
                                              special_model_vars, )

from apps.weld.enums import WELDING_JOINT_STATES
from apps.weld.models import WeldingJoint
from apps.weld.company_model import Company, Subject, Titul, Base, Line, Joint
from apps.weld.views import CUR_APP

companies_vars = {
    'singular_obj': 'Компания',
    'plural_obj': 'Компании',
    'rp_singular_obj': 'компании',
    'rp_plural_obj': 'компаний',
    'template_prefix': 'directories/companies_',
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
    'search_result_format': ('{}', 'name'),
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

subjects_vars = {
    'singular_obj': 'Объект',
    'plural_obj': 'Объекты',
    'rp_singular_obj': 'объекта',
    'rp_plural_obj': 'объектов',
    'template_prefix': 'directories/subjects_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'directories',
    'submenu': 'subjects',
    'show_urla': 'show_subjects',
    'create_urla': 'create_subject',
    'edit_urla': 'edit_subject',
    'model': Subject,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('company', ),
    'search_result_format': ('{}', 'name'),
}

@login_required
def show_subjects(request, *args, **kwargs):
    """Вывод объектов"""
    return show_view(request,
                     model_vars = subjects_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_subject(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объекта"""
    return edit_view(request,
                     model_vars = subjects_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def subjects_positions(request, *args, **kwargs):
    """Изменение позиций объектов"""
    result = {}
    mh_vars = subjects_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_subjects(request, *args, **kwargs):
    """Поиск объектов"""
    return search_view(request,
                       model_vars = subjects_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

tituls_vars = {
    'singular_obj': 'Титул',
    'plural_obj': 'Титулы',
    'rp_singular_obj': 'титула',
    'rp_plural_obj': 'титулов',
    'template_prefix': 'directories/tituls_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'directories',
    'submenu': 'tituls',
    'show_urla': 'show_tituls',
    'create_urla': 'create_titul',
    'edit_urla': 'edit_titul',
    'model': Titul,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('subject', 'subject__company'),
    'search_result_format': ('{}', 'name'),
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

bases_vars = {
    'singular_obj': 'Установка',
    'plural_obj': 'Установки',
    'rp_singular_obj': 'установки',
    'rp_plural_obj': 'установок',
    'template_prefix': 'directories/bases_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'directories',
    'submenu': 'bases',
    'show_urla': 'show_bases',
    'create_urla': 'create_base',
    'edit_urla': 'edit_base',
    'model': Base,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('titul', 'titul__subject', 'titul__subject__company'),
    'search_result_format': ('{}', 'name'),
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

lines_vars = {
    'singular_obj': 'Линия',
    'plural_obj': 'Линии',
    'rp_singular_obj': 'линии',
    'rp_plural_obj': 'линий',
    'template_prefix': 'directories/lines_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'directories',
    'submenu': 'lines',
    'show_urla': 'show_lines',
    'create_urla': 'create_line',
    'edit_urla': 'edit_line',
    'model': Line,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': (
        'titul',
        'titul__subject',
        'titul__subject__company',
    ),
    'search_result_format': ('{} титул {}', 'name titul__name'),
}

@login_required
def show_lines(request, *args, **kwargs):
    """Вывод линий"""
    only_fields = (
        'id',
        'name',
        'img',
        'new_joints',
        'in_progress_joints',
        'repair_joints',
        'complete_joints',
        'titul__name',
        'titul__subject__name',
        'titul__subject__company__name',
    )
    fk_keys = {
        'titul': ('name', ),
        'subject': ('name', ),
        'company': ('name', ),
    }

    return show_view(request,
                     model_vars = lines_vars,
                     cur_app = CUR_APP,
                     only_fields = only_fields,
                     fk_only_keys = fk_keys,
                     extra_vars = None, )

@login_required
def edit_line(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование линий"""
    pass_fields = ('new_joints',
                   'in_progress_joints',
                   'repair_joints',
                   'complete_joints', )
    return edit_view(request,
                     model_vars = lines_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     pass_fields = pass_fields,
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

joints_vars = {
    'singular_obj': 'Стык',
    'plural_obj': 'Стыки',
    'rp_singular_obj': 'стыка',
    'rp_plural_obj': 'стыков',
    'template_prefix': 'directories/joints_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'directories',
    'submenu': 'joints',
    'show_urla': 'show_joints',
    'create_urla': 'create_joint',
    'edit_urla': 'edit_joint',
    'model': Joint,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': (
        'line',
        'line__titul',
        'line__titul__subject',
        'line__titul__subject__company',
        'welding_joint',
    ),
    'search_result_format': ('{}, {}, {}, {}, {}', 'name line__name line__titul__name line__titul__subject__name line__titul__subject__company__name'),
}

@login_required
def show_joints(request, *args, **kwargs):
    """Вывод стыков"""
    mh_vars = joints_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context
    context['state_choices'] = WELDING_JOINT_STATES
    special_model_vars(mh, mh_vars, context)
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'name',
            'img',
            'diameter',
            'side_thickness',
            'dinc',
            'welding_date',
            'welding_joint__state',
            'line__name',
            'line__titul__name',
            'line__titul__subject__name',
            'line__titul__subject__company__name',
        )
        rows = mh.standard_show(only_fields=only_fields,
                                related_fields=('welding_joint', ), )
        result = []
        fk_keys = {
            'line': ('name', ),
            'titul': ('name', ),
            'subject': ('name', ),
            'company': ('name', ),
            'welding_joint': ('state', ),
        }
        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys,
                                 related_fields=('welding_joint', ), )
            item['actions'] = row.id
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            result.append(item)

        if request.GET.get('page'):
            dinc = mh.query.aggregate(Sum('dinc'))
            result = {'data': result,
                      'last_page': mh.raw_paginator['total_pages'],
                      'total_records': mh.raw_paginator['total_records'],
                      'cur_page': mh.raw_paginator['cur_page'],
                      'by': mh.raw_paginator['by'],
                      'dinc': dinc['dinc__sum'],
            }

        return JsonResponse(result, safe=False)
    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def edit_joint(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование стыков"""
    mh_vars = joints_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
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
        pass_fields = ()
        mh.post_vars(pass_fields=pass_fields)
        can_edit = True

        if row and hasattr(row, 'welding_joint') and row.welding_joint.state:
            state = row.welding_joint.state
            if state > 1:
                can_edit = False
                context['error'] = 'Нельзя отредактировать стык со статусом %s' % row.welding_joint.get_state_display()
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
            if action == 'edit' and can_edit:
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
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

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
                       sfields = ('name', ), )
