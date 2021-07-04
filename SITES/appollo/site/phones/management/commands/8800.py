#-*- coding:utf-8 -*-
import re
import time
import json
import logging
import datetime
import requests

import html
from lxml import html as lxml_html

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.main_functions.string_parser import kill_html, translit
from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.catcher import json_pretty_print

from apps.site.phones.models import Phones

logger = logging.getLogger(__name__)

default_folder = settings.MEDIA_ROOT

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--demo_mode',
            action = 'store_true',
            dest = 'demo_mode',
            default = False,
            help = 'Set demo mode')
        parser.add_argument('--cat_id',
            action = 'store',
            dest = 'cat_id',
            type = str,
            default = False,
            help = 'Set cat tag for update')

    def handle(self, *args, **options):
        started = time.time()
        hotlines = HotlinesTop()

        menus = hotlines.fetch_mapa()
        for menu in menus:
            companies = []
            for i in range(1, 100):
                result = hotlines.fetch_rubric_page(rubric=menu, page=i)
                #print(json_pretty_print(result))
                if not result:
                    break
                companies += result

            for company in companies:
                hotlines.fetch_company_page(company)


class HotlinesTop(object):
    def __init__(self):
        self.domain = 'https://hotlines.top'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent, 'X-Requested-With': 'XMLHttpRequest'}
        tag = 'phones8800'
        # Создаем/находим каталог
        container = Containers.objects.filter(
            tag=tag,
            state=1).first()
        if not container:
            container = Containers.objects.create(
                tag=tag, state=1,
                name='Категории 8800',
            )
        self.container = container

    def fetch_mapa(self):
        """Получить ссылки на разделы"""
        content = None
        while not content:
            try:
                r = requests.get(self.domain, headers=self.headers)
                content = r.text
            except Exception as e:
                logger.info('[ERROR]: %s' % e)

        tree = lxml_html.fromstring(content)
        box = tree.xpath('//div[@id="categories-2"]')[0]
        ahrefs = box.xpath('.//ul/li/a')
        result = [{
            'href': link.attrib.get('href'),
            'name': link.text,
        } for link in ahrefs]
        for menu in result:
            name = menu['name'].strip()
            link = '/phones/%s/' % translit(name)
            analog = Blocks.objects.filter(container=self.container, name=name).first()
            if not analog:
                analog = Blocks.objects.create(container=self.container, name=name, link=link, state=4)
            menu['block'] = analog

        return result


    def fetch_rubric_page(self, rubric: dict = None, page: int = 1):
        """Получить страничку рубрики
           :param rubric: Рубрика (словарь со ссылкой и названием)
           :param page: номер страницы
        """
        if not rubric:
            rubric = {
                'href': 'https://hotlines.top/aviakompanii/',
                'name': 'Авиакомпании',
            }
        content = None
        rubric_href = rubric['href']
        if page != 1:
            rubric_href = '%s/page/%s/' % (rubric['href'].rstrip('/'), page)
        print(rubric_href)
        while not content:
            try:
                r = requests.get(rubric_href, headers=self.headers)
                content = r.text
            except Exception as e:
                logger.info('[ERROR]: %s' % e)
        companies = []
        tree = lxml_html.fromstring(content)
        box = tree.xpath('//div[@id="main-content"]')[0]
        articles = box.xpath('.//article')
        for article in articles:
            company = article.xpath('.//h3/a')[0]
            imga = article.xpath('.//img')[0]
            companies.append({
                'href': company.attrib.get('href'),
                'name': company.text,
                'img': imga.attrib.get('src'),
                'info': [],
                'rubric': rubric,
            })
        return companies


    def fetch_company_page(self, company: dict = None):
        """Получить страничку компании
           :param company: Компания (словарь со ссылкой и названием)
        """
        if not company:
            company = {
                'href': 'https://hotlines.top/goryachaya-liniya-airbaltic/',
                'name': 'Горячая линия airBaltic',
                'img': 'https://hotlines.top/wp-content/uploads/2018/06/airBaltic2.jpg',
                'info': [],
            }
        content = None
        print(company['href'])
        while not content:
            try:
                r = requests.get(company['href'], headers=self.headers)
                content = r.text
            except Exception as e:
                logger.info('[ERROR]: %s' % e)
        companies = []
        tree = lxml_html.fromstring(content)
        box = tree.xpath('//div[@id="main-content"]')[0]
        article = box.xpath('.//article')[0]
        articles = article.xpath('.//p')
        for par in articles:
            if par.attrib.get('class') == 'tel':
                phones = par.xpath('.//a')
                for phone in phones:
                    number = phone.attrib.get('href').replace('tel:+7', '8')
                    if number.startswith('8800') or not 'phone' in company:
                        company['phone'] = number
            if not par.text:
                continue
            company['info'].append('<p>%s</p>' % par.text)
        articles = article.xpath('.//ul/li')

        lis = []
        for li in articles:
            if not li.text:
                continue
            text = li.text
            hrefs = li.xpath('.//a')
            for href in hrefs:
                text += '<a href="%s" target="_blank" rel="nofollow">%s</a><br>' % (href.attrib.get('href'), href.text)
            lis.append('<li>%s</li>' % text)
        if lis:
            company['info'].append('<ul>%s</ul>' % (''.join(lis), ))

        code = company['href'].replace(self.domain, '').replace('/', '')
        analog = Phones.objects.filter(code=code).first()
        if not analog:
            analog = Phones(code=code)
        analog.phone = company.get('phone')
        if not analog.phone:
            print('--- empty phone %s ---' % company['href'])
        analog.name = company['name']
        analog.info1 = '<br>'.join(company['info'])
        if 'rubric' in company:
            rubric = company['rubric']
            if 'block' in rubric:
                analog.menu = rubric['block']
        analog.save()
        if not analog.img:
            analog.upload_img(company['img'])

        return company
