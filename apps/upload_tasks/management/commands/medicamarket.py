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

from apps.main_functions.string_parser import kill_html, kill_quotes
from apps.flatcontent.models import Containers, Blocks
from apps.products.models import Products, Property, PropertiesValues, ProductsProperties, ProductsCats, ProductsPhotos
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file, make_folder

logger = logging.getLogger(__name__)

default_folder = settings.MEDIA_ROOT

def clear_tables():
    """Очистка таблиц"""
    for prop in Property.objects.all():
        prop.delete()
    #Products.objects.all().update(img=None)
    ProductsPhotos.objects.all().delete()
    Products.objects.all().delete()

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
        #clear_tables()
        medica = MedicaMarket()
        ids_cats = medica.fetch_catalogue()
        for cat in ids_cats:
            products = []
            medica.fetch_products(products, cat)
            for product in products:
                medica.fetch_product(product)

class MedicaMarket(object):
    def __init__(self):
        self.domain = 'https://medicamarket.ru/'
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

    def fill_product_props(self, props, product):
        """Заполняем свойства"""
        for item in props:
            td_name = item[0]
            td_value = item[1]
            if not td_name.tag == 'td' or not td_value.tag == 'td':
                logger.info('[ERROR]: wrong el %s, %s' % (td_name.tag, td_value.tag))
                continue
            prop_name = td_name.text
            if len(td_name) > 0:
                prop_name = ' '.join([child.text for child in td_name if child.text])
            prop = Property.objects.filter(name=prop_name).first()
            if not prop:
                prop = Property.objects.create(name=prop_name)
            prop_value = td_value.text
            if len(td_value) > 0:
                prop_value = ' '.join([child.text for child in td_value if child.text])
            value = PropertiesValues.objects.filter(prop=prop, str_value=prop_value).first()
            if not value:
                value = PropertiesValues.objects.create(prop=prop, str_value=prop_value)
            analog = ProductsProperties.objects.filter(product=product, prop=value).first()
            if not analog:
                ProductsProperties.objects.create(product=product, prop=value)

    def fill_product_photos(self, photos, product):
        """Заполнение фоток к товару"""
        analogs = ProductsPhotos.objects.filter(product=product)
        if analogs:
            return

        for photo in photos:
            path = photo.attrib.get('href')
            if not product.img:
                product.upload_img('%s%s' % (self.domain.rstrip('/'), path))
            else:
                new_photo = ProductsPhotos.objects.create(product=product)
                new_photo.upload_img('%s%s' % (self.domain.rstrip('/'), path))

    def fetch_product(self, data: dict):
        """Получение полной информации о товаре
           :param data: словарь с данными по товару
        """
        pass_fields = ('cat', 'code')
        params = {k: v for k, v in data.items() if not k in pass_fields}
        product = Products.objects.filter(code=data['code']).first()
        if not product:
            product = Products.objects.create(code=data['code'])
        # Линковка к рубрике
        cat_link = ProductsCats.objects.filter(product=product, cat=data['cat'])
        if not cat_link:
            ProductsCats.objects.create(product=product, cat=data['cat'])

        urla = '%scshow.php?id_goods=%s' % (self.domain, data['code'])
        logger.info(urla)
        r = requests.get(urla)
        content = r.text
        tree = lxml_html.fromstring(content)
        box = tree.xpath('//td[@id="mainblock"]')[0]
        name = box.xpath('.//h1')[0].text
        info = []
        desc = box.xpath('.//span[@id="contctype0"]')
        if desc:
            desc = desc[0].xpath('.//td[@class="news"]')[0]
            info = [lxml_html.tostring(child, encoding=str) for child in desc]

        params.update({
            'name': name,
            'info': ''.join(info),
        })
        Products.objects.filter(pk=product.id).update(**params)

        props_span = box.xpath('.//span[@id="contctype10"]')
        if props_span:
            props_table = props_span[0].xpath('.//table[@class="price"]')
            if props_table:
                trs = props_table[0].xpath('.//tr')
                self.fill_product_props(trs, product)
        photos_div = tree.xpath('//div[@id="slidingProduct%s"]' % product.code)
        if photos_div:
            photos = photos_div[0].xpath('.//a')
            self.fill_product_photos(photos, product)

    def fetch_products(self, products: list, tag: str, page: int = 0):
        """Получение ид+цен товаров по категории

           Пагинация товаров идет с нуля, например,
           https://medicamarket.ru/catalog.php?idg=26&Page=1
           это уже вторая страничка,
           страничка будет пустой, если пагинация закончилась

           :param products: аккумулированный результат выполнения
           :param tag: tag категории в нашем каталоге
           :param page: страничка для постраничной навигации
        """
        while True:
            result = self.fetch_products_page(tag, page)
            if not result:
                break
            products += result
            page += 1

    def fetch_products_page(self, tag: str, page: int = 0):
        """Получение ид+цен товаров по категории
           по конкретной страничке

           Пагинация товаров идет с нуля, например,
           https://medicamarket.ru/catalog.php?idg=26&Page=1
           это уже вторая страничка,
           страничка будет пустой, если пагинация закончилась

           :param tag: tag категории в нашем каталоге
           :param page: страничка для постраничной навигации
        """
        products = []
        cat = Blocks.objects.filter(tag=tag, container=self.container).first()
        if not cat:
            logger.info('[ERROR]: CAT NOT FOUND %s' % tag)
            return
        urla = '%scatalog.php?idg=%s&Page=%s' % (
            self.domain,
            cat.tag.replace('cat_', ''),
            page,
        )
        logger.info(urla)
        r = requests.get(urla)
        content = r.text
        tree = lxml_html.fromstring(content)
        box = tree.xpath('//td[@id="mainblock"]')[0]
        forms = box.xpath('.//form')
        for form in forms:
            divs = form.xpath('.//div[@class="cardtv"]')
            if not divs:
                continue
            pk = form.attrib.get('id').replace('form', '')
            div = divs[0]
            price = form.xpath('.//input[@name="cena"]')
            if price:
                price = price[0].attrib.get('value')
            else:
                span = form.xpath('.//span[@class="cena"]')[0]
                price = span[0].text
                price = kill_quotes(price, 'int')
            products.append({'code': pk, 'price': price, 'cat': cat})
        return products

    def cat_level_helper(self, name: str, tag: str, parents: str = None):
        """Вспомогательная функция для заполнения уровня меню
           :param name: название меню
           :param tag: тег меню
        """
        new_tag = 'cat_%s' % tag.replace('/catalog.php?idg=', '')
        return {
            'name': name,
            'tag': new_tag,
            'container': self.container,
            'state': 4,
            'parents': parents,
        }

    def fetch_catalogue(self):
        """Скомуниздить каталог"""
        r = requests.get(self.domain)
        content = r.text
        tree = lxml_html.fromstring(content)
        box = tree.xpath('//div[@id="catalogmenupc"]')[0]
        container = box.xpath('.//div[@class="conteiner"]/ul')[0]

        level0 = []
        level1 = []
        level2 = []
        last_level = [] # Уровень без children

        lis = container.xpath('.//li')
        for li in lis:
            name = li[0].text # // <a>Медтехника для дома</a>
            tag = li.attrib.get('rel')
            if not tag:
                continue
            level0.append(self.cat_level_helper(name, tag))

        # Заполняем верхний уровень
        for item in level0:
            analog = self.container.blocks_set.filter(tag=item['tag']).first()
            if not analog:
                analog = Blocks.objects.create(**item)
            item['id'] = analog.id
        # Верхний уровень заполнен

        for item in level0:
            rel = item['tag'].replace('cat_', '')
            spans = container.xpath('.//p[@id="subc%s"]/span' % rel)
            for span in spans:
                if not span.tag == 'span':
                    continue
                name = span[0].text
                tag = span[0].attrib.get('href')
                # Надо сразу создавать второй уровень,
                # чтобы знать parents для третьего
                cat = self.cat_level_helper(name, tag, '_%s' % item['id'])
                analog = self.container.blocks_set.filter(tag=cat['tag']).first()
                if not analog:
                    analog = Blocks.objects.create(**cat)
                cat['id'] = analog.id
                level1.append(cat)
                subspans = span.xpath('.//span/a')
                if(len(subspans) == 0):
                    last_level.append(cat['tag'])
                    continue
                # Сразу хомячим третий уровень
                for subspan in span:
                    if not subspan.tag == 'span':
                        continue
                    name = subspan[0].text
                    tag = subspan[0].attrib.get('href')
                    subcat = self.cat_level_helper(name, tag, '%s_%s' % (cat['parents'], cat['id']))
                    analog = self.container.blocks_set.filter(tag=subcat['tag']).first()
                    if not analog:
                        analog = Blocks.objects.create(**subcat)
                    subcat['id'] = analog.id
                    level2.append(subcat)
                    last_level.append(subcat['tag'])
        return last_level




