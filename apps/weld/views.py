# -*- coding:utf-8 -*-
import json
import datetime
from urllib.parse import quote

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.files import full_path, check_path, file_size
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, get_user_permissions
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )
from apps.main_functions.pdf_helper import render_pdf
from apps.files.models import Files

from apps.weld.enums import (WELDING_TYPES,
                             MATERIALS,
                             JOIN_TYPES,
                             WELDING_JOINT_STATES,
                             get_welding_joint_state, )
from apps.weld.welder_model import (Welder,
                                    LetterOfGuarantee, )
from .models import (WeldingJoint,
                     JointWelder,
                     WeldingJointFile,
                     WeldingJointState,
                     JointConclusion,
                     recalc_joints, )

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
    'search_result_format': ('{}', 'request_number'),
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

def manual(request, action: str = 'welder'):
    """Документация в PDF"""
    template = 'manual/welder.html'
    context = {
        'menu': 'manual',
        'submenu': 'welder',
    }
    return render(request, template, context)

@login_required
def show_welding(request, *args, **kwargs):
    """Вывод бланк-заявок
       :param request: HttpRequest
    """
    state = kwargs.get('state')

    mh_vars = welding_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('joint')
    mh.select_related_add('joint__line')
    mh.select_related_add('joint__line__titul')
    mh.select_related_add('joint__line__titul__subject')
    mh.select_related_add('joint__line__titul__subject__company')
    context = mh.context
    context['welding_joint_state_permissions'] = get_user_permissions(request.user, WeldingJointState)

    context['repair_choices'] = WeldingJoint.repair_choices
    context['workshift_choices'] = WeldingJoint.workshift_choices
    context['control_choices'] = WeldingJoint.control_choices
    context['welding_conn_view_choices'] = WeldingJoint.welding_conn_view_choices
    context['welding_type_choices'] = WELDING_TYPES
    context['category_choices'] = WeldingJoint.category_choices
    context['control_result_choices'] = WeldingJoint.control_result_choices
    context['material_choices'] = MATERIALS
    context['join_types'] = JOIN_TYPES
    context['state_choices'] = WELDING_JOINT_STATES

    if state and not 'state' in context['fas']['filters']:
        context['fas']['filters']['state'] = get_welding_joint_state(state)
        context['submenu'] = '%s_%s' % (mh_vars['submenu'], state)

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'request_number',
            'request_control_date',
            'joint__name',
            'joint__line__name',
            'joint__line__titul__name',
            'joint__line__titul__subject__name',
            'joint__line__titul__subject__company__name',
            'repair',
            'cutout',
            'diameter',
            'side_thickness',
            'material',
            'join_type_from',
            'join_type_to',
            'welding_date',
            'workshift',
            'control_type',
            'welding_conn_view',
            'welding_type',
            'category',
            'control_result',
            'conclusion_number',
            'conclusion_date',
            'notice',
            'state',
        )
        rows = mh.standard_show(only_fields=only_fields)
        result = []
        for row in rows:
            fk_keys = {
                'joint': ('name', ),
                'line': ('name', ),
                'titul': ('name', ),
                'subject': ('name', ),
                'company': ('name', ),
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
    context['url_form'] = reverse('%s:%s' % (CUR_APP, mh_vars['create_urla']),
                                  kwargs={'action': 'form'})
    return render(request, template, context)

def update_welding_join_welders(request, mh):
    """Заполненение сварщиками заявки на сварку
       Вспомогательная функция для сохранения
    """
    if not (mh.permissions['create'] and mh.row and mh.row.id):
        return
    # Заполнение сварщиков
    mh.row.jointwelder_set.all().delete()
    for i in range(1, 5):
        wid = request.POST.get('welder%s' % i)
        if not wid:
            continue
        wid = int(wid)
        welder = Welder.objects.filter(pk=wid).first()
        if not welder:
            continue
        actually = True if i >= 3 else False
        JointWelder.objects.create(welder=welder,
                                   welding_joint=mh.row,
                                   actually=actually,
                                   position=i, )

def update_welding_joint_state(request, mh):
    """Обновление статуса заявки
       Вспомогательная функция для сохранения
    """
    permissions = get_user_permissions(request.user, WeldingJointState)
    if not permissions['edit'] or not mh.row.id:
        return
    state = mh.row.state
    new_state = request.POST.get('new_state')
    if new_state:
        new_state = get_welding_joint_state(new_state)
    # Новая => В работе
    new2progress = state == 1 and new_state == 2
    # В ремонте => В работе
    repair2progress = state == 4 and new_state == 2
    # В работе => Готово
    progress2complete = state == 2 and new_state == 3
    # -----------------
    # Установить статус
    # -----------------
    if new2progress or repair2progress or progress2complete:
        WeldingJointState.objects.create(
            from_state=state,
            to_state=new_state,
            user=request.user,
            welding_joint=mh.row, )
        params = {'state': new_state}
        if not mh.row.receiver:
            params['receiver'] = request.user
        WeldingJoint.objects.filter(pk=mh.row.id).update(**params)
        # Пересчитать процент готовности линии
        if mh.row.joint and mh.row.joint.line:
            line = mh.row.joint.line
            recalc_joints(line)
        return True
    return False

@login_required
def edit_welding(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование бланк-заявок
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = welding_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('joint')
    mh.select_related_add('joint__line')
    mh.select_related_add('joint__line__titul')
    mh.select_related_add('joint__line__titul__subject')
    mh.select_related_add('joint__line__titul__subject__company')
    mh.select_related_add('requester')
    mh.select_related_add('receiver')

    context = mh.context
    # Права на файлы к заявке
    context['files_permissions'] = get_user_permissions(request.user, WeldingJointFile)
    context['welding_joint_state_permissions'] = get_user_permissions(request.user, WeldingJointState)

    context['repair_choices'] = WeldingJoint.repair_choices
    context['workshift_choices'] = WeldingJoint.workshift_choices
    context['control_choices'] = WeldingJoint.control_choices
    context['welding_conn_view_choices'] = WeldingJoint.welding_conn_view_choices
    context['welding_type_choices'] = WELDING_TYPES
    context['category_choices'] = WeldingJoint.category_choices
    context['control_result_choices'] = WeldingJoint.control_result_choices
    context['material_choices'] = MATERIALS
    context['join_types'] = JOIN_TYPES
    context['state_choices'] = WELDING_JOINT_STATES
    context['today'] = datetime.datetime.today().strftime('%d.%m.%Y')

    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        # Вытаскиваем узел, по которому создается заявка
        # На данный момент считаем, что на один стык
        # можно создать несколько заявок, возможно, это переиграется
        joint_str = request.GET.get('joint')
        if joint_str and not mh.row:
            joint = Joint.objects.select_related(
                'line',
                'line__titul',
                'line__base',
                'line__titul__subject',
                'line__titul__subject__company',
            ).filter(pk=joint_str).first()
            context['row'] = {
                'joint': joint,
            }
            if not joint:
                return redirect('%s?error=not_found' % (mh.root_url, ))
            # -------------------------------------
            # На один стык должна быть одна заявка,
            # если на данный стык уже есть заявка,
            # тогда переадресовываем на нее
            # -------------------------------------
            analog = WeldingJoint.objects.filter(joint=joint).first()
            if analog:
                params = {'action': 'form', 'row_id': analog.id}
                form = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']), kwargs=params)
                return redirect(form)
        if action in ('edit', 'form', 'pdf') and row:
            if row.id:
                context['welders'] = {}
                welders = row.jointwelder_set.select_related('welder').all()
                for welder in welders:
                    context['welders'][welder.position] = welder.welder
                if row.requester:
                    context['requester'] = {
                        'name': '%s' % row.requester.customuser,
                        'function': '%s' % row.requester.customuser.function,
                        'login': row.requester.username,
                        'id': row.requester.id,
                    }
                if row.receiver:
                    context['receiver'] = {
                        'name': '%s' % row.receiver.customuser,
                        'function': '%s' % row.receiver.customuser.function,
                        'login': row.receiver.username,
                        'id': row.receiver.id,
                    }
                context['files'] = row.get_files()
                if row.joint and row.joint.line:
                    context['total_joints'] = row.joint.line.get_total_joints()

        if action == 'create':
            mh.breadcrumbs_add({
                'link': mh.url_create,
                'name': '%s %s' % (mh.action_create, mh.rp_singular_obj),
            })
        elif action in ('edit', 'form') and mh.row:
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
            })
            context['joint'] = mh.row.joint
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
        elif action == 'pdf' and row:
            context['row'] = row
            context['logo'] = full_path('misc/logo_standard.png')
            return render_pdf(
                request,
                template = 'pdf/welding_form.html',
                context = context,
                download = False,
                fname = 'welding_joint_%s' % row.joint.id,
            )

    elif request.method == 'POST':
        pass_fields = ()
        mh.post_vars(pass_fields=pass_fields)
        if action in ('create', 'form') or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model(set_fields={'state': 1})
                    mh.save_row()
                    update_welding_join_welders(request, mh)
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            elif action == 'edit' and mh.row:

                # ------------------------------
                # Редактирование пока что бреем,
                # пока используем form действие,
                # т/к надо добавить файлы,
                # логирование смены статуса...
                # ------------------------------
                assert False

                if mh.permissions['edit']:
                    mh.save_row()
                    update_welding_join_welders(request, mh)
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            elif action == 'form':
                if mh.permissions['edit'] and mh.row:
                    # Принятую заявку не редактируем
                    if mh.row.state == 3:
                        context['error'] = 'Нельзя изменить принятую заявку'
                    else:
                        mh.save_row()
                        update_welding_join_welders(request, mh)
                        update_welding_joint_state(request, mh)
                        context['success'] = 'Данные успешно записаны'
                elif mh.permissions['create'] and not mh.row: # NOT!
                    mh.row = mh.model()
                    mh.save_row(set_fields={'state': 1})
                    update_welding_join_welders(request, mh)
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'

            # Если не удалось сохранить, значит не выбран стык
            if not mh.row or not mh.row.id:
                context['error'] = 'Выберите стык'
        elif action == 'file' and request.FILES:
            # Принятую заявку не редактируем
            if mh.row.state == 3:
                context['error'] = 'Нельзя изменить принятую заявку'
            else:
                # Загрузка файла в WeldingJointFile
                mh.files_add('path')
                new_file = Files.objects.create(
                    desc = mh.row.request_number,
                    name = request.FILES['path'].name,
                )
                mh.uploads(row=new_file)
                if new_file.path:
                    joint_file = WeldingJointFile.objects.create(
                        welding_joint=mh.row,
                        file=new_file, )
                    new_file.update_mimetype()
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

        elif action == 'img' and request.FILES:
            mh.uploads()
        elif action == 'state' and row:
            # Смена статуса заявки на стык
            if update_welding_joint_state(request, mh):
                context['success'] = 'Статус заявки обновлен'
            else:
                context['error'] = 'Статус заявки не обновлен'

    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        mh.url_form = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'form', 'row_id': mh.row.id})
        context['url_form'] = mh.url_form
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        # Не надо инфу о пользователях сливать
        context['row']['receiver'] = None
        context['row']['requester'] = None
        context['redirect'] = mh.url_edit
        if action == 'form':
            context['redirect'] = mh.url_form
    else:
        mh.url_form = reverse('%s:%s' % (CUR_APP, mh_vars['create_urla']),
                              kwargs={'action': 'form'})
    if request.is_ajax() or action in ('img', 'file', 'state'):
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
    """Поиск заявок на стык"""
    return search_view(request,
                       model_vars = welding_vars,
                       cur_app = CUR_APP,
                       sfields = ('request_number', ), )

welding_files_vars = {
    'singular_obj': 'Файл заявки на стык',
    'plural_obj': 'Файлы заявок на стык',
    'rp_singular_obj': 'файла заявки на стык',
    'rp_plural_obj': 'файлов заявки на стык',
    'template_prefix': 'welding_files_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'welding_files',
    'show_urla': 'show_welding_files',
    #'create_urla': 'create_welding_file',
    'edit_urla': 'edit_welding_file',
    'model': WeldingJointFile,
    'select_related_list': ('file', 'welding_joint'),
}

@login_required
def show_welding_files(request, *args, **kwargs):
    """Вывод файлов для заявок на стык"""
    return show_view(request,
                     model_vars = welding_files_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_welding_file(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование файла заявки на стык"""
    mh_vars = welding_files_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('welding_joint')
    context = mh.context
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
                if mh.row.welding_joint.state == 3:
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
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row)
        if mh.row.file:
            context['row']['file'] = object_fields(mh.row.file)
        context['redirect'] = mh.url_edit
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

welding_joint_state_vars = {
    'singular_obj': 'Статус заявки на стык',
    'plural_obj': 'Статусы заявок на стыки',
    'rp_singular_obj': 'статуса заявки на стык',
    'rp_plural_obj': 'статусов заявок на стыки',
    'template_prefix': 'logs/welding_joint_state_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'logs',
    'submenu': 'welding_joint_state',
    'show_urla': 'show_welding_joint_state',
    'create_urla': 'create_welding_joint_state',
    'edit_urla': 'edit_welding_joint_state',
    'model': WeldingJointState,
    #'custom_model_permissions': WeldingJoint,
}

@login_required
def show_welding_joint_state(request, *args, **kwargs):
    """Вывод истории изменений статусов заявок на стыки"""
    mh_vars = welding_joint_state_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('welding_joint')
    mh.select_related_add('user')
    mh.order_by_add('-date')
    context = mh.context
    context['state_choices'] = WELDING_JOINT_STATES
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'welding_joint__request_number',
            'date',
            'from_state',
            'to_state',
            'user__username',
        )
        rows = mh.standard_show(only_fields=only_fields)
        result = []
        for row in rows:
            item = object_fields(row)
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

@login_required
def edit_welding_joint_state(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование истории изменений статусов заявок на стыки"""
    mh_vars = welding_joint_state_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('welding_joint')
    mh.select_related_add('user')
    context = mh.context
    context['state_choices'] = WELDING_JOINT_STATES

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
            if row.user:
                context['customuser'] = {
                    'name': '%s' % row.user.customuser,
                    'function': '%s' % row.user.customuser.function,
                    'login': row.user.username,
                    'id': row.user.id,
                }
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
    elif request.method == 'POST':
        pass_fields = []
        mh.post_vars(pass_fields=pass_fields)
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
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    if mh.error:
                        context['error'] = mh.error
                    else:
                        context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'

    if not mh.error and mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['redirect'] = mh.url_edit
    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

conclusions_vars = {
    'singular_obj': 'Заключение',
    'plural_obj': 'Заключения',
    'rp_singular_obj': 'заключения',
    'rp_plural_obj': 'заключений',
    'template_prefix': 'conclusions_',
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
    return show_view(request,
                     model_vars = conclusions_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_conclusion(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование заключений (актов)"""
    return edit_view(request,
                     model_vars = conclusions_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

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
