# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

from apps.main_functions.date_time import str_to_date
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, ModelHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view,
                                              special_model_vars, )

from apps.weld.enums import WELDING_TYPES, MATERIALS
from apps.weld.welder_model import (Welder,
                                    Certification,
                                    CertSections,
                                    Defectoscopist,
                                    LetterOfGuarantee,
                                    HoldingKSS,
                                    MechTest,
                                    AdmissionSheet, )
from apps.weld.views import CUR_APP

welders_vars = {
    'singular_obj': 'Сварщик',
    'plural_obj': 'Сварщики',
    'rp_singular_obj': 'сварщика',
    'rp_plural_obj': 'сварщиков',
    'template_prefix': 'welders/welders_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'welders',
    'show_urla': 'show_welders',
    'create_urla': 'create_welder',
    'edit_urla': 'edit_welder',
    'model': Welder,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('subject', ),
    'search_result_format': ('{} - {}', 'name stigma'),
}

# заготовленные хлебные крошки
insert_breadcrumbs = ({
    'name': welders_vars['plural_obj'],
    'link': reverse_lazy('%s:%s' % (CUR_APP, welders_vars['show_urla'])),
 }, )

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

letters_of_guarantee_vars = {
    'singular_obj': 'Гарантийное письмо',
    'plural_obj': 'Гарантийные письма',
    'rp_singular_obj': 'гарантийного письма',
    'rp_plural_obj': 'гарантийных писем',
    'template_prefix': 'welders/letters_of_guarantee_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'letters_of_guarantee',
    'show_urla': 'show_letters_of_guarantee',
    'create_urla': 'create_letter_of_guarantee',
    'edit_urla': 'edit_letter_of_guarantee',
    'model': LetterOfGuarantee,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('welder', ),
}

@login_required
def show_letters_of_guarantee(request, *args, **kwargs):
    """Вывод гарантийных писем"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return show_view(request,
                     model_vars = letters_of_guarantee_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_letter_of_guarantee(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование гарантийных писем"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return edit_view(request,
                     model_vars = letters_of_guarantee_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def letters_of_guarantee_positions(request, *args, **kwargs):
    """Изменение позиций гарантийных писем"""
    result = {}
    mh_vars = letters_of_guarantee_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_letters_of_guarantee(request, *args, **kwargs):
    """Поиск гарантийных писем"""
    return search_view(request,
                       model_vars = letters_of_guarantee_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

mechtest_vars = {
    'singular_obj': 'Мехиспытание',
    'plural_obj': 'Мехиспытания',
    'rp_singular_obj': 'мехиспытания',
    'rp_plural_obj': 'мехиспытаний',
    'template_prefix': 'welders/mechtest_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'mechtest',
    'show_urla': 'show_mechtest',
    'create_urla': 'create_mechtest',
    'edit_urla': 'edit_mechtest',
    'model': MechTest,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('welder', ),
}

@login_required
def show_mechtest(request, *args, **kwargs):
    """Вывод мехиспытаний"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return show_view(request,
                     model_vars = mechtest_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_mechtest(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование мехиспытаний"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return edit_view(request,
                     model_vars = mechtest_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def mechtest_positions(request, *args, **kwargs):
    """Изменение позиций мехиспытаний"""
    result = {}
    mh_vars = mechtest_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_mechtest(request, *args, **kwargs):
    """Поиск мехиспытаний"""
    return search_view(request,
                       model_vars = mechtest_vars,
                       cur_app = CUR_APP,
                       sfields = ('number', ), )

admission_sheet_vars = {
    'singular_obj': 'Лист допуска',
    'plural_obj': 'Листы допуска',
    'rp_singular_obj': 'листа допуска',
    'rp_plural_obj': 'листов допуска',
    'template_prefix': 'welders/admission_sheet_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'admission_sheet',
    'show_urla': 'show_admission_sheet',
    'create_urla': 'create_admission_sheet',
    'edit_urla': 'edit_admission_sheet',
    'model': AdmissionSheet,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('welder', ),
}

@login_required
def show_admission_sheet(request, *args, **kwargs):
    """Вывод листов допуска"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return show_view(request,
                     model_vars = admission_sheet_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_admission_sheet(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование листов допуска"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return edit_view(request,
                     model_vars = admission_sheet_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def admission_sheet_positions(request, *args, **kwargs):
    """Изменение позиций листов допуска"""
    result = {}
    mh_vars = admission_sheet_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_admission_sheet(request, *args, **kwargs):
    """Поиск листов допуска"""
    return search_view(request,
                       model_vars = admission_sheet_vars,
                       cur_app = CUR_APP,
                       sfields = ('number', ), )

defectoscopists_vars = {
    'singular_obj': 'Дефектоскопист',
    'plural_obj': 'Дефектоскописты',
    'rp_singular_obj': 'дефектоскописта',
    'rp_plural_obj': 'дефектоскопистов',
    'template_prefix': 'welders/defectoscopists_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'defectoscopists',
    'submenu': 'defectoscopists',
    'show_urla': 'show_defectoscopists',
    'create_urla': 'create_defectoscopist',
    'edit_urla': 'edit_defectoscopist',
    'model': Defectoscopist,
    #'custom_model_permissions': WeldingJoint,
    #'select_related_list': ('subject', ),
    'search_result_format': ('{} - {}', 'name stigma'),
}

@login_required
def show_defectoscopists(request, *args, **kwargs):
    """Вывод дефектоскопистов"""
    extra_vars = {
        'state_choices': Defectoscopist.state_choices,
    }
    return show_view(request,
                     model_vars = defectoscopists_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_defectoscopist(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование дефектоскопистов"""
    extra_vars = {
        'state_choices': Defectoscopist.state_choices,
    }
    return edit_view(request,
                     model_vars = defectoscopists_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def defectoscopists_positions(request, *args, **kwargs):
    """Изменение позиций дефектоскопистов"""
    result = {}
    mh_vars = defectoscopists_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_defectoscopists(request, *args, **kwargs):
    """Поиск дефектоскопистов"""
    return search_view(request,
                       model_vars = defectoscopists_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', 'stigma'), )

certifications_vars = {
    'singular_obj': 'Удостоверение',
    'plural_obj': 'Удостоверения',
    'rp_singular_obj': 'удостоверения',
    'rp_plural_obj': 'удостоверений',
    'template_prefix': 'welders/certifications_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'certifications',
    'show_urla': 'show_certifications',
    'create_urla': 'create_certification',
    'edit_urla': 'edit_certification',
    'model': Certification,
    'select_related_list': ('welder', 'welder__subject'),
}

@login_required
def show_certifications(request, *args, **kwargs):
    """Вывод удостоверений"""
    mh_vars = certifications_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context
    context['insert_breadcrumbs'] = insert_breadcrumbs
    context['welding_types'] = WELDING_TYPES
    context['group_choices'] = CertSections.group_choices
    special_model_vars(mh, mh_vars, context)
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        ids_certs = {row.id: [] for row in rows}
        # Вытаскиваем группы для удостоверений
        cert_sections = CertSections.objects.filter(certification__in=ids_certs.keys()).values('certification', 'group', 'points')
        for cert_section in cert_sections:
            ids_certs[cert_section['certification']].append(cert_section)

        for row in rows:
            item = object_fields(row)
            item['sections'] = ids_certs.get(row.id, [])

            welding_view = 'ТТ'
            with_tt = False
            with_mk = False
            for section in item['sections']:
                if section['group'] == 12:
                    with_mk = True
                else:
                    with_tt = True
            if with_mk:
                welding_view = 'МК'
            if with_mk and with_tt:
                welding_view = 'ТТ/МК'
            item['certsections__group'] = welding_view
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

def fill_cert_sections(request, row):
    """Заполнить группы технических устройств
       опасных производственных объектов
       :param request: HttpRequest
       :param row: Certification экземпляр удостоверения
    """
    row.certsections_set.all().delete()
    cert_sections = request.POST.get('section_sections')
    if not cert_sections:
        return
    cert_sections = int(cert_sections)
    for i in range(cert_sections):
        section = {}
        for field in ('group', 'points'):
            value = request.POST.get('section_%s_%s' % (field, i))
            section[field] = value
        section['welder'] = row.welder
        section['certification'] = row
        CertSections.objects.create(**section)

@login_required
def edit_certification(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование удостоверений"""
    mh_vars = certifications_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
    context['extra_vars'] = insert_breadcrumbs
    context['welding_types'] = WELDING_TYPES
    special_model_vars(mh, mh_vars, context)
    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        if action in ('create', 'edit'):
            context['group_choices'] = CertSections.group_choices
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
            context['cert_sections'] = row.certsections_set.select_related('certification').all().order_by('position')
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
                    if mh.error:
                        context['error'] = mh.error
                    else:
                        fill_cert_sections(request, mh.row)
                        context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    if mh.error:
                        context['error'] = mh.error
                    else:
                        fill_cert_sections(request, row)
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
def certifications_positions(request, *args, **kwargs):
    """Изменение удостоверений"""
    result = {}
    mh_vars = certifications_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_certifications(request, *args, **kwargs):
    """Поиск удостоверений"""
    result = {'results': []}
    model = certifications_vars['model']
    mh = ModelHelper(model, request)
    mh.select_related_add('welder')
    mh_vars = certifications_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('number', 'welder__stigma', 'welder__stigma2', 'welder__name')

    rows = mh.standard_show(only_fields=('id', 'number', 'welder__stigma', 'welder__name'))

    for row in rows:
        name = '%s %s %s' % (row.number, row.welder.name, row.welder.stigma)
        result['results'].append({'text': name, 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

holding_kss_vars = {
    'singular_obj': 'Проведение КСС',
    'plural_obj': 'Проведения КСС',
    'rp_singular_obj': 'проведения КСС',
    'rp_plural_obj': 'проведений КСС',
    'template_prefix': 'welders/holding_kss_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'holding_kss',
    'show_urla': 'show_holding_kss',
    'create_urla': 'create_holding_kss',
    'edit_urla': 'edit_holding_kss',
    'model': HoldingKSS,
}

@login_required
def show_holding_kss(request, *args, **kwargs):
    """Вывод проведений КСС"""
    mh_vars = holding_kss_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('welder')
    mh.select_related_add('welder__subject')
    mh.select_related_add('certification')
    context = mh.context
    context['insert_breadcrumbs'] = insert_breadcrumbs
    context['welding_types'] = WELDING_TYPES
    context['materials'] = MATERIALS
    context['group_choices'] = CertSections.group_choices
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        ids_certs = {row.certification.id: [] for row in rows if row.certification}
        # Вытаскиваем группы для удостоверений
        cert_sections = CertSections.objects.filter(certification__in=ids_certs.keys()).values('certification', 'group', 'points')
        for cert_section in cert_sections:
            ids_certs[cert_section['certification']].append(cert_section)

        for row in rows:
            item = object_fields(row)
            item['sections'] = []
            if row.certification:
                item['sections'] = ids_certs.get(row.certification.id, [])
            welding_view = 'ТТ'
            with_tt = False
            with_mk = False
            for section in item['sections']:
                if section['group'] == 12:
                    with_mk = True
                else:
                    with_tt = True
            if with_mk:
                welding_view = 'МК'
            if with_mk and with_tt:
                welding_view = 'ТТ/МК'
            item['certification__certsections__group'] = welding_view
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

def check_cert_for_welder(row):
    """Проверка на то, что удостоверение принадлежит сварщику
       :param row: Проведение КСС
    """
    if not row or not row.welder or not row.certification:
        return False
    cert_welder = Certification.objects.filter(pk=row.certification.id).values_list('welder', flat=True).first()
    if cert_welder == row.welder.id:
        return True
    return False

@login_required
def edit_holding_kss(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование проведений КСС"""
    mh_vars = holding_kss_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('welder')
    mh.select_related_add('welder__subject')
    mh.select_related_add('certification')
    context = mh.context
    context['extra_vars'] = insert_breadcrumbs
    context['welding_types'] = WELDING_TYPES
    context['materials'] = MATERIALS
    special_model_vars(mh, mh_vars, context)
    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        if action in ('create', 'edit'):
            context['group_choices'] = CertSections.group_choices
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
            if not check_cert_for_welder(mh.row):
                context['error'] = 'Сварщик и удостоверение должны быть заполнены и удостоверение должно принадлежать выбранному сварщику'
        elif not mh.error and action == 'img' and request.FILES:
            mh.uploads()
    if not mh.error and mh.row:
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def holding_kss_positions(request, *args, **kwargs):
    """Изменение позиций проведений КСС"""
    result = {}
    mh_vars = holding_kss_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_holding_kss(request, *args, **kwargs):
    """Поиск проведений КСС"""
    return search_view(request,
                       model_vars = holding_kss_vars,
                       cur_app = CUR_APP,
                       sfields = ('number', ), )