# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from apps.weld.enums import WELDING_TYPES, MATERIALS
from apps.weld.welder_model import (Welder,
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
    'select_related_list': ('company', ),
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
