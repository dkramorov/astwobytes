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

from apps.main_functions.string_parser import kill_html
from apps.flatcontent.models import Containers, Blocks
from apps.products.models import Products, Property, PropertiesValues, ProductsProperties, ProductsCats, ProductsPhotos
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file, make_folder
from apps.products.models import Products, ProductsPhotos, ProductsCats

logger = logging.getLogger(__name__)

default_folder = settings.MEDIA_ROOT
cookies = {
    'PHPSESSID': '4799930f2f5a1e71f3610f23f0b59c75',
    'cookie[valuta]': '0',
    'cookie[page_rows]': '10000',
    'cookie[city]': '29',
    'cookie[sort_cat_n]': '4',
    'cookie[stiso]': '1',
    'cookie[sort_direct]': '0',
    'cookie[only_cond]': '0',
    'cookie[only_active]': '0',
    'cookie[as_client]': '0',
    'cookie[all_whs]': '0',
    'cookie[is_selections_open]': '0',
    'ab': 'main',
    'cookie[jcid]': '0',
    'cookie[is_prop_open]': '0',
    'cookie[looked_str]': '54247',
    '_ga': 'GA1.2.1146821704.1598155929',
    '_gid': 'GA1.2.846886334.1598155929',
    '_ym_uid': '1598155929160341499',
    '_ym_d': '1598155929',
    '_ym_isad': '1',
}

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
        for prop in Property.objects.all():
            prop.delete()
        rp = RupoolPrices()
        elapsed = time.time() - started
        print('%.2f' % elapsed)

class RupoolPrices(object):
    def __init__(self):
        self.isError = None
        self.total_pages = 0
        self.domain = 'https://www.rupool.ru'
        self.bad_image = 'shablon_foto.jpg'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent, 'X-Requested-With': 'XMLHttpRequest'}
        # Создаем/находим каталог
        container = Containers.objects.filter(
            tag='catalogue',
            state=7).first()
        if not container:
            container = Containers.objects.create(
                tag='catalogue', state=7,
                name='Каталог',
            )
        self.container = container
        self.fetch_mapa() # Хаваем ссылки на рубрики

    def fetch_mapa(self):
        """Скачать карту сайта (все ссылки на рубрики)"""
        content = None
        link = '%s/map/' % self.domain
        while not content:
            try:
                r = requests.get(link, headers=self.headers)
                content = r.text
            except Exception as e:
                logger.info('[ERROR]: %s' % e)

        tree = lxml_html.fromstring(content)
        box = tree.xpath('//div[@id="page_in_bottom"]')[0]
        ahrefs = box.xpath('.//a[@class="list-group-item"]')
        self.fill_rubrics(ahrefs)

    def fill_rubrics(self, ahrefs):
        """Заполнить рубрики
           :param ahrefs: ссылки на рубрики
        """
        for ahref in ahrefs:
            href = ahref.attrib.get('href')
            name = ahref.text
            if not name:
                name = ahref.xpath('.//p')[0].text
            cat = self.fill_rubric(name, href)
            self.fill_products(cat)

    def fill_rubric(self, name: str, href: str, parents: str = None):
        """Заполнить рубрику
           :param name: Название рубрики
           :param href: ссылка на рубрику
           :param parents: родительские рубрики
           :return: cat
        """
        cat_id = int(href.split('/')[-1])
        tag = '_cat_%s' % cat_id
        cat = Blocks.objects.filter(
            container=self.container,
            state=4,
            tag=tag, ).first()
        if not cat:
            cat = Blocks(
                container=self.container,
                state=4,
                tag=tag, )
        if parents:
            cat.parents = parents
        cat.name = name
        cat.save()
        return cat

    def fill_products(self, cat):
        """Заполнение товарами по каталогу
           :param cat: рубрика каталога
        """
        cat_id = cat.tag.replace('_cat_', '')
        content = None
        link = '%s/catalog/%s' % (self.domain, cat_id)
        while not content:
            try:
                r = requests.get(link, headers=self.headers)
                content = r.text
            except Exception as e:
                logger.info('[ERROR]: %s' % e)
        tree = lxml_html.fromstring(content)

        breadcrumbs = tree.xpath('//ol[@class="breadcrumb"]')[0]
        ahrefs = breadcrumbs.xpath('.//a')
        parents = None
        for ahref in ahrefs:
            if ahref.attrib.get('itemprop'):
                name = ahref.xpath('.//span')[0].text
                href = ahref.attrib.get('href')
                parent_cat = self.fill_rubric(name, href, parents)
                parents = '%s_%s' % (parent_cat.parents or '', parent_cat.id)
        Blocks.objects.filter(pk=cat.id).update(parents=parents)

        s = requests.Session()
        s.cookies.update(cookies)
        link = '%s/lib/JsHttpRequest/this.php?JsHttpRequest=1' % self.domain
        data = {
            'id': cat_id,
            'action': 'goods_list',
            'page': 1,
            'func_before': 'GoodsListAfter',
        }
        resp = s.post(link, data=data).text
        # JsHttpRequest.dataReady( в начале и ) с нуль-байтом в конце
        resp = resp[24:-2]
        resp = json.loads(resp)
        #print(json_pretty_print(resp))
        table = lxml_html.fromstring(resp['js']['good_mess'])
        trs = table.xpath('.//tr[@class="tr_tovar"]')
        for tr in trs:
            self.fill_product(cat, tr)

    def fill_product(self, cat, tr):
        """Заполнить товар
           :param cat: категория товара
           :param tr: элемент таблицы с инфой о товаре
        """
        # Изображение
        search_img = tr.xpath('.//td[@class="td_img"]')[0]
        images = search_img.xpath('.//a[@class="highslide"]')
        photos = []
        for img in images:
            href = img.attrib.get('href')
            if not href:
                href = img.attrib.get('ps_href')
            photos.append(href)
        # Описание
        search_info = tr.xpath('.//td[@class="descr_short"]')[0]
        # Название товара, ссылка, ид
        search_name = search_info.xpath('.//h3/a')[0]
        product_name = search_name.text
        product_link = search_name.attrib.get('href')
        product_id = int(product_link.split('/')[-1])
        # Производитель
        manufacturer = None
        search_manufacturer = search_info.xpath('.//a[@class="brand"]')
        if search_manufacturer:
            manufacturer = search_manufacturer[0].text
        # Свойства
        props = []
        search_props = search_info.xpath('.//div[@id="good_short%s"]' % product_id)
        if search_props:
            # Тут также дополнительное описание
            props_arr = search_props[0].xpath('.//div[@class="div2"]')
            props = self.get_props_array(props_arr)

        # Цена/свойства
        print(product_id, product_name)
        search_price = tr.xpath('.//td[@class="right_block"]')[0]
        # Цены может не быть
        product_price = None
        price = search_price.xpath('.//span[@class="price_view"]')
        if price:
            price = price[0]
            product_price = price.text.split('руб')[0]
            product_price = product_price.replace(' ', '')
            product_price = float(product_price)

        analog = Products.objects.filter(code=product_id).first()
        if not analog:
            analog = Products(code=product_id)
        analog.name = product_name
        analog.price = product_price
        analog.save()

        self.update_props(analog, props)
        self.update_cat(analog, cat)

    def get_props_array(self, props_arr):
        """Найти свойства товара/услуги
           :param props_arr: элемент с возможными свойствами
        """
        if not props_arr:
            return []
        props = []
        props_arr = lxml_html.tostring(props_arr[0])
        props_arr = props_arr.decode()
        props_arr = html.unescape(props_arr)
        props_arr = props_arr.replace('<br/>', '<br>')
        props_arr = props_arr.replace('<br />', '<br>')
        props_arr = props_arr.replace('<div class="div2">', '')
        props_arr = props_arr.replace('</div>', '')
        props_arr = props_arr.split('<br>')
        for prop in props_arr:
            if 'Подходящие модели' in prop:
                continue
            prop_name = prop.split('<span>')[0]
            prop_value = prop.split('</span>')[0]
            prop_value = prop_value.split('<span>')[1]
            prop_measure =  prop.split('</span>')[1]
            props.append({
                'name': prop_name.replace(':', '').strip(),
                'value': prop_value.strip(),
                'measure': prop_measure.strip(),
            })
        return props

    def update_cat(self, product, cat):
        """Привязка рубрики
           :param product: товар/услуга
           :param cat: рубрика
        """
        if not cat:
            return
        cat_link = ProductsCats.objects.filter(
            product=product,
            cat=cat,
            container = self.container, ).values_list('id', flat=True)
        if not cat_link:
            cat_link = ProductsCats.objects.create(
                product=product,
                cat=cat,
                container=self.container, )

    def update_props(self, product, props):
        """Обновление свойств товара
           :param product: товар/услуга
           :param props: массив со словарями свойств
        """
        #print(props)
        for item in props:
            prop_name = item['name']
            prop_value = item['value']
            if len(prop_value) > 50:
                continue
            prop = Property.objects.filter(name=prop_name).first()
            if not prop:
                measure = item['measure']
                prop = Property.objects.create(
                    name=prop_name,
                    measure=measure, )
            pvalue = PropertiesValues.objects.filter(
                prop=prop,
                str_value=prop_value, ).first()
            if not pvalue:
                pvalue = PropertiesValues.objects.create(
                    prop=prop,
                    str_value=prop_value, )
            product_prop = ProductsProperties.objects.filter(
                product=product,
                prop=pvalue, ).first()
            if not product_prop:
                product_prop = ProductsProperties.objects.create(
                    product=product,
                    prop=pvalue, )

