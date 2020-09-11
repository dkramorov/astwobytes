# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
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
                                    Vik,
                                    ControlK,
                                    HoldingKSS,
                                    MechTest,
                                    NAX,
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
    extra_vars = {
        'welding_types': WELDING_TYPES,
    }
    return show_view(request,
                     model_vars = welders_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

def fill_certifications(request, row):
    """Заполнить удостоверения для сварщиков
       :param request: HttpRequest
       :param row: текущий Welder экземпляр
    """
    row.certification_set.all().delete()
    certifications = request.POST.get('certifications')
    if not certifications:
        return
    certifications = int(certifications)
    for i in range(certifications):
        cert = {}
        for field in ('number', 'welding_type'):
            value = request.POST.get('cert_%s_%s' % (field, i))
            cert[field] = value
        cert['welder'] = row
        Certification.objects.create(**cert)

def fill_cert_sections(request, row):
    """Заполнить группы технических устройств
       опасных производственных объектов
       :param request: HttpRequest
       :param row: текущий Welder экземпляр
    """
    row.certsections_set.all().delete()
    cert_sections = request.POST.get('section_sections')
    if not cert_sections:
        return
    cert_sections = int(cert_sections)
    for i in range(cert_sections):
        section = {}
        for field in ('group', 'certification', 'points'):
            value = request.POST.get('section_%s_%s' % (field, i))
            if field == 'certification':
                value = Certification.objects.filter(number=value).first()
            section[field] = value
        section['welder'] = row
        CertSections.objects.create(**section)

@login_required
def edit_welder(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование сварщиков"""
    mh_vars = welders_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
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
            context['certifications'] = row.certification_set.all().order_by('position')
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
                        fill_certifications(request, mh.row)
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
                        fill_certifications(request, row)
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

viks_vars = {
    'singular_obj': 'Акт ВИК',
    'plural_obj': 'Акты ВИК',
    'rp_singular_obj': 'акта ВИК',
    'rp_plural_obj': 'актов ВИК',
    'template_prefix': 'welders/viks_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'viks',
    'show_urla': 'show_viks',
    'create_urla': 'create_vik',
    'edit_urla': 'edit_vik',
    'model': Vik,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('welder', ),
}

@login_required
def show_viks(request, *args, **kwargs):
    """Вывод актов ВИК"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return show_view(request,
                     model_vars = viks_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_vik(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование актов ВИК"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return edit_view(request,
                     model_vars = viks_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def viks_positions(request, *args, **kwargs):
    """Изменение позиций актов ВИК"""
    result = {}
    mh_vars = viks_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_viks(request, *args, **kwargs):
    """Поиск актов ВИК"""
    return search_view(request,
                       model_vars = viks_vars,
                       cur_app = CUR_APP,
                       sfields = ('number', ), )

controlk_vars = {
    'singular_obj': 'УЗК/РК контроль',
    'plural_obj': 'УЗК/РК контроли',
    'rp_singular_obj': 'УЗК/РК контроля',
    'rp_plural_obj': 'УЗК/РК контролей',
    'template_prefix': 'welders/controlk_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'controlk',
    'show_urla': 'show_controlk',
    'create_urla': 'create_controlk',
    'edit_urla': 'edit_controlk',
    'model': ControlK,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('welder', ),
}

@login_required
def show_controlk(request, *args, **kwargs):
    """Вывод УЗК/РК контролей"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return show_view(request,
                     model_vars = controlk_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_controlk(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование УЗК/РК контролей"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
    }
    return edit_view(request,
                     model_vars = controlk_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def controlk_positions(request, *args, **kwargs):
    """Изменение позиций УЗК/РК контролей"""
    result = {}
    mh_vars = controlk_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_controlk(request, *args, **kwargs):
    """Поиск УЗК/РК контролей"""
    return search_view(request,
                       model_vars = controlk_vars,
                       cur_app = CUR_APP,
                       sfields = ('number', ), )

holding_kss_vars = {
    'singular_obj': 'Проведение КСС',
    'plural_obj': 'Проведения КСС',
    'rp_singular_obj': 'Проведения КСС',
    'rp_plural_obj': 'Проведений КСС',
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
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('welder', ),
}

@login_required
def show_holding_kss(request, *args, **kwargs):
    """Вывод проведений КСС"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
        'holding_choices': HoldingKSS.holding_choices,
        'spent_length_choices': HoldingKSS.spent_length_choices,
        'material_choices': MATERIALS,
    }
    return show_view(request,
                     model_vars = holding_kss_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_holding_kss(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование проведений КСС"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
        'spent_length_choices': HoldingKSS.spent_length_choices,
        'holding_choices': HoldingKSS.holding_choices,
        'material_choices': MATERIALS,
    }
    return edit_view(request,
                     model_vars = holding_kss_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

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

nax_vars = {
    'singular_obj': 'Аттестат НАКС',
    'plural_obj': 'Аттестаты НАКС',
    'rp_singular_obj': 'аттестата НАКС',
    'rp_plural_obj': 'аттестатов НАКС',
    'template_prefix': 'welders/nax_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'welders',
    'submenu': 'nax',
    'show_urla': 'show_nax',
    'create_urla': 'create_nax',
    'edit_urla': 'edit_nax',
    'model': NAX,
    #'custom_model_permissions': WeldingJoint,
    'select_related_list': ('welder', ),
}

@login_required
def show_nax(request, *args, **kwargs):
    """Вывод аттестатов НАКС"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
        'welding_type_choices': WELDING_TYPES,
        'identification_choices': NAX.identification_choices,
    }
    return show_view(request,
                     model_vars = nax_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_nax(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование аттестатов НАКС"""
    extra_vars = {
        'insert_breadcrumbs': insert_breadcrumbs,
        'welding_type_choices': WELDING_TYPES,
        'identification_choices': NAX.identification_choices,
    }
    return edit_view(request,
                     model_vars = nax_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def nax_positions(request, *args, **kwargs):
    """Изменение позиций аттестатов НАКС"""
    result = {}
    mh_vars = nax_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_nax(request, *args, **kwargs):
    """Поиск аттестатов НАКС"""
    return search_view(request,
                       model_vars = nax_vars,
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