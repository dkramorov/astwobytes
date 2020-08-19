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
from apps.main_functions.files import full_path, check_path, file_size
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )
from apps.main_functions.pdf_helper import render_pdf
from apps.weld.enums import WELDING_TYPE_DESCRIPTIONS, CONCLUSION_STATES
from apps.weld.models import WeldingJoint
from apps.weld.conclusion_model import JointConclusion, RKFrames
from apps.weld.views import CUR_APP

conclusions_vars = {
    'singular_obj': 'Заключение',
    'plural_obj': 'Заключения',
    'rp_singular_obj': 'заключения',
    'rp_plural_obj': 'заключений',
    'template_prefix': 'conclusions/conclusions_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'conclusions',
    'submenu': 'conclusions',
    'show_urla': 'show_conclusions',
    'create_urla': 'create_conclusion',
    'edit_urla': 'edit_conclusion',
    'model': JointConclusion,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_conclusions(request, *args, **kwargs):
    """Вывод заключений (актов)"""
    mh_vars = conclusions_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('welding_joint')
    context = mh.context
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'welding_joint__request_number',
            'date',
        )
        rows = mh.standard_show(only_fields=only_fields)
        result = []
        for row in rows:
            fk_keys = {
                'welding_joint': ('request_number', ),
            }
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys)
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

def fill_rk_frames(request, row):
    """Заполнить снимки на РК заключение
       :param request: HttpRequest
       :param row: текущий Conclusion экземпляр
    """
    row.rkframes_set.all().delete()
    rk_frames = request.POST.get('rk_frames')
    if not rk_frames:
        return
    rk_frames = int(rk_frames)
    for i in range(rk_frames):
        frame = {}
        for field in ('number', 'sensitivity', 'state', 'defects', 'notice'):
            value = request.POST.get('rk_%s_%s' % (field, i))
            frame[field] = value
        frame['joint_conclusion'] = row
        RKFrames.objects.create(**frame)

@login_required
def edit_conclusion(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование заключений (актов)"""
    mh_vars = conclusions_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('welding_joint')
    mh.select_related_add('welding_joint__joint')
    mh.select_related_add('vik_controller')
    mh.select_related_add('vik_director')
    mh.select_related_add('rk_defectoscopist1')
    mh.select_related_add('rk_defectoscopist2')
    mh.select_related_add('rk_defectoscopist3')
    mh.select_related_add('pvk_director')
    mh.select_related_add('pvk_defectoscopist')
    mh.select_related_add('uzk_defectoscopist1')
    mh.select_related_add('uzk_defectoscopist2')
    mh.select_related_add('uzk_defectoscopist3')
    mh.select_related_add('uzk_operator')
    # pdf
    mh.select_related_add('welding_joint__joint__line')
    mh.select_related_add('welding_joint__joint__line__titul')
    mh.select_related_add('welding_joint__joint__line__titul__subject')
    mh.select_related_add('welding_joint__joint__line__titul__subject__company')
    row = mh.get_row(row_id)
    context = mh.context

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        # ---------------------------------------------------
        # Вытаскиваем заявку, по которой создается заключение
        # ---------------------------------------------------
        welding_joint_str = request.GET.get('welding_joint')
        if welding_joint_str and not mh.row:
            welding_joint = WeldingJoint.objects.filter(pk=welding_joint_str).values('id', 'request_number').first()
            context['welding_joint'] = welding_joint
            if not welding_joint:
                return redirect('%s?error=not_found' % (mh.root_url, ))

        if action in ('create', 'edit'):
            context['welding_type_descriptions'] = WELDING_TYPE_DESCRIPTIONS
            context['conclusion_states'] = CONCLUSION_STATES
            context['pvk_control_choices'] = JointConclusion.pvk_control_choices

        if action in ('edit', 'pdf_vik', 'pdf_rk', 'pdf_pvk', 'pdf_uzk'):
            context['welding_type'] = '%s и %s' % (
                WELDING_TYPE_DESCRIPTIONS[0][1],
                WELDING_TYPE_DESCRIPTIONS[1][1],
            )
            for item in WELDING_TYPE_DESCRIPTIONS:
                if row.welding_joint.welding_type == item[0]:
                    context['welding_type'] = item[1]
                    break
            context['rk_frames'] = row.rkframes_set.all().order_by('position')

        # TODO: нельзя сохранять дубль

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
            if row.welding_joint:
                context['welding_joint'] = {
                    'id': row.welding_joint.id,
                    'request_number': row.welding_joint.request_number,
                }
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
        elif action in ('pdf_vik', 'pdf_rk', 'pdf_pvk', 'pdf_uzk') and row:
            pdf_type = action.replace('pdf_', '')
            context.update({
                'row': row,
                'logo': full_path('misc/logo_standard.png'),
                'pdf_type': pdf_type,
                'joint': row.welding_joint.joint,
                'today': datetime.datetime.today(),
                'welders': {},
            })
            welders = row.welding_joint.jointwelder_set.select_related('welder').all()
            for welder in welders:
                context['welders'][welder.position] = welder.welder
            template = 'pdf/conclusion_%s_form.html' % pdf_type
            return render_pdf(
                request,
                template = template,
                context = context,
                download = False,
                fname = 'conclusion_%s_%s' % (
                    pdf_type,
                    row.welding_joint.joint.id,
                )
            )
    elif request.method == 'POST':
        mh.post_vars()
        if action == 'create' or (action == 'edit' and row):

            # ---------------------------------
            # Без заявки стыка нельзя сохранить
            # ---------------------------------
            welding_joint = None
            welding_joint_str = mh.row_vars.get('welding_joint')
            if welding_joint_str:
                welding_joint = WeldingJoint.objects.filter(pk=welding_joint_str).first()
            if not welding_joint:
                context['error'] = 'Выберите заявку на стык'
                return JsonResponse(context)
            else:
                analogs = JointConclusion.objects.filter(welding_joint=welding_joint)
                if mh.row:
                    analogs = analogs.exclude(pk=mh.row.id)
                if analogs:
                    analog = analogs[0]
                    context['error'] = 'Вы создаете дубликат, переадресовываем на заключение...'
                    link = reverse(
                        '%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                        kwargs={'action': 'edit', 'row_id': analog.id}
                    )
                    context['redirect_on_error'] = link
                    return JsonResponse(context)

            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    if mh.error:
                        context['error'] = mh.error
                    else:
                        context['success'] = 'Данные успешно записаны'
                        fill_rk_frames(request, mh.row)
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    # -----------------------
                    # Изменить заявку на стык
                    # не даем в заключении
                    # -----------------------
                    mh.save_row(set_fields={'welding_joint': mh.row.welding_joint})
                    if mh.error:
                        context['error'] = mh.error
                    else:
                        context['success'] = 'Данные успешно записаны'
                        fill_rk_frames(request, mh.row)
                else:
                    context['error'] = 'Недостаточно прав'

    if not mh.error and mh.row:
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def conclusions_positions(request, *args, **kwargs):
    """Изменение позиций заключений (актов)"""
    result = {}
    mh_vars = conclusions_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_conclusions(request, *args, **kwargs):
    """Поиск заключений (актов)"""
    return search_view(request,
                       model_vars = conclusions_vars,
                       cur_app = CUR_APP,
                       sfields = ('welding_joint__joint__name', ), )
