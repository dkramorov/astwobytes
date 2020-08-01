# -*- coding:utf-8 -*-
import json
import datetime

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

from apps.weld.enums import WELDING_TYPES, MATERIALS, JOIN_TYPES, get_welding_joint_state
from apps.weld.welder_model import (Welder,
                                    LetterOfGuarantee, )
from .models import WeldingJoint, Joint

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
    state = kwargs.get('state')

    mh_vars = welding_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('titul')
    mh.select_related_add('joint')
    mh.select_related_add('joint__line')
    mh.select_related_add('joint__line__titul')
    mh.select_related_add('joint__line__titul__subject')
    mh.select_related_add('joint__line__titul__subject__company')
    context = mh.context

    context['repair_choices'] = WeldingJoint.repair_choices
    context['workshift_choices'] = WeldingJoint.workshift_choices
    context['control_choices'] = WeldingJoint.control_choices
    context['welding_conn_view_choices'] = WeldingJoint.welding_conn_view_choices
    context['welding_type_choices'] = WELDING_TYPES
    context['category_choices'] = WeldingJoint.category_choices
    context['control_result_choices'] = WeldingJoint.control_result_choices
    context['material_choices'] = MATERIALS
    context['join_types'] = JOIN_TYPES
    context['state_choices'] = WeldingJoint.state_choices

    if state and not 'state' in context['fas']['filters']:
        context['fas']['filters']['state'] = get_welding_joint_state(state)
        context['submenu'] = '%s_%s' % (mh_vars['submenu'], state)

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
    context['url_form'] = reverse('%s:%s' % (CUR_APP, mh_vars['create_urla']),
                                  kwargs={'action': 'form'})
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
    mh.select_related_add('titul')
    mh.select_related_add('joint')
    mh.select_related_add('joint__line')
    mh.select_related_add('joint__line__titul')
    mh.select_related_add('joint__line__titul__subject')
    mh.select_related_add('joint__line__titul__subject__company')

    context = mh.context
    context['repair_choices'] = WeldingJoint.repair_choices
    context['workshift_choices'] = WeldingJoint.workshift_choices
    context['control_choices'] = WeldingJoint.control_choices
    context['welding_conn_view_choices'] = WeldingJoint.welding_conn_view_choices
    context['welding_type_choices'] = WELDING_TYPES
    context['category_choices'] = WeldingJoint.category_choices
    context['control_result_choices'] = WeldingJoint.control_result_choices
    context['material_choices'] = MATERIALS
    context['join_types'] = JOIN_TYPES
    context['state_choices'] = WeldingJoint.state_choices
    context['today'] = datetime.datetime.today().strftime('%d.%m.%Y')

    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        # Вытаскиваем узел, по которому создается заявка
        joint_str = request.GET.get('joint')
        if joint_str:
            context['joint'] = Joint.objects.select_related(
                'line',
                'line__titul',
                'line__base',
                'line__titul__subject',
                'line__titul__subject__company',
            ).filter(pk=joint_str).first()

        if action == 'create':
            mh.breadcrumbs_add({
                'link': mh.url_create,
                'name': '%s %s' % (mh.action_create, mh.rp_singular_obj),
            })
        elif action in ('edit', 'form') and row:
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
        mh.url_form = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'form', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.url_edit
    else:
        mh.url_form = reverse('%s:%s' % (CUR_APP, mh_vars['create_urla']),
                              kwargs={'action': 'form'})
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    if action == 'form':
        mh.breadcrumbs_add({
            'link': mh.url_form,
            'name': '%s' % (mh.singular_obj, ),
        })
        template = '%sform.html' % (mh.template_prefix, )
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
