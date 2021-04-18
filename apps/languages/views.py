# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, get_user_permissions
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from apps.languages.models import Translate, UITranslate, get_domains, get_domain

CUR_APP = 'languages'
languages_vars = {
    'singular_obj': 'Перевод',
    'plural_obj': 'Переводы',
    'rp_singular_obj': 'перевода',
    'rp_plural_obj': 'переводов',
    'template_prefix': 'languages_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'languages',
    'submenu': 'lanuages',
    'show_urla': 'show_translates',
    'create_urla': 'create_translate',
    'edit_urla': 'edit_translate',
    'model': Translate,
}

def get_referer_path(request):
    """Получение ссылки без домена от реферера
       :param request: HttpRequest"""
    referer = request.META.get('HTTP_REFERER')
    if not referer or 'languages/pick' in referer:
        return '/'
    referer = referer.replace('http://', '')
    referer = referer.replace('https://', '')
    referer = referer.replace('www.', '')
    referer = referer.replace(request.META.get('HTTP_HOST', ''), '')
    return referer

def pick_language(request, lang):
    """Переключение языка
       :param request: HttpRequest
       :param lang: язык (домен) на который переключаемся"""
    schema = 'https://' if request.is_secure() else 'http://'
    referer = get_referer_path(request)
    domains = get_domains()
    for domain in domains:
        if domain['domain'].startswith("%s." % lang):
            request.session['lang'] = lang
            #if settings.DEBUG:
            #    return redirect(referer)
            # Если домен совпадает с доменом по умолчанию,
            # тогда переадресацию делаюм на MAIN_DOMAIN
            dest = '%s%s%s' % (schema, domain['domain'], referer)
            if settings.DEFAULT_DOMAIN == lang:
                dest = '%s%s%s' % (schema, settings.MAIN_DOMAIN, referer)
            return redirect(dest)

    # Если домен не нашелся, удаляем
    try:
        del request.session['lang']
    except Exception:
        pass

    return redirect(referer)

def api(request, action: str = 'languages'):
    """Апи-метод для получения всех данных"""
    #if action == 'languages':
    #    result = ApiHelper(request, languages_vars, CUR_APP)
    result = ApiHelper(request, languages_vars, CUR_APP)
    return result

@login_required
def show_translates(request, *args, **kwargs):
    """Вывод переводов"""
    return show_view(request,
                     model_vars = languages_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_translate(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование перевода"""
    return edit_view(request,
                     model_vars = languages_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def translates_positions(request, *args, **kwargs):
    """Изменение позиций переводов"""
    result = {}
    mh_vars = languages_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

@login_required
def select_language(request, lang: str = None):
    """Выбор языка для заполнения в админке
       Также правильно было бы и язык самой админки переключать
    """
    result = {}
    mh_vars = languages_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'settings')
    context = mh.context

    if lang:
        request.session['lang'] = lang

    context['domains'] = get_domains()
    template = '%sselect_lang.html' % mh.template_prefix
    return render(request, template, context)

@login_required
def translate_mode(request, *args, **kwargs):
    """Перевод текстов админки"""
    result = {}
    domain = get_domain(request)
    perms = get_user_permissions(request.user, UITranslate)
    if not perms['edit']:
        result['error'] = 'Недостаточно прав'
    elif not domain:
        result['error'] = 'Не выбран домен'
    else:
        domain_pk = domain.get('pk')
        class_name = request.POST.get('pk')
        value = request.POST.get('value', '')[:254]
        analog = UITranslate.objects.filter(class_name=class_name, domain_pk=domain_pk).first()
        if not analog:
            analog = UITranslate(class_name=class_name, domain_pk=domain_pk)
        analog.value = value.strip()
        analog.save()
        result['translate'] = object_fields(analog)

    result['domain'] = domain
    return JsonResponse(result, safe=False)


def get_translations(request, *args, **kwargs):
    """Получение переводов"""
    result = {'translations': []}
    domain = get_domain(request)
    domain_pk = domain.get('pk')
    class_names = []
    for class_name in request.POST.get('class_names', '').split(','):
        class_name = class_name.strip()
        if class_name:
            class_names.append(class_name)
    if class_names:
        translations = UITranslate.objects.filter(class_name__in=class_names, domain_pk=domain_pk).values('class_name', 'value')
        result['translations'] = list(translations)
    result['class_names'] = class_names
    result['domain'] = domain
    return JsonResponse(result, safe=False)
