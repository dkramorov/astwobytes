# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from apps.main_functions.functions import recursive_fill, sort_voca
from apps.flatcontent.models import Containers, Blocks, get_ftype

register = template.Library()

# -----------------------
# Если мультиязычный сайт
# -----------------------
if settings.IS_DOMAINS:
    from apps.languages.models import (
        get_domain,
        get_domains,
        get_translate,
        get_content_type,
        translate_rows, )

@register.inclusion_tag('web/flat_menu.html')
def flatmenu(request, tag: str = None, containers: list = []):
    """Все виды меню в шаблоне
       :param tag: Тег контейнера меню
       :param containers: Контейнеры, которые нужно передать в шаблон"""
    result = {}
    all_blocks = [] # Для перевода
    if not tag:
        return result
    cache_time = 60 # 60 секунд
    cache_var = '%s_flatmenu_%s' % (settings.PROJECT_NAME, tag)
    if settings.IS_DOMAINS:
        domain = get_domain(request)
        if domain:
            cache_var += '_%s' % domain['pk']

    inCache = cache.get(cache_var)
    ignore_cache = request.GET.get('ignore_cache') or request.GET.get('force_new')
    if inCache and not ignore_cache:
        result = inCache
    else:
        search_blocks = Blocks.objects.filter(container__tag=tag, state=4, is_active=True, container__is_active=True)
        for item in search_blocks:
            all_blocks.append(item)
        menu_queryset = []
        recursive_fill(search_blocks, menu_queryset, '')
        menus = sort_voca(menu_queryset)

        # --------------------------
        # Переводим блоки/контейнеры
        # --------------------------
        if settings.IS_DOMAINS:
            domains = get_domains()
            domain = get_domain(request, domains)
            if domain:
                domains = [domain]
                get_translate(all_blocks, domains)
                translate_rows(all_blocks, domain)

        result['menus'] = menus
        cache.set(cache_var, result, cache_time)
    result['containers'] = containers
    result['request'] = request
    result['tag'] = tag
    return result

@register.inclusion_tag('web/flat_content.html')
def flatcontent(request,
                page: Blocks = None,
                tag: str = None,
                template_position: str = 'content'):
    """Вывод контента по шаблону из web папки сайта
       :param request: HttpRequest
       :param page: меню с линковками контейнеров
       :param tag: тег, который надо вывести из page
       :param template_position: позиция в шаблоне, куда выводим контент"""
    result = {}
    result['request'] = request
    if not page:
        return result

    result['page'] = page
    result['tag'] = tag

    if not hasattr(page, 'containers'):
        return result

    for container in page.containers:
        if not container:
            continue
        # --------------------------
        # Контент для всех страничек
        # --------------------------
        if 'container' in container:
            t = 'main'
            if not hasattr(container['container'], 'tag') or not container['container'].tag == t:
                continue
            if container['container'].tag == t:
                containers = {}
                containers[t] = {}
                containers[t]['tags'] = {}
                for block in container['blocks']:
                    if not hasattr(block, 'tag') or not block.tag:
                        continue
                    containers[t]['tags'][block.tag] = block
                result['containers'] = containers

    for item in page.containers:
        if not item:
            continue
        if not isinstance(item.get('container'), Containers):
            continue

        container = item['container']
        # ---------------------------------------
        # На страничке могут быть 2 контейнера
        # с одинаковыми тегами, в этом случае,
        # попробуем записать в контейнер, что он,
        # уже был показан
        # ---------------------------------------
        if hasattr(container, 'was_shown'):
            continue

        if not container.template_position:
            container.template_position = 'content'

        if not (container.tag == tag and container.template_position == template_position):
            continue

        container.was_shown = 1
        result['container'] = container
        result['blocks'] = item['blocks']
        result['products'] = item['products']

        # ---------------------------------
        # Проверяем наличие шаблона в
        # flatcontent/templates/containers/
        # TODO объединить в select_template
        # ---------------------------------
        #t = 'containers/%s.html' % tag
        #try:
        #    one_line = template.loader.select_template([t])
        #except template.TemplateDoesNotExist:
        #    one_line = None
        #if one_line:
        #    result['one_line'] = t
        #    return result

        # ---------------------------
        # Проверяем наличие шаблона в
        # templates/web/containers/
        # ---------------------------
        t = 'web/containers/%s.html' % tag
        try:
            one_line = template.loader.select_template([t])
        except template.TemplateDoesNotExist:
            one_line = None
        if one_line:
            result['one_line'] = t
        return result
    return result

