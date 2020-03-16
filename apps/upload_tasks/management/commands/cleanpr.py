#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from lxml import html

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.catcher import json_pretty_print
from apps.products.models import Products, ProductsPhotos

logger = logging.getLogger(__name__)

host = 'https://www.cleanpr.ru'
headers = {"X-Requested-With":"XMLHttpRequest"}

def parse_ul_menu(ul, result):
    """Рекурсивный обход меню"""
    for li in ul:
        menu = {'name': None, 'href': None, 'img': None, 'sub': []}
        for item in li:
            tag = item.tag.lower()
            if tag == 'a':
                name = item.text
                if not name:
                    for subitem in item:
                        name = subitem.text
                        if name:
                            break
                href = item.attrib.get('href')
                menu['href'] = href
                menu['name'] = name
                result.append(menu)
            elif tag == 'ul':
                parse_ul_menu(item, result[-1]['sub'])
            elif tag == 'span':
                for subitem in item:
                    for img in subitem:
                        imga = img.attrib.get('src')
                        if imga:
                            menu['img'] = imga
                            break
            #else:
            #    print(item.tag.lower())

def create_catalogue(rubrics, parents='', tag: str = 'catalogue'):
    """Заполнение рубрик"""
    catalogue = Containers.objects.filter(tag='catalogue', state=7).first()
    if not catalogue:
        catalogue = Containers.objects.create(
            tag = tag,
            state = 7,
            name = 'Каталог продукции',
        )
    for rubric in rubrics:
        link = rubric['href'].replace('/catalog/', '/cat/')
        if not link.endswith('/'):
            link = '%s/' % link
        analog = catalogue.blocks_set.filter(link=link).first()
        if not analog:
            analog = Blocks.objects.create(
                link = link,
                name = rubric['name'],
                parents = parents,
                container = catalogue,
                state = 4,
            )
            if rubric['img']:
                imga = '%s%s' % (host, rubric['img'])
                analog.upload_img(imga)
            if rubric['sub']:
                create_catalogue(rubric['sub'], '%s_%s' % (parents, analog.id), tag)

def new_catalogue(tag: str = 'catalogue'):
    """Создание каталога
       TODO: Перейти на
             все рубрики, еще и с подписанным кол-вом товаров
             all_rubrics = 'https://www.cleanpr.ru/catalog'
    """
    result = []
    r = requests.get(host)
    tree = html.fromstring(r.text)
    ul = tree.xpath('//ul[@class="menu dropdown"]')[0]
    parse_ul_menu(ul, result)
    #print(json_pretty_print(result))
    create_catalogue(result)

def grab_products(rubric):
    """Получить все товары по рубрике
       :param rubric: рубрика

       Когда встречаем первый товар,
       при переходе на следующую страничку,
       значит странички закончились
       params = {'display': 'list', 'PAGEN_1': 20, 'ajax_get': 'y'}
       r = requests.get('https://www.cleanpr.ru/catalog/gigienicheskaya-produktsiya/tualetnaya-bumaga', params=params, headers=headers)
       print(r.text)

       На этом уровне есть помимо списка брендов статья
       также могут быть дополнительные подрубрики
    """
    link = rubric.link.replace('/cat/', '/catalog/')
    params = {'display': 'list', 'PAGEN_1': 1, 'ajax_get': 'y'}
    urla = '%s%s' % (host, link)
    products = []
    for i in range(1, 99):
        params['PAGEN_1'] = i
        r = requests.get(urla, headers=headers, params=params)
        tree = html.fromstring(r.text)
        content = tree.xpath('//div[@class="display_list"]')[0]
        # Каждая таблица - товар
        tables = content.xpath('.//table[@class="list_item"]')
        for table in tables:
            href = table.xpath('.//a[@class="thumb"]')[0]
            product_link = href.attrib.get('href').replace('/catalog/../', '/')
            product = grab_product('%s%s' % (host, product_link))
            if not product.get('price', {}).get('id'):
                continue
            # Проверяем, если мы уже имеем такой товар,
            # значит больше нехуй запрашивать - нам вернули
            # первую страничку - наибать пытаются
            in_list = [x['price']['id'] for x in products if product['price']['id'] == x['price']['id']]
            if in_list:
                return products
            #print(json_pretty_print(product))
            products.append(product)
    # Мы всегда должны возвращаться в цикле не доходя до конца
    assert False

def get_props(tr):
    """Получить характеристики из html таблицы
       :param tr: Element tr"""
    props = []
    for item in tr:
        prop = {}
        if item.tag.lower() == 'td':
            class_name = item.attrib.get('class')
            if class_name == 'char_name':
                value = item.xpath('.//span')[0]
                prop['name'] = value.text.strip()
            elif class_name == 'char_value':
                value = item.xpath('.//span')[0]
                prop['value'] = value.text.strip()
        if prop:
            props.append(prop)
    return props

def grab_product(href: str):
    """Получить товар по ссылке
       :param href: ссылка на товар"""
    r = requests.get(href, headers=headers, params={})
    tree = html.fromstring(r.text)

    photos = []
    slider = tree.xpath('//div[@class="slides"]')[0]
    slides = slider.xpath('.//ul')
    if slides:
        for slide in slides[0]:
            if slide.tag.lower() == 'li':
                for item in slide:
                    if item.tag.lower() == 'a':
                        photos.append(item.attrib.get('href'))
    else:
        for slide in slider:
            if slide.tag.lower() == 'div':
                for item in slide:
                    if item.tag.lower() == 'a':
                        photos.append(item.attrib.get('href'))
    name = tree.xpath('//div[@class="preview_text dotdot"]')[0].text.strip()

    brand = {}
    brand_blocks = tree.xpath('//div[@class="brand"]')
    if brand_blocks:
        img = brand_blocks[0].xpath('.//img')[0]
        brand['img'] = img.attrib.get('src')
        brand['name'] = img.attrib.get('title')
    #print('photos', photos)
    #print('brand', brand)

    price = {}
    price_blocks = tree.xpath('//div[@class="button_block"]')
    if price_blocks:
        for item in price_blocks[0]:
            if item.attrib.get('data-currency'):
                price = {
                    'cost': item.attrib.get('data-value'),
                    'currency': item.attrib.get('data-currency'),
                    'id': item.attrib.get('data-item'),
                }
    #print('price', price)

    props = []
    props_lists = tree.xpath('//table[@class="props_list"]')
    for props_list in props_lists:
        for item in props_list:
            if item.tag.lower() == 'tr':
                new_props = get_props(item)
                if new_props:
                    props.append(new_props)
    return {
        'name': name,
        'props': props,
        'photos': photos,
        'brand': brand,
        'price': price,
    }

def save_product(product: dict):
    """Сохранить товар"""
    price = product.get('price', {})
    code = price.get('id')
    if not code:
        logger.info('[ERROR]: %s absent id' % product)
    analog = Products.objects.filter(code=code).first()
    if not analog:
        analog = Products(code=code)
    cost = price.get('cost')
    if cost:
        analog.price = float(cost)
    name = product.get('name')
    if name:
        analog.name = name
    analog.save()
    photos = product.get('photos', [])
    if photos:
        if not analog.img:
            photo = photos[0]
            analog.upload_img('%s%s' % (host, photo))

        #analog.productsphotos_set.all().delete()
        analog_photos = analog.productsphotos_set.all()
        if len(photos) > 1 and not analog_photos:
            for photo in photos[1:]:
                new_photo = ProductsPhotos.objects.create(product=analog)
                new_photo.upload_img(photo)

def parse_rubrics():
    """Обойти все рубрики в поисках товаров"""
    rubrics = Blocks.objects.filter(container__state=7,
                                    container__tag='catalogue',
                                    parents__startswith='_')
    for rubric in rubrics:
        logger.info(rubric.link)
        try:
            products = grab_products(rubric)
        except Exception:
            logger.info('[ERROR]: grab_products %s' % (rubric.link, ))
            continue
        logger.info('%s => %s' % (rubric.name, len(products)))
        for product in products:
            try:
                save_product(product)
            except Exception:
                logger.info('[ERROR]: save_product %s' % (product, ))
            #return

class Command(BaseCommand):
    def handle(self, *args, **options):
        for block in Blocks.objects.filter(container__isnull=True):
            block.delete()
        parse_rubrics()




