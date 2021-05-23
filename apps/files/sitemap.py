# -*- coding:utf-8 -*-
import datetime

from django.conf import settings
from django.shortcuts import render

from apps.main_functions.functions import object_fields, recursive_fill, sort_voca

from apps.flatcontent.models import Containers, Blocks
from apps.flatcontent.views import SearchLink, CUR_APP

if settings.IS_DOMAINS:
    from apps.languages.models import (
        get_domain,
        get_domains,
        get_translate,
        translate_rows, )

class SitemapXML:
    """Класс для работы с картой сайта xml"""
    def __init__(self,
                 domain: dict = None,
                 scheme: str = 'https://'):
        """Инициализация
           :parm domain: Домен для карты сайта
           :param scheme: http/https
        """
        if not domain:
            self.domain_site = settings.MAIN_DOMAIN or 'masterme.ru'
        else:
            self.domain_site = domain.get('domain')
        self.domain_site = '%s%s' % (scheme, self.domain_site)

    def get_menu_managers(self):
        """Получаем все менеджеры меню
           с кол-вом ссылок
        """
        managers = {
            'menus': {'state': 1}, # flatmenu
            #'products': {'state': 4}, # flatprices
            #'cats': {'state': 7}, # flatcat
        }
        if 'apps.products' in settings.INSTALLED_APPS:
            managers.update({
                'products': {'state': 4}, # flatprices
                'cats': {'state': 7}, # flatcat
            })

        now = datetime.datetime.now()
        lastmod = datetime.datetime.strftime(now, '%Y-%m-%dT%H:%M:%SZ')

        for key, manager in managers.items():
            manager['containers'] = list(Containers.objects.filter(state=manager['state']).values_list('id', flat=True))
            manager['lastmod'] = lastmod
            manager['loc'] = '%s/sitemap/%s.xml' % (self.domain_site, key)
        return managers

    def get_manager(self, link):
        """Формирование ссылок для карты сайта
           по ссылке с определением менеджера меню
           :param link: ссылка из индекса карты сайта,
                        например, /sitemap/menus.xml
        """
        managers = self.get_menu_managers()
        for key, manager in managers.items():
            if '%s.xml' % key in link:
                return self.get_links(managers[key])
        return self.get_links(managers['menus'])

    def get_links(self, manager: dict):
        """Формирование ссылок для карты сайта
           по всем менюшкам
           :param manager: менеджер меню
        """
        blocks = Blocks.objects.filter(container__in=manager['containers']).values('updated', 'link')
        manager['blocks'] = []
        for block in blocks:
            manager['blocks'].append({
                'lastmod': block['updated'].strftime('%Y-%m-%d'),
                'loc': '%s%s' % (self.domain_site, block['link']),
            })
        return manager['blocks']

class SitemapHTML(SitemapXML):
    """Класс для работы с картой сайта html"""

    def show_sitemap(self, request):
        """Формирование ссылок для карты сайта
           :param request: HttpRequest
           TODO: постраничная навигация
           TODO: выполнять кроном и ложить в кэш/файл
        """
        managers = self.get_menu_managers()

        context = {}
        q_string = {}
        containers = {}

        # для перевода
        all_containers = []
        all_blocks = []

        for key, manager in managers.items():
            query = Blocks.objects.filter(container__in=manager['containers']).order_by('position')
            manager['structure'] = []
            for container in manager['containers']:
                menus = []
                blocks = [block for block in query if block.container_id == container]

                recursive_fill(blocks, menus, parents='')
                sort_voca(menus)
                container = Containers.objects.filter(pk=container).first()
                all_containers.append(container)
                all_blocks += blocks
                manager['structure'].append({
                    'container': container,
                    'blocks': menus
                })

        # Переводим блоки/контейнеры
        if settings.IS_DOMAINS and request:
            domains = get_domains()
            domain = get_domain(request, domains)
            if domain:
                domains = [domain]
                get_translate(all_blocks, domains)
                translate_rows(all_blocks, domain)
                get_translate(all_containers, domains)
                translate_rows(all_containers, domain)

        context['managers'] = managers
        page = SearchLink(q_string, request, containers)
        if not page:
            page = Blocks(name='Карта сайта')
        context['breadcrumbs'] = [{
            'name': page.name,
            'link': '/sitemap/',
        }]
        context['page'] = page
        context['containers'] = containers
        template = 'sitemap_html.html'
        return render(request, template, context)

