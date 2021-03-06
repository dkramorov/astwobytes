# -*- coding:utf-8 -*-
import json
import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

from apps.flatcontent.views import SearchLink
from apps.main_functions.catcher import feedback_form, json_pretty_print
from apps.main_functions.models import Tasks, Config
from apps.main_functions.model_helper import get_user_permissions

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

logger = logging.getLogger('main')

CUR_APP = 'main_functions'

main_vars = {
    'singular_obj': 'Задача',
    'plural_obj': 'Задачи',
    'rp_singular_obj': 'задачи',
    'rp_plural_obj': 'задач',
    'template_prefix': 'main_functions_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'main_functions',
    'submenu': 'tasks',
    'show_urla': 'show_tasks',
    'create_urla': 'create_task',
    'edit_urla': 'edit_task',
    'model': Tasks,
}

@login_required
def show_tasks(request, *args, **kwargs):
    """Вывод задач"""
    return show_view(request,
                     model_vars = main_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_task(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование задачи"""
    mh_vars = main_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
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

    elif request.method == 'POST':
        pass_fields = ()
        mh.post_vars(pass_fields=pass_fields)

        if action == 'create' or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    if not mh.row.id:
                        context['error'] = 'Ошибка при сохранении, возможно, дубль'
                    else:
                        context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
        # -------------------------------------------
        # Нужно обновить ссылку на файл, если ее нету
        # Если есть файл, нужно обновить mimetype
        # -------------------------------------------
        elif action == 'img' and request.FILES:
            mh.uploads()

    if mh.row and mh.row.id:
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.get_url_edit()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@csrf_exempt
def my_ip(request):
    """Апи-метод для получения ip-адреса"""
    method = request.GET if request.method == 'GET' else request.POST
    result = {
        'method': request.method,
        'ip': request.META.get('REMOTE_ADDR'),
        'ip_forwarded': request.META.get('HTTP_X_FORWARDED_FOR'),
    }
    # на случай, если надо посмотреть тело json запроса
    if hasattr(request, 'body') and request.body:
        logger.info(json_pretty_print(json.loads(request.body)))
    return JsonResponse(result, safe=False)

@csrf_exempt
def test_statuses(request):
    """Апи-метод для тестирования ответов"""
    status_code = request.GET.get('status_code')
    if not status_code:
        status_code = 400
    status_code = int(status_code)
    result = {
        'status': status_code,
        'msg': 'test_statuses',
    }
    return JsonResponse(result, safe=False, status=status_code)

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
         ..., ]
    """
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
        breadcrumbs.append({
            'name': 'Обратная связь',
            'link': '/feedback/',
        })
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

        logger.info('\n[--- SENDING EMAIL ---]' +
                    '\n[TITLE]:%s' % feedback_vars['title'] +
                    '\n[MSG]: %s' % feedback_vars['result'] +
                    '\n[SENDER]: %s' % feedback_vars['sender'] +
                    '\n[EMAILS]: %s' % feedback_vars['emails'] +
                    '\n[---------------------]')

        mail = EmailMessage(feedback_vars['title'], feedback_vars['result'], feedback_vars['sender'], feedback_vars['emails'])
        mail.content_subtype = 'html'
        if feedback_vars['file']:
            mail.attach(feedback_vars['file']['name'], feedback_vars['file']['content'], feedback_vars['file']['content_type'])
        if not do_not_send:
            try:
                mail.send()
            except Exception as e:
                result['error'] = str(e)
        else:
            logger.info(json_pretty_print(feedback_vars))
    # ---------------------------
    # Не возвращаем  HttpResponse
    # ---------------------------
    if kwargs.get('dummy'):
        return {'feedback_vars': feedback_vars, 'result': result}

    return JsonResponse(result, safe=False)

@login_required
def settings(request, app: str = 'flatcontent'):
    """Настройки для разделов
       :param app: приложение
    """
    result = {}
    app_label = '%s_' % app
    permissions = get_user_permissions(request.user, Config)
    # настройки могут быть зависимы или независимы от пользователя
    # 'user_defined': False, # Не зависят от пользователя
    # 'user_defined': True, # Зависят от пользователя
    settings_store = {
        'flatcontent': {
            'singular_obj': 'Раздел "Контент" и стат. странички',
            'rp_singular_obj': 'раздела "Контент" и стат. страничек',
            'name': 'Настройки раздела "Контент" и стат. страничек',
            'user_defined': False,
        },
        'spamcha': {
            'singular_obj': 'Раздел "Почта"',
            'rp_singular_obj': 'раздела "Почта"',
            'name': 'Настройки почты',
            'user_defined': True,
        },
        'languages': {
            'singular_obj': 'Раздел "Мультидомен"',
            'rp_singular_obj': 'раздела "Мультидомен"',
            'name': 'Настройки раздела "Мультидомен"',
            'user_defined': True,
        },
    }
    name = settings_store[app]['name']
    user_defined = settings_store[app]['user_defined']
    root_url = reverse('main_functions:settings', args=[app])
    context = {
         'app': app,
         'title': name,
         'singular_obj': settings_store[app]['singular_obj'],
         'rp_singular_obj': settings_store[app]['rp_singular_obj'],
         'user_defined': user_defined,
         'breadcrumbs': [{
             'name': name,
             'link': root_url,
         }],
         'menu': main_vars['menu'],
         'submenu': app,
    }
    template = '%s_settings.html' % (app, )
    if request.method == 'POST':
        settings = []
        settings_count = request.POST.get('settings', 0)
        try:
            settings_count = int(settings_count)
        except ValueError:
            settings_count = 0
        for i in range(settings_count):
            settings.append({
                'name': request.POST.get('name_%s' % i),
                'attr': request.POST.get('attr_%s' % i),
                'value': request.POST.get('value_%s' % i),
            })
        if permissions['edit'] or user_defined:
            configs = Config.objects.filter(attr__startswith=app_label)
            if user_defined:
                configs = configs.filter(user=request.user)
            configs.delete()
            for setting in settings:
                if not setting['attr']:
                    continue
                if not setting['attr'].startswith(app_label):
                    setting['attr'] = '%s%s' % (app_label, setting['attr'])
                analog = Config(attr=setting['attr'])
                analog.name = setting['name']
                analog.value = setting['value']
                if user_defined:
                    analog.user = request.user
                analog.save()
            result['success'] = 'Данные успешно сохранены'
        else:
            result['error'] = 'Недостаточно прав'
        return JsonResponse(result, safe=False)

    configs = Config.objects.filter(attr__startswith='%s_' % app)
    if user_defined:
        configs = configs.filter(user=request.user)
    context['rows'] = configs
    for row in context['rows']:
        if row.attr and row.attr.startswith(app):
            row.attr = row.attr.split(app_label, 1)[1]
    return render(request, template, context)
