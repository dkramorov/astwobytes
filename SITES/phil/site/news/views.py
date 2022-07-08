# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings

from django.template.loader import render_to_string
from django.db.models import Count, Q
from apps.main_functions.model_helper import ModelHelper

from apps.flatcontent.models import Containers, Blocks, LinkContainer

from apps.flatcontent.views import SearchLink

if settings.IS_DOMAINS:
    from apps.languages.models import (
        get_domain,
        get_domains,
        get_translate,
        get_content_type,
        translate_rows, )

CUR_APP = 'main'
news_vars = {
    'singular_obj': 'Блог',
    'plural_obj': 'Блоги',
    'template_prefix': 'news_',
    'show_urla': 'news',
}

def show_news(request, link: str = None, sublink: str = None):
    """Вывод новостей / блога
       :param request: HttpRequest
       :param link: ссылка из менюшки новостей
       :param sublink: дополнительная часть ссылки на ссылку в новость
    """
    news_prefix = '/news/'
    mh_vars = news_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    mh_vars = news_vars.copy()
    mh = ModelHelper(Containers, request=request, cur_app=CUR_APP)
    mh.q_string['by'] = 6
    mh.paginator_template = 'web/paginator.html'
    mh.filter_add(Q(state=5))
    mh.filter_add(Q(is_active=True))

    page = SearchLink(q_string, request, containers)
    if not page:
        page = Blocks(name=news_vars['singular_obj'])

    context['breadcrumbs'] = []
    news_menus = Blocks.objects.filter(container__tag='newsmenu', state=4, parents='')
    if link:
        main_link = Blocks.objects.filter(state=4, container__tag='mainmenu', link='/news/').first()
        if main_link:
            context['breadcrumbs'].append({
                'name': main_link.name,
                'link': main_link.link,
            })

        news_menus = news_menus.filter(link__startswith='%s%s/' % (news_prefix, link))
        # Находим привязки, которые будем выводить
        if news_menus:
            parents = ['%s_%s' % (item.parents, item.id) for item in news_menus]
            ids_containers = list(LinkContainer.objects.filter(block__parents__in=parents).values_list('container', flat=True))
            mh.filter_add(Q(pk__in=ids_containers))

            # Детальная страничка новости
            if sublink:
                context['breadcrumbs'].append({
                    'name': news_menus[0].name,
                    'link': news_menus[0].link,
                })

    context['breadcrumbs'].append({
        'name': page.name,
        'link': reverse('%s:%s' % (CUR_APP, 'news')),
    })

    context['page'] = page
    context['containers'] = containers
    template = 'web/news/show_news.html'

    rows = mh.standard_show()
    # Получение ссылок в контейнеры
    ids_rows = {row.id: row for row in rows}
    links = LinkContainer.objects.filter(container__in=ids_rows.keys()).values('container', 'block__link')
    for item in links:
        if item['container'] in ids_rows:
            ids_rows[item['container']].link = item['block__link']

    context['news'] = rows
    context['paginator'] = mh.paginator
    context['raw_paginator'] = mh.raw_paginator

    if settings.IS_DOMAINS:
        domains = get_domains()
        domain = get_domain(request, domains)
        if domain:
            domains = [domain]
            get_translate(rows, domains)
            translate_rows(rows, domain)

    if request.is_ajax():
        next_page = -1
        if mh.raw_paginator.get('next_page') != mh.raw_paginator.get('cur_page'):
            next_page = mh.raw_paginator['next_page']
        context = {
            'result': render_to_string('web/news/news_grid.html', context),
            'next_page': next_page,
        }
        return JsonResponse(context, safe=False)

    return render(request, template, context)
