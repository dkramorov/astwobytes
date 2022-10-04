# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

from apps.main_functions.date_time import str_to_date
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, tabulator_filters_and_sorters
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.views_helper import (
    show_view,
    edit_view,
    search_view,
    special_model_vars,
)
from apps.site.polis.models import Polis, PolisMember

CUR_APP = 'polis'
polis_vars = {
    'singular_obj': 'Полюс',
    'plural_obj': 'Полюсы',
    'rp_singular_obj': 'полюсов',
    'rp_plural_obj': 'полюсов',
    'template_prefix': 'polis_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'polis',
    'submenu': 'polis',
    'show_urla': 'show_polises',
    'create_urla': 'create_polis',
    'edit_urla': 'edit_polis',
    'model': Polis,
    #'custom_model_permissions': Phones,
    'select_related_list': ('order', ),
}

def api(request, action: str = 'polis'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'phones':
    #    result = ApiHelper(request, polis_vars, CUR_APP)
    result = ApiHelper(request, polis_vars, CUR_APP)
    return result

@login_required
def show_polises(request, *args, **kwargs):
    """Вывод паспортных данных
       :param request: HttpRequest
    """
    mh_vars = polis_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('order')
    context = mh.context
    special_model_vars(mh, mh_vars, context)
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
        #    'id',
        #    'shopper__name',
        #    'shopper__phone',
        #    'birthday',
        #    'series',
        #    'number',
        #    'issued',
        #    'issued_date',
        #    'registration',
        )
        fk_keys = {
        #    'shopper': ('name',
        #                'phone'),
        }
        rows = mh.standard_show(only_fields=only_fields)
        result = []
        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys)
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
    return render(request, template, context)

@login_required
def edit_polis(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование паспортных данных
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    members = PolisMember.objects.filter(polis__in=(row_id, ))
    insurance_members = [{
        'id': member.id,
        'name': member.name,
        'birthday': member.birthday.strftime('%d-%m-%Y') if member.birthday else '',
    } for member in members]
    extra_vars = {
        'insurance_members': insurance_members,
    }
    result = edit_view(request,
                       model_vars = polis_vars,
                       cur_app = CUR_APP,
                       action = action,
                       row_id = row_id,
                       extra_vars = extra_vars)
    if request.method == 'POST':
        if action in ('create', 'edit'):
            mh_vars = polis_vars.copy()
            mh = create_model_helper(mh_vars, request, CUR_APP, action)
            if mh.permissions['edit']:
                PolisMember.objects.filter(polis_id=row_id).delete()
                members_count = int(request.POST.get('members'))
                for i in range(members_count):
                    name, birthday = (
                        request.POST.get('insurance_member_name_%s' % i),
                        str_to_date(request.POST.get('insurance_member_birthday_%s' % i)),
                    )
                    PolisMember.objects.create(polis_id=row_id, name=name, birthday=birthday)
    return result

@login_required
def polis_positions(request, *args, **kwargs):
    """Изменение позиций паспортных данных
       :param request: HttpRequest
    """
    result = {}
    mh_vars = polis_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_polises(request, *args, **kwargs):
    """Поиск паспортных данных
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = polis_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

