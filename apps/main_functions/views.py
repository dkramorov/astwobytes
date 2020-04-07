# -*- coding:utf-8 -*-
import json
import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

from apps.flatcontent.views import SearchLink
from apps.main_functions.catcher import feedback_form, json_pretty_print

logger = logging.getLogger('main')

def my_ip(request):
    """Апи-метод для получения ip-адреса"""
    result = {
        'ip': request.META.get('REMOTE_ADDR'),
        'ip_forwarded': request.META.get('HTTP_X_FORWARDED_FOR'),
    }
    return JsonResponse(result, safe=False)

def DefaultFeedback(request, **kwargs):
    """Контакты и форма обратной связи
       kwargs['fv']:
       fv => array дополнительной информации для письма
       ------------------------------------------------
       Любое количество полей с его описанием принимаем
       из main.views.FeedBack
       kwargs['fields'] = [{"name":"value"}, ...]
       name - название input/select...
       value - описание что за поле
       соответственно, вытаскиваем из POST по name и
       описание будет value:request.POST['name']
       -------------------------------------------------
       kwargs['additional_emails'] = True =>
       принимаем request.POST.get("additional_emails)
       kwargs['additional_emails_condition'] = "223.ru"
       => условие - в email должно быть это выражение
       -------------------------------------------------
       kwargs['additional_conds'] - доп. валидация
       kwargs['additional_conds'] = [
         {"name":"sms", "error":u"Неправильный смс-код", "value":"1234"},
         ..., ]"""
    q_string = kwargs.get('q_string', {})
    breadcrumbs = kwargs.get('breadcrumbs', [])
    result = {'errors': []}
    # -----------------------------------
    # Принудительная попытка отправки,
    # даже если не все гладко - например,
    # не все поля заполнены
    # -----------------------------------
    force_send = kwargs.get('force_send') == True
    do_not_send = kwargs.get('do_not_send') == True

    isError = None
    if not breadcrumbs:
        breadcrumbs.append({'name': 'Обратная связь', 'link': '/feedback/'})
    # ---
    # GET
    # ---
    if request.method == "GET":
        product = kwargs.get('product')
        q_string['recall'] = kwargs.get('recall')
        containers = {}
        context = {}
        template = kwargs.get('template', 'web/main_stat.html')
        page = SearchLink(q_string, request, containers)
        context['page'] = page
        context['q_string'] = q_string
        context['breadcrumbs'] = breadcrumbs
        context['containers'] = containers
        context['product'] = product
        return render(request, template, context)
    # ----
    # POST
    # -------------------
    # Дополнительные поля
    # -------------------
    fields = kwargs.get('fields', [])

    feedback_vars = feedback_form(request, q_string, fields=fields)
    for required_key in ('name', 'phone', 'msg'):
        if not required_key in feedback_vars:
            result['error'] = required_key
            isError = 1

    # ------------------------------------
    # Принудительная отправка даже
    # при незаполненных обязательных полях
    # ------------------------------------
    if force_send:
        isError = None
        if 'error' in result:
            del result['error']

    # ------------------------
    # Проверка по доп условиям
    # ------------------------
    additional_conds = kwargs.get('additional_conds', [])
    for acond in additional_conds:
        v = request.POST.get(acond['name'])
        if not v == acond['value']:
            result['errors'].append(acond['error'])
            result['error'] = acond['name']
            isError = 1

    if not isError:
        result['success'] = 1
        title = kwargs.get('title')
        if title:
            feedback_vars['title'] = title

        fv = kwargs.get('fv', [])
        for item in fv:
            feedback_vars['result'] += item

        mail = EmailMessage(feedback_vars['title'], feedback_vars['result'], feedback_vars['sender'], feedback_vars['emails'])
        mail.content_subtype = 'html'
        if feedback_vars['file']:
            mail.attach(feedback_vars['file']['name'], feedback_vars['file']['content'], feedback_vars['file']['content_type'])
        if not do_not_send:
            mail.send()
        else:
            logger.info(json_pretty_print(feedback_vars))
    # ---------------------------
    # Не возвращаем  HttpResponse
    # ---------------------------
    if kwargs.get('dummy'):
        return {'feedback_vars': feedback_vars, 'result': result}

    return JsonResponse(result, safe=False)
