#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from lxml import html

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.flatcontent.models import Containers, Blocks
from apps.products.models import Products, Property, PropertiesValues, ProductsProperties, ProductsCats, ProductsPhotos
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file, make_folder
from apps.products.models import Products, ProductsPhotos, ProductsCats

logger = logging.getLogger(__name__)

token = 'epATp8_p3J_lS60jpy11Opaz856N47U1We0yKnrft1ciS7SpQuZVG5Gk0Oe6cX_od1tVdIHUS1DPah4B8hJx6N-GBcuqPS1giH6p-SBOLo_etEFLzp1j-WsSLWoFQwVG_GjyQoWJJRJ2OQlv3qCqUQ2'
token_hash = 'hGTKJxHup6eap6yzSMUYWB7tV6eJirumdQ6uKK_tEpaKIb-ae82Crm2Rx7n_DZQT_Htkzx1DTnqVxW9qdaNnmjNm_j0rFSiDjbDtsEu3kC1fmXPP9V_735bo5pdeP9wGVeJKW-0TKeIyN1ig1kChhg2'

host = 'https://emex.ru'
endpoint = '/Accessories/Accessories/GetProducts'

# TEST
#host = 'http://httpbin.org'
#endpoint = '/post'

demo_urla = 'https://emex.ru/Accessories/Accessories?%s' % '&'.join([
       'CAT_ID=36',
       's[0].i=Price',
       's[0].d=0',
       's[1].i=Rating',
       's[1].d=2'])

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
headers = {
    'referer': demo_urla,
    'User-Agent': user_agent,
    'X-Requested-With': 'XMLHttpRequest',
}

cookies = {
    'siteversion': '2',
    '__RequestVerificationToken': token_hash,
}

def show_link(link):
    """Преобразовывает ссылку
       'CatalogCategoryId=36&CurrencyId=1&SearchString=&CurrentPage=9&SortFields%5B0%5D%5BCode%5D=Price&SortFields%5B0%5D%5BDirection%5D=0&SortFields%5B1%5D%5BCode%5D=Rating&SortFields%5B1%5D%5BDirection%5D=2&__RequestVerificationToken=3O98nIsVPL4d6c7R1Qdul0X690zVfbuIlgrg4FUuh1yJ_awkwAwocSK46vhDnM7UmA1MHq_MXGXb_2OQFoi7ytSi6HUSDQ86nTHj0pCdrugoiiPzoq-AlWMcHD_AFkLnCBxbXF1VuXCh9RDImHcUKQ2'
       в читаемый вид
       'CatalogCategoryId=36&CurrencyId=1&SearchString=&CurrentPage=9&SortFields[0][Code]=Price&SortFields[0][Direction]=0&SortFields[1][Code]=Rating&SortFields[1][Direction]=2&__RequestVerificationToken=3O98nIsVPL4d6c7R1Qdul0X690zVfbuIlgrg4FUuh1yJ_awkwAwocSK46vhDnM7UmA1MHq_MXGXb_2OQFoi7ytSi6HUSDQ86nTHj0pCdrugoiiPzoq-AlWMcHD_AFkLnCBxbXF1VuXCh9RDImHcUKQ2'
    """
    from urllib.parse import unquote
    return unquote(link)

def grab_products(cat_id: int = 36, demo_mode: bool = False):
    """Получить товары
       :param cat_id: Категория для привязки товаров
       :param demo_mode: Получить только первую страничку
    """
    products = []
    params = {
        'CatalogCategoryId': cat_id,
        'CurrencyId': 1,
        'SearchString': '',
        'CurrentPage': 0,
        'SortFields[0][Code]': 'Price',
        'SortFields[0][Direction]': 0,
        'SortFields[1][Code]': 'Rating',
        'SortFields[1][Direction]': 2,
        '__RequestVerificationToken': token,
    }
    # С первой странички ответы
    max_pages = 10000
    for i in range(1, max_pages):
        params['CurrentPage'] = i
        urla = '%s%s' % (host, endpoint)

        r = requests.post(urla, data=params, headers=headers, cookies=cookies)

        if not r.status_code == 200:
            logger.info('%s => %s' % (r.status_code, r.text))
            continue

        resp = r.json()
        items = resp.get('data', {}).get('Items', [])
        # len(items) == 0, когда кончилась пагинация
        if len(items) == 0:
            #logger.info('zero answer %s' % json_pretty_print(params))
            break

        products += items
        if demo_mode:
            break

    return products

def update_products(products_list: list, cat_id: int = 36):
    """Обновление товаров
       :param products_list: список json товаров
       :param cat_id: ид категории для привязки товаров
    """
    container = Containers.objects.filter(tag='catalogue', state=7).first()
    cat = container.blocks_set.filter(tag='_cat_%s' % cat_id).first()
    for item in products_list:
        code = '_em_%s' % item['ProductId']
        analog = Products.objects.filter(code=code).first()
        if not analog:
            analog = Products(
                code=code,
            )
        price = item.get('MinPrice', {}).get('Value')
        if not price:
            price = item.get('LowestPrice', {}).get('Value')
        analog.name = item['ProductName']
        analog.altname = item['ProductCode']
        analog.manufacturer = item['MakeName'] # MakeId код производителя
        analog.mini_info = item['DescriptionShort']
        analog.info = item['Description']
        analog.count = item['OffersCount']
        analog.price = price
        try:
            analog.save()
        except Exception:
            logger.error('Ошибка сохранения %s' % json_pretty_print(item))
            continue
        # Привязка рубрики
        if cat:
            cat_link = ProductsCats.objects.filter(product=analog, cat=cat).values_list('id', flat=True)
            if not cat_link:
                cat_link = ProductsCats.objects.create(
                    product=analog,
                    cat=cat,
                    container=container,
                )
        if item['ImageUrls'] and not analog.img:
            img = grab_img_by_url(item['ImageUrls'][0], analog)
            if img:
                Products.objects.filter(pk=analog.id).update(img=img)

            if len(item['ImageUrls']) > 1:
                logger.info('gallery %s' % analog.id)
                for photo in item['ImageUrls'][1:]:
                    new_photo = Photo.objects.create(product=analog)
                    img = grab_img_by_url(photo, new_photo)
                    if img:
                        Photos.objects.filter(pk=new_photo.id).update(img=img)
        update_props(analog, item)

def update_props(product, obj):
    """Обновление свойств товара"""
    props = obj.get('Properties')
    if not props:
        return
    for k, v in props.items():
        prop = Property.objects.filter(code=k).first()
        if not prop:
            measure = v.get('Units')
            if not measure:
                measure = None
            caption = v['Caption']
            if caption:
                caption = caption.replace(':', ''), # нахер там ":"?
            prop = Property.objects.create(
                code=k,
                name=caption,
                measure=measure,
            )
        pvalue = PropertiesValues.objects.filter(
            prop=prop,
            str_value=v['Value'],
        ).first()
        if not pvalue:
            pvalue = PropertiesValues.objects.create(
                prop=prop,
                str_value=v['Value'],
            )
        product_prop = ProductsProperties.objects.filter(
            product=product,
            prop=pvalue,
        ).first()
        if not product_prop:
            product_prop = ProductsProperties.objects.create(
                product=product,
                prop=pvalue,
            )

def grab_img_by_url(url, obj):
    """Получение картинки по ссылке
       :param url: ссылка
       :param obj: объект, куда добавляем изображение
    """
    if 'id=0' in url:
        return
    link = url.replace('&h=150', '')
    r = requests.get(link, headers=headers, cookies=cookies)
    resp = r.content
    img = '%s.jpg' % obj.id
    folder = obj.get_folder()
    fname = '%s/%s' % (folder, img)
    make_folder(folder)
    with open_file(fname, 'wb+') as f:
        f.write(resp)
    return img

def get_catalogue():
    """Получение рубрик каталога"""
    tree_endpoint = '/api/home/tree'
    r = requests.get('%s%s' % (host, tree_endpoint), headers=headers, cookies=cookies)
    resp = r.json()
    return resp

def update_catalogue(catalogue: list = None, parents: str = None):
    """Обновление каталога"""
    if not catalogue:
        catalogue = get_catalogue()
    container = Containers.objects.filter(tag='catalogue', state=7).first()
    if not container:
        container = Containers.objects.create(
            tag='catalogue', state=7,
            name='Каталог',
        )
    for item in catalogue:
        if item['id'] < 1:
            continue
        tag = '_cat_%s' % item['id']
        cat = Blocks.objects.filter(
            container=container, state=4,
            tag=tag
        ).first()
        if not cat:
            cat = Blocks.objects.create(
                container=container, state=4,
                tag=tag, name=item['title'],
                parents=parents,
            )
        children = item.get('children')
        if children:
            new_parents = '_%s' % cat.id
            if parents:
                new_parents = '%s%s' % (parents, new_parents)
            update_catalogue(children, new_parents)

def update_cat(cat, demo_mode: str = True):
    """Обновить товары рубрики
       :param cat: рубрика
       :param demo_mode: демо-режим (первая страничка товаров)
    """
    if not cat.tag or not '_cat_' in cat.tag:
        return
    cat_id = int(cat.tag.replace('_cat_', ''))
    products = grab_products(cat_id = cat_id, demo_mode = demo_mode)
    update_products(products, cat_id = cat_id)

def test_cat_update():
    urla = '%s%s' % (host, endpoint)
    params = {
        'CatalogCategoryId': 66,
        'CurrencyId': 1,
        'SearchString': '',
        'CurrentPage': 1,
        'SortFields[0][Code]': 'Price',
        'SortFields[0][Direction]': 0,
        'SortFields[1][Code]': 'Rating',
        'SortFields[1][Direction]': 2,
        '__RequestVerificationToken': token,
    }
    sheaders = {
        'referer': 'https://emex.ru/Accessories/Accessories?%s' % '&'.join([
            'CAT_ID=66',
            's[0].i=Price',
            's[0].d=0',
            's[1].i=Rating',
            's[1].d=2']),
        'User-Agent': user_agent,
        'X-Requested-With': 'XMLHttpRequest',
    }

    r = requests.post(urla, data=params, headers=sheaders, cookies=cookies)
    print(r.text, r.headers)
    # Сопоставить можно через
    #print(r.request.body)
    #print(r.request.body == "CatalogCategoryId=66&CurrencyId=1&SearchString=&CurrentPage=1&SortFields%5B0%5D%5BCode%5D=Price&SortFields%5B0%5D%5BDirection%5D=0&SortFields%5B1%5D%5BCode%5D=Rating&SortFields%5B1%5D%5BDirection%5D=2&__RequestVerificationToken=epATp8_p3J_lS60jpy11Opaz856N47U1We0yKnrft1ciS7SpQuZVG5Gk0Oe6cX_od1tVdIHUS1DPah4B8hJx6N-GBcuqPS1giH6p-SBOLo_etEFLzp1j-WsSLWoFQwVG_GjyQoWJJRJ2OQlv3qCqUQ2")
    #print(r.request.headers)
    #for k, v in r.request.headers.items():
    #    print(k, '=>', v)

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
        #test_cat_update()
        #exit()

        demo_mode = options.get('demo_mode')
        cat_id = options.get('cat_id')
        update_catalogue()

        catalogue = Containers.objects.filter(tag='catalogue', state=7).first()
        if cat_id:
            tag = '_cat_%s' % cat_id
            cat = catalogue.blocks_set.filter(tag=tag).first()
            if not cat:
                logger.info('%s cat not found' % tag)
                return
            logger.info('only %s cat' % tag)
            children = Blocks.objects.filter(parents='_%s' % cat.id)
            if not children:
                update_cat(cat, demo_mode)
            else:
                for child in children:
                    logger.info('child %s' % child.tag)
                    update_cat(child, demo_mode)
            return
        cats = catalogue.blocks_set.filter(parents='')
        for cat in cats:
            children = Blocks.objects.filter(parents='_%s' % cat.id)
            if not children:
                update_cat(cat, demo_mode)
            else:
                for child in children:
                    update_cat(child, demo_mode)
