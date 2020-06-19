# -*- coding: utf-8 -*-
import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.date_time import str_to_date
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import ModelHelper, create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.demonology.models import Daemon

from .models import Robots, Schedule

CUR_APP = 'binary_com'
binary_com_vars = {
    'singular_obj': 'Робот',
    'plural_obj': 'Роботы',
    'rp_singular_obj': 'робота',
    'rp_plural_obj': 'роботов',
    'template_prefix': 'binary_com_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'binary_com',
    'submenu': 'robots',
    'show_urla': 'show_robots',
    'create_urla': 'create_robot',
    'edit_urla': 'edit_robot',
    'model': Robots,
}

def api(request, action: str = 'binary_com'):
    """Апи-метод для получения всех данных"""
    #if action == 'binary_com':
    #    result = ApiHelper(request, binary_com_vars, CUR_APP)
    result = ApiHelper(request, binary_com_vars, CUR_APP)
    return result

@login_required
def show_robots(request, *args, **kwargs):
    """Вывод объектов"""
    mh_vars = binary_com_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
            item['actions'] = row.id
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            #item['exec_path'] = row.get_exec_path_display()
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
def edit_robot(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование объекта"""
    mh_vars = binary_com_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('daemon')
    context = mh.context

    row = mh.get_row(row_id)
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
            context['events'] = Schedule.event_choices
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
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.url_edit
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)

    context['url_schedule_constructor'] = reverse('%s:%s' % (CUR_APP, 'schedule_constructor'))
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def robots_positions(request, *args, **kwargs):
    """Изменение позиций объектов"""
    result = {}
    mh_vars = binary_com_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_robots(request, *args, **kwargs):
    """Поиск объектов"""
    result = {'results': []}
    mh = ModelHelper(Daemon, request)
    mh_vars = binary_com_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('id', 'name')
    rows = mh.standard_show()
    for row in rows:
        result['results'].append({'text': '%s (%s)' % (row.name, row.id), 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

@login_required
def schedule_constructor(request, *args, **kwargs):
    """Изменение расписаний демона через fullcalendar"""
    result = {}
    if not request.is_ajax():
        return JsonResponse(result, safe=False)

    body = request.GET
    if request.method == 'POST':
        body = request.POST

    robot_id = body.get('robot')
    schedule_id = body.get('id')
    action = body.get('action')
    title = body.get('title')
    event = None
    for schedule in Schedule.event_choices:
        if schedule[1] == title:
            event = schedule[0]
    start = str_to_date(body.get('start'))
    end = str_to_date(body.get('end'))
    robot = Robots.objects.filter(pk=robot_id).first()

    if action == 'new':
        if robot and event and start and end:
            new_schedule = Schedule.objects.create(robot=robot, event=event, start=start, end=end)
            result['start'] = start
            result['end'] = end
            result['id'] = new_schedule.id

    elif action == 'edit':
        schedule = Schedule.objects.filter(pk=schedule_id).first()
        if schedule and start and end:
            Schedule.objects.filter(pk=schedule.id).update(start=start, end=end)
            result['start'] = start
            result['end'] = end
            result['id'] = schedule.id

    elif action == 'show':
        if robot and start and end:
            result = []
            schedules = Schedule.objects.filter(robot=robot, start__gte=start, end__lte=end)
            for schedule in schedules:
                result.append({
                    'id': schedule.id,
                    'title': schedule.get_event_display(),
                    'start': schedule.start.strftime('%Y-%m-%dT%H:%M:%S'),
                    'end': schedule.end.strftime('%Y-%m-%dT%H:%M:%S'),
                    'allDay': False,
                })
    elif action == 'drop':
        schedule = Schedule.objects.filter(pk=schedule_id).first()
        if schedule:
            result['id'] = schedule.id
            schedule.delete()

    return JsonResponse(result, safe=False)

def get_schedule(request, *args, **kwargs):
    """Получение настроек расписания по текену для демона"""
    result = {}
    token = request.GET.get('token')
    now = datetime.datetime.today()
    daemon = Daemon.objects.filter(token=token).first()
    if daemon:
        schedule = Schedule.objects.filter(robot__daemon=daemon, start__lte=now, end__gte=now).only('event', 'start', 'end').first()
        if schedule:
            result = {
                'strategy': schedule.event,
                'start': schedule.start,
                'end': schedule.end,
            }
    return JsonResponse(result, safe=False)

def index(request, *args, **kwargs):
    """Фронтовый робот"""
    context = {}
    template = 'binary_com_index.html'
    return render(request, template, context)

@csrf_exempt
def generate_report(request, *args, **kwargs):
    """Создание отчета plotly по полученным данным"""
    result = {}

    now = datetime.datetime.today()

    if request.body:
      body = json.loads(request.body)
      token = body.get('token', '')
      ticks_data = body.get('ticks_data', [])
      deals_data = body.get('deals_data', [])

    # Нихрена не пашет
    #from django.core import management
    #management.call_command('test_plotly', image=True)

    return JsonResponse(result, safe=False)
