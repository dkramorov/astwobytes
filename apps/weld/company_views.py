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
from apps.main_functions.model_helper import create_model_helper, get_user_permissions
from apps.main_functions.files import check_path, full_path
from apps.files.models import Files
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view,
                                              special_model_vars, )

from apps.weld.enums import (WELDING_TYPES,
                             MATERIALS,
                             JOIN_TYPES,
                             DIAMETERS,
                             WELDING_JOINT_STATES, )
from apps.weld.models import WeldingJoint, JointWelder
from apps.weld.welder_model import Welder
from apps.weld.company_model import (Company,
                                     Subject,
                                     Titul,
                                     Base,
                                     Line,
                                     Joint,
                                     LineFile, )
from apps.weld.views import CUR_APP

def update_welding_join_welders(request, mh):
    """Заполненение сварщиками заявки на сварку
       Вспомогательная функция для сохранения
       :param request: HttpRequest
       :param mh: ModelHelper для Joint
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
                                   joint=mh.row,
                                   actually=actually,
                                   position=i, )

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
        'project_joint_count',
        'project_dinc',
        'new_joints',
        'in_progress_joints',
        'repair_joints',
        'complete_joints',
        'complete_dinc',
        'titul__name',
    )
    fk_keys = {
        'titul': ('name', ),
    }
    # Права на файлы к линии
    extra_vars = {
        'files_permissions': get_user_permissions(request.user, LineFile),
    }
    return show_view(request,
                     model_vars = lines_vars,
                     cur_app = CUR_APP,
                     only_fields = only_fields,
                     fk_only_keys = fk_keys,
                     extra_vars = extra_vars, )

@login_required
def edit_line(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование линий"""
    mh_vars = lines_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
    # Права на файлы к линии
    context['files_permissions'] = get_user_permissions(request.user, LineFile)
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
            context['files'] = row.get_files()
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
    elif request.method == 'POST':
        pass_fields = ('new_joints',
                       'in_progress_joints',
                       'repair_joints',
                       'complete_joints',
                       'complete_dinc', )
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

        elif action == 'file' and request.FILES:
            # Загрузка файла в LineFile
            mh.files_add('path')
            new_file = Files.objects.create(
                desc = mh.row.name,
                name = request.FILES['path'].name,
            )
            mh.uploads(row=new_file)
            if new_file.path:
                line_file = LineFile.objects.create(
                    line=mh.row,
                    file=new_file, )
                new_file.update_mimetype()
                context['success'] = 'Файл загружен'
                context['file'] = {
                    'id': line_file.id,
                    'path': new_file.path,
                    'name': new_file.name,
                    'mime': new_file.mime,
                    'folder': new_file.get_folder(),
                }
            else:
                new_file.delete()
                context['error'] = 'Не удалось загрузить файл'

        elif not mh.error and action == 'img' and request.FILES:
            mh.uploads()
    if not mh.error and mh.row:
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action in ('img', 'file'):
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

line_files_vars = {
    'singular_obj': 'Файл линии',
    'plural_obj': 'Файлы линий',
    'rp_singular_obj': 'файла линии',
    'rp_plural_obj': 'файлов линий',
    'template_prefix': 'line_files_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welding',
    'submenu': 'line_files',
    'show_urla': 'show_line_files',
    #'create_urla': 'create_line_file',
    'edit_urla': 'edit_line_file',
    'model': LineFile,
    'select_related_list': ('file', 'line'),
}

@login_required
def show_line_files(request, *args, **kwargs):
    """Вывод файлов для линий"""
    return show_view(request,
                     model_vars = line_files_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_line_file(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование файла линии"""
    mh_vars = line_files_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('line')
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
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
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
        #'line__titul__subject',
        #'line__titul__subject__company',
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
    context['welding_type_choices'] = WELDING_TYPES
    context['material_choices'] = MATERIALS
    context['join_types'] = JOIN_TYPES
    context['welding_conn_view_choices'] = Joint.welding_conn_view_choices
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
            'welding_type',
            'material',
            'join_type_from',
            'join_type_to',
            'welding_conn_view',
            'dinc',
            'welding_date',
            'welding_joint__state',
            'line__name',
            'line__titul__name',
            #'line__titul__subject__name',
            #'line__titul__subject__company__name',
        )
        rows = mh.standard_show(only_fields=only_fields,
                                related_fields=('welding_joint', ), )
        result = []
        fk_keys = {
            'line': ('name', ),
            'titul': ('name', ),
            #'subject': ('name', ),
            #'company': ('name', ),
            'welding_joint': ('state', ),
        }
        ids_stigmas = {row.id: [] for row in rows}
        stigmas = JointWelder.objects.select_related('welder').filter(joint__in=ids_stigmas.keys()).values('joint', 'welder__stigma')
        for stigma in stigmas:
            ids_stigmas[stigma['joint']].append(stigma['welder__stigma'])
        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys,
                                 related_fields=('welding_joint', ), )
            item['stigma'] = []
            if row.id in ids_stigmas:
                item['stigma'] = ids_stigmas[row.id]
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
    context['state_choices'] = WELDING_JOINT_STATES
    context['welding_type_choices'] = WELDING_TYPES
    context['material_choices'] = MATERIALS
    context['diameters'] = DIAMETERS
    context['join_types'] = JOIN_TYPES
    context['welding_conn_view_choices'] = Joint.welding_conn_view_choices
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
            context['welders'] = row.get_welders()
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
                        update_welding_join_welders(request, mh)
                        context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit' and can_edit:
                if mh.permissions['edit']:
                    mh.save_row()
                    if mh.error:
                        context['error'] = mh.error
                    else:
                        update_welding_join_welders(request, mh)
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
