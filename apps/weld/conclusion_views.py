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
from apps.main_functions.model_helper import create_model_helper, get_user_permissions
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )
from apps.main_functions.pdf_helper import render_pdf
from apps.files.models import Files

from apps.weld.enums import (WELDING_TYPE_DESCRIPTIONS,
                             CONCLUSION_STATES,
                             WELDING_JOINT_STATES, )
from apps.weld.models import WeldingJoint, WeldingJointState
from apps.weld.conclusion_model import (JointConclusion,
                                        RKFrames,
                                        JointConclusionFile, )
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
    context['conclusion_states'] = CONCLUSION_STATES
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'welding_joint__request_number',
            'date',
            'state',
        )
        rows = mh.standard_show(only_fields=only_fields)
        result = []
        fk_keys = {
            'welding_joint': ('request_number', ),
        }
        # ---------------------------
        # Выбираем снимки с дефектами
        # по РК заключениям
        # ---------------------------
        ids_rows = [row.id for row in rows]
        rk_frames = RKFrames.objects.filter(joint_conclusion__in=ids_rows).exclude(state=1).values('joint_conclusion', 'defects', 'notice')
        ids_frames = {}
        for rk_frame in rk_frames:
            conclusion_id = rk_frame['joint_conclusion']
            if not conclusion_id in ids_frames:
                ids_frames[conclusion_id] = []
            ids_frames[conclusion_id].append({
                'defects': rk_frame['defects'],
                'notice': rk_frame['notice'],
            })

        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys)
            item['actions'] = row.id
            if row.vik_active:
                item['vik'] = {'defects': row.vik_defects}
            if row.rk_active:
                item['rk'] = ids_frames.get(row.id)
            if row.pvk_active:
                item['pvk'] = {'defects': row.pvk_defects}
            if row.uzk_active:
                item['uzk'] = {
                    'defects': row.uzk_defects,
                    'notice': row.uzk_notice,
                }

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

def welding_joint_fields(welding_joint):
    """Вспомогательная функция, чтобы вернуть словарь
       по стыку
       :param welding_joint: стык
    """
    return {
        'id': welding_joint.id,
        'request_number': welding_joint.request_number,
        'diameter': welding_joint.joint.diameter,
        'join_type_from': welding_joint.joint.get_join_type_from_display(),
        'join_type_to': welding_joint.joint.get_join_type_to_display(),
        'material': welding_joint.joint.get_material_display(),
        'welding_conn_view': welding_joint.joint.get_welding_conn_view_display(),
        'created': welding_joint.created.strftime('%d-%m-%Y %H:%M:%S'),
        'state': welding_joint.state,
        'get_state_display': welding_joint.get_state_display(),
        'side_thickness': welding_joint.joint.side_thickness,
        'welding_date': welding_joint.joint.welding_date.strftime('%d-%m-%Y') if welding_joint.joint.welding_date else '',
    }

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

    # Права на файлы к заключению
    context['files_permissions'] = get_user_permissions(request.user, JointConclusionFile)
    context['welding_joint_state_permissions'] = get_user_permissions(request.user, WeldingJointState)

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        # ---------------------------------------------------
        # Вытаскиваем заявку, по которой создается заключение
        # ---------------------------------------------------
        welding_joint_str = request.GET.get('welding_joint')
        if welding_joint_str and not mh.row:
            welding_joint = WeldingJoint.objects.select_related('joint').filter(pk=welding_joint_str).first()
            if not welding_joint:
                return redirect('%s?error=not_found' % (mh.root_url, ))

            welding_joint.join_type_from = welding_joint.joint.get_join_type_from_display()
            welding_joint.join_type_to = welding_joint.joint.get_join_type_to_display()
            welding_joint.material = welding_joint.joint.get_material_display()
            welding_joint.welding_conn_view = welding_joint.joint.get_welding_conn_view_display()
            context['welding_joint'] = welding_joint_fields(welding_joint)
            context['welders'] = {}
            if welding_joint.joint:
                context['welders'] = welding_joint.joint.get_welders()
            context['welding_type'] = '?'
            for item in WELDING_TYPE_DESCRIPTIONS:
                if welding_joint.joint.welding_type == item[0]:
                    context['welding_type'] = item[1]
                    break

        if action in ('create', 'edit'):
            context['welding_type_descriptions'] = WELDING_TYPE_DESCRIPTIONS
            context['conclusion_states'] = CONCLUSION_STATES
            context['pvk_control_choices'] = JointConclusion.pvk_control_choices
            context['state_choices'] = WELDING_JOINT_STATES

        if action in ('edit', 'pdf_vik', 'pdf_rk', 'pdf_pvk', 'pdf_uzk'):
            context['welding_type'] = '%s и %s' % (
                WELDING_TYPE_DESCRIPTIONS[0][1],
                WELDING_TYPE_DESCRIPTIONS[1][1],
            )
            for item in WELDING_TYPE_DESCRIPTIONS:
                if row.welding_joint.joint.welding_type == item[0]:
                    context['welding_type'] = item[1]
                    break
            context['rk_frames'] = row.rkframes_set.all().order_by('position')
            # Номера заключений
            context.update(row.get_conclusion_numbers(row.welding_joint))

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
                context['welding_joint'] = welding_joint_fields(row.welding_joint)
                context['all_conclusions'] = JointConclusion.objects.filter(welding_joint=row.welding_joint).values_list('id', flat=True).order_by('repair')
            context['files'] = row.get_files()
            context['welders'] = {}
            if row.welding_joint.joint:
                context['welders'] = row.welding_joint.joint.get_welders()

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
            })
            context['welders'] = {}
            if row.welding_joint and row.welding_joint.joint:
                context['welders'] = row.welding_joint.joint.get_welders()
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
        # Общий статус ставится в save по заключениям
        pass_fields = ('state', 'repair')
        mh.post_vars(pass_fields=pass_fields)
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
                analog = JointConclusion.objects.filter(welding_joint=welding_joint).order_by('-repair').first()
                if not mh.row and analog:
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
        elif action == 'file' and request.FILES:
            # Принятую заявку не редактируем
            if mh.row.welding_joint.state == 3:
                context['error'] = 'Нельзя изменить принятую заявку'
            else:
                # Загрузка файла в JointConclusionFile
                mh.files_add('path')
                new_file = Files.objects.create(
                    desc = mh.row.welding_joint.request_number,
                    name = request.FILES['path'].name,
                )
                mh.uploads(row=new_file)
                if new_file.path:
                    joint_file = JointConclusionFile.objects.create(
                        joint_conclusion=mh.row,
                        file=new_file, )
                    new_file.update_mimetype()
                    context['success'] = 'Файл загружен'
                    context['file'] = {
                        'id': joint_file.id,
                        'path': new_file.path,
                        'name': new_file.name,
                        'mime': new_file.mime,
                        'folder': new_file.get_folder(),
                    }
                else:
                    new_file.delete()
                    context['error'] = 'Не удалось загрузить файл'
    if not mh.error and mh.row:
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action in ('img', 'file'):
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

conclusion_files_vars = {
    'singular_obj': 'Файл заключения на заявку',
    'plural_obj': 'Файлы заключения на заявку',
    'rp_singular_obj': 'файла заключения на заявку',
    'rp_plural_obj': 'файлов заключений на заявки',
    'template_prefix': 'conclusions/files_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'conclusions',
    'submenu': 'conclusions',
    'show_urla': 'show_conclusion_files',
    #'create_urla': 'create_conclusion_file',
    'edit_urla': 'edit_conclusion_file',
    'model': JointConclusionFile,
    'select_related_list': ('file', 'joint_conclusion'),
}

@login_required
def show_conclusion_files(request, *args, **kwargs):
    """Вывод файлов для заключений на заявку"""
    return show_view(request,
                     model_vars = conclusion_files_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_conclusion_file(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование файлов для заключений на заявку"""
    mh_vars = conclusion_files_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('joint_conclusion')
    mh.select_related_add('joint_conclusion__welding_joint')
    row = mh.get_row(row_id)
    context = mh.context

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
                if mh.row.joint_conclusion.welding_joint.state == 3:
                    context['error'] = 'Нельзя изменить принятую заявку'
                else:
                    row.delete()
                    mh.row = None
                    context['success'] = '%s удалено' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
        elif action == 'download' and row:
            # Возвращаем файл по имени
            path = '%s%s' % (row.file.get_folder(), row.file.path)
            if not check_path(path):
                with open(full_path(path), 'rb') as f:
                    response = HttpResponse(f.read(), content_type=row.file.mime)
                response['Content-Disposition'] = row.file.content_disposition_for_cyrillic_name(row.file.name)
                return response

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
                    if mh.row.welding_joint.state == 3:
                        context['error'] = 'Нельзя изменить принятую заявку'
                    else:
                        mh.save_row()
                        context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
        elif action == 'img' and request.FILES:
            mh.uploads()
    if mh.row:
        context['row'] = object_fields(mh.row)
        if mh.row.file:
            context['row']['file'] = object_fields(mh.row.file)
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)