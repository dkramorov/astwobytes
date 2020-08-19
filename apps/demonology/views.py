# -*- coding:utf-8 -*-
import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import management

from apps.main_functions.date_time import str_to_date
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import ModelHelper, create_model_helper
from apps.main_functions.api_helper import ApiHelper

from .models import Daemon

CUR_APP = 'demonology'
daemon_vars = {
    'singular_obj': 'Сервис-робот',
    'plural_obj': 'Сервисы-роботы',
    'rp_singular_obj': 'сервис-робота',
    'rp_plural_obj': 'сервис-роботов',
    'template_prefix': 'daemon_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'demonology',
    'submenu': 'daemon',
    'show_urla': 'show_daemons',
    'create_urla': 'create_daemon',
    'edit_urla': 'edit_daemon',
    'model': Daemon,
}

def api(request, action: str = 'daemon'):
    """Апи-метод для получения всех данных"""
    #if action == 'daemon':
    #    result = ApiHelper(request, daemon_vars, CUR_APP)
    result = ApiHelper(request, daemon_vars, CUR_APP)
    return result

@login_required
def show_daemons(request, *args, **kwargs):
    """Вывод объектов"""
    return show_view(request,
                     model_vars = daemon_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_daemon(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объекта"""
    mh_vars = daemon_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    row = mh.get_row(row_id)
    context = mh.context

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':

        if action in ('create', 'edit'):
            context['exec_paths'] = Daemon.exec_choices
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
        elif action == 'status' and row:
            context['status'] = management.call_command('update_daemons', status=row.get_name())

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
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def daemons_positions(request, *args, **kwargs):
    """Изменение позиций объектов"""
    result = {}
    mh_vars = daemon_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_daemons(request, *args, **kwargs):
    """Поиск объектов"""
    return search_view(request,
                       model_vars = daemon_vars,
                       cur_app = CUR_APP,
                       sfields = None, )
