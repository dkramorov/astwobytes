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
from apps.weld.company_model import Joint
from apps.weld.enums import (WELDING_TYPES,
                             MATERIALS,
                             JOIN_TYPES,
                             WELDING_JOINT_STATES,
                             WELDING_TYPE_DESCRIPTIONS,
                             CONCLUSION_STATES,
                             get_welding_joint_state, )
from apps.weld.welder_model import (Welder,
                                    LetterOfGuarantee, )
from apps.weld.conclusion_model import JointConclusion, RKFrames
from .models import (WeldingJoint,
                     JointWelder,
                     WeldingJointFile,
                     WeldingJointState,
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
    if action == 'lab':
        template = 'manual/lab.html'
        context.update({
            'submenu': 'lab',
        })
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
    mh.select_related_add('joint_conclusion')
    context = mh.context
    context['welding_joint_state_permissions'] = get_user_permissions(request.user, WeldingJointState)

    context['repair_choices'] = WeldingJoint.repair_choices
    context['workshift_choices'] = WeldingJoint.workshift_choices
    context['control_choices'] = WeldingJoint.control_choices
    context['welding_conn_view_choices'] = WeldingJoint.welding_conn_view_choices
    context['welding_type_choices'] = WELDING_TYPES
    context['category_choices'] = WeldingJoint.category_choices
    context['conclusion_states'] = CONCLUSION_STATES
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
            'notice',
            'state',
            'joint_conclusion__date',
            'joint_conclusion__state',
            'joint_conclusion__vik_defects',
            'joint_conclusion__pvk_defects',
            'joint_conclusion__uzk_defects',
        )
        rows = mh.standard_show(only_fields=only_fields,
                                related_fields=('joint_conclusion', ))
        result = []
        fk_keys = {
            'joint': ('name', ),
            'line': ('name', ),
            'titul': ('name', ),
            'subject': ('name', ),
            'company': ('name', ),
            'joint_conclusion': (
                'date',
                'state',
                'vik_defects',
                'pvk_defects',
                'uzk_defects', ),
        }
        # Только для ремонта
        conclusions = {row.joint_conclusion.id: [] for row in rows if hasattr(row, 'joint_conclusion')}
        rk_frames = []
        if conclusions:
            rk_frames = RKFrames.objects.filter(
                joint_conclusion__in=conclusions.keys(),
            ).exclude(state=1).values('joint_conclusion', 'defects')
        for rk_frame in rk_frames:
            conclusions[rk_frame['joint_conclusion']].append(rk_frame['defects'])
        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys,
                                 related_fields=('joint_conclusion', ))
            item['actions'] = row.id
            if hasattr(row, 'joint_conclusion'):
                if row.joint_conclusion.id in conclusions:
                    item['joint_conclusion']['rk_frames'] = conclusions[row.joint_conclusion.id]
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
    if not mh.row.id:
        return
    state = mh.row.state
    new_state = request.POST.get('new_state')
    if new_state:
        new_state = get_welding_joint_state(new_state)
    # Новая => В работе
    new2progress = state == 1 and new_state == 2 and permissions['edit']
    # Новая => Отклоненнные заявки
    # В работе => Отклоненные заявки
    new2rejected = state in (1, 2) and new_state == 5 and permissions['edit']
    # Отклоненная => В работе
    rejected2new = state == 5 and new_state == 1 and permissions['repair_completed']
    # В работе => В ремонте
    progress2repair = state == 2 and new_state == 4 and permissions['edit']
    # В ремонте => Новая
    repair2new = state == 4 and new_state == 1 and permissions['repair_completed']
    # В работе => Готово
    progress2complete = state == 2 and new_state == 3 and permissions['edit']
    # Новый стык
    none2new = state is None and new_state == 1
    # -----------------
    # Установить статус
    # -----------------
    if new2progress or progress2repair or repair2new or progress2complete or none2new or new2rejected or rejected2new:
        WeldingJointState.objects.create(
            from_state=state,
            to_state=new_state,
            user=request.user,
            welding_joint=mh.row, )
        params = {'state': new_state}
        if not mh.row.receiver and not none2new:
            params['receiver'] = request.user
        if progress2repair:
            params['repair'] = mh.row.repair or 0
            params['repair'] += 1
        WeldingJoint.objects.filter(pk=mh.row.id).update(**params)
        for k, v in params.items():
            setattr(mh.row, k, v)
        mh.row.request_number = mh.row.update_request_number()
        # ------------------------------------
        # Пересчитать процент готовности линии
        # ------------------------------------
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
    row = mh.get_row(row_id)
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
    context['conclusion_states'] = CONCLUSION_STATES
    context['material_choices'] = MATERIALS
    context['join_types'] = JOIN_TYPES
    context['state_choices'] = WELDING_JOINT_STATES
    context['today'] = datetime.datetime.today().strftime('%d.%m.%Y')

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        # ----------------------------------------------
        # Вытаскиваем узел, по которому создается заявка
        # ----------------------------------------------
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
                link = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                               kwargs={'action': 'form', 'row_id': analog.id})
                return redirect(link)
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
            context['state'] = mh.row.get_state_display()
            context['joint_conclusion'] = JointConclusion.objects.filter(welding_joint=mh.row).first()
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
        elif action == 'conclusion' and row:
            # Если по акту нет заключения,
            # переадресовываем на создание,
            conclusion = JointConclusion.objects.filter(welding_joint=row).first()
            # -------------------------------
            # Ссылки не импортирую тупо меняю
            # welding на conclusion
            # -------------------------------
            create_conclusion = mh_vars['create_urla'].replace('welding', 'conclusion')
            edit_conclusion = mh_vars['edit_urla'].replace('welding', 'conclusion')
            if conclusion:
                link = reverse('%s:%s' % (CUR_APP, edit_conclusion),
                               kwargs={'action': 'edit', 'row_id': conclusion.id})
                return redirect(link)
            link = reverse('%s:%s' % (CUR_APP, create_conclusion),
                           kwargs={'action': 'create'})
            return redirect('%s?welding_joint=%s' % (link, row.id))

    elif request.method == 'POST':
        pass_fields = ()
        mh.post_vars(pass_fields=pass_fields)
        if action in ('create', 'form') or (action == 'edit' and row):
            if action == 'create':
                # -------------------------
                # Создание пока что бреем,
                # используем form действие,
                # -------------------------
                assert False

                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    update_welding_join_welders(request, mh)
                    update_welding_joint_state(request, mh)
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            elif action == 'edit' and mh.row:
                # ------------------------------
                # Редактирование пока что бреем,
                # используем form действие,
                # ------------------------------
                assert False

                if mh.permissions['edit']:
                    mh.save_row()
                    update_welding_join_welders(request, mh)
                    update_welding_joint_state(request, mh)
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            elif action == 'form':
                # Заявки в ремонте даем редактировать,
                # чтобы гондоны смогли хотя бы со второго
                # раза правильно подать, а кто то с пятого
                if mh.row.state in (1, 5) and mh.permissions['repair']:
                    mh.permissions['edit'] = True

                if mh.permissions['edit'] and mh.row:
                    # Принятую заявку не редактируем
                    if mh.row.state == 3:
                        context['error'] = 'Нельзя изменить принятую заявку'
                    else:
                        # -------------------------------
                        # Изменять на другой стык не даем
                        # 1 стык = 1 заявка
                        # -------------------------------
                        mh.save_row(set_fields={'joint': mh.row.joint})
                        update_welding_join_welders(request, mh)
                        update_welding_joint_state(request, mh)
                        context['success'] = 'Данные успешно записаны'
                elif mh.permissions['create'] and not mh.row: # NOT!
                    # --------------------------
                    # Без стыка нельзя сохранить
                    # --------------------------
                    joint = None
                    joint_str = mh.row_vars.get('joint')
                    if joint_str:
                        joint = Joint.objects.filter(pk=joint_str).first()
                    if not joint:
                        context['error'] = 'Выберите стык'
                        return JsonResponse(context)
                    else:
                        analog = WeldingJoint.objects.filter(joint=joint).first()
                        if analog:
                            context['error'] = 'Вы создаете дубликат, переадресовываем на заявку...'
                            link = reverse(
                                '%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                                kwargs={'action': 'form', 'row_id': analog.id}
                            )
                            context['redirect_on_error'] = link
                            return JsonResponse(context)
                    mh.row = mh.model()
                    mh.save_row()
                    update_welding_join_welders(request, mh)
                    update_welding_joint_state(request, mh)
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

        elif action == 'img' and request.FILES:
            mh.uploads()
        elif action == 'state' and row:
            # Смена статуса заявки на стык
            if update_welding_joint_state(request, mh):
                context['success'] = 'Статус заявки обновлен'
            else:
                context['error'] = 'Статус заявки не обновлен'

    if mh.row:
        mh.url_form = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'form', 'row_id': mh.row.id})
        context['url_form'] = mh.url_form
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        # Не надо инфу о пользователях сливать
        context['row']['receiver'] = None
        context['row']['requester'] = None
        context['redirect'] = mh.get_url_edit()
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
        context['row'] = object_fields(mh.row)
        if mh.row.file:
            context['row']['file'] = object_fields(mh.row.file)
        context['redirect'] = mh.get_url_edit()
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
        fk_keys = {
            'welding_joint': ('request_number', ),
            'user': ('username'),
        }
        result = []
        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys, )
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
    row = mh.get_row(row_id)
    context = mh.context
    context['state_choices'] = WELDING_JOINT_STATES

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
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)
