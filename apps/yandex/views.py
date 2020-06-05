# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect

from apps.main_functions.date_time import str_to_date
from .metrika import YandexMetrika

CUR_APP = 'yandex'
metrika_vars = {
    'singular_obj': 'Яндекс',
    'plural_obj': 'Яндекс',
    'rp_singular_obj': 'Яндекс',
    'rp_plural_obj': 'Яндекс',
    'template_prefix': 'yandex_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'yandex',
    'submenu': 'yandex',
}

def metrika(request):
    """Страничка для отчета по апи Яндекс.Метрики """
    context = {}
    context.update(metrika_vars)

    method = request.GET
    if request.method == 'POST':
        method = request.POST
    params = {}
    proxies = {}
    ip = method.get('ip')
    if ip:
        params['filters'] = '(ym:s:paramsLevel2=@\'%s\')' % ip
    dates = method.get('dates')
    date1 = None
    date2 = None
    if dates:
        dates_arr = dates.split(' - ')
        date1 = str_to_date(dates_arr[0])
        date2 = str_to_date(dates_arr[1])
    if date1:
        params['date1'] = date1.strftime('%Y-%m-%d')
    if date2:
        params['date2'] = date2.strftime('%Y-%m-%d')

    ym = YandexMetrika()
    if request.is_ajax():
        result = {}
        action = method.get('action')
        if action == 'bad_users':
            result = ym.get_bad_users(**params)
        elif action == 'weak_users':
            result = ym.get_weak_users(**params)
        elif action == 'robots':
            result = ym.get_robots(**params)

        return JsonResponse(result, safe=False)

    template = 'yandex_metrika.html'
    return render(request, template, context)

