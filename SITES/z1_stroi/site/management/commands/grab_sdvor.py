#-*- coding:utf-8 -*-
import os
import requests
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.main_functions.catcher import json_pretty_print
from apps.flatcontent.models import Containers, Blocks
from apps.products.models import Products, ProductsCats, ProductsPhotos, Property, PropertiesValues, ProductsProperties

logger = logging.getLogger('main')

def get_container():
    """Получение контейнера для каталога"""
    container = Containers.objects.filter(tag='catalogue', state=7).first()
    if not container:
        container = Containers.objects.create(
            name='Каталог товаров',
            tag='catalogue',
            state=7)
    return container


def fill_catalogue(branches: list, container: Containers, parent: Blocks = None):
    """Заполнить каталог иерархией
       :param branches: рубрики
       :param container: контейнер каталога
       :param parents: родительский блок
    """
    for branch in branches:
        if branch['name'].startswith('__'):
            continue
        tag = 'cat_%s' % branch['id']
        analog = container.blocks_set.filter(tag=tag).first()
        if not analog:
            analog = Blocks(tag=tag, container=container)
        analog.name = branch['name']
        if parent:
            root_parents = parent.parents if parent.parents else ''
            analog.parents = '%s_%s' % (root_parents, parent.id)
        analog.state = 4
        analog.save()
        sub_branches = branch.get('branches')
        if sub_branches:
            fill_catalogue(sub_branches, container, analog)


def get_hierarchy():
    """Создать каталог"""
    urla = 'https://catalog-hierarchy.itlabs.io/api/hierarchy'
    r = requests.get(urla)
    resp = r.json()
    container = get_container()
    fill_catalogue(resp['branches'], container)


def fill_products(cat: Blocks):
    """Получение и заполнение товаров по конкретной рубрике
       :param cat: рубрика
    """
    logger.info('fetching %s' % cat.name)
    urla = 'https://catalog-api.itlabs.io/hierarchy/{}/products/'
    params = {
        'city_id': '1000',
        'only_in_stock': 1,
        'only_with_cat': 1,
        'size': 50,
        'from': 0,
    }
    url = urla.format(cat.tag.split('_')[-1])

    result = []
    while True:
        r = requests.get(url, params=params)
        resp = r.json()
        products = resp.get('products')
        total = int(resp.get('total'))
        if not products or not total:
            break
        print('%s from %s' % (len(result), total))
        params['from'] += len(products)
        result += [{
            'name': p['name'],
            'code': p['erp_id'],
            'manufacturer': p.get('brand'),
            'price': p.get('price'),
            'measure': p.get('unit'),
        } for p in products]
    for product in result:
        analog = Products.objects.filter(code=product['code']).first()
        if not analog:
            analog = Products(code=product['code'])
        analog.name = product['name']
        analog.manufacturer = product['manufacturer']
        analog.price = product['price']
        analog.measure = product['measure']
        analog.save()

        cat_link = ProductsCats.objects.filter(product=analog, cat=cat).first()
        if not cat_link:
            ProductsCats.objects.create(product=analog, cat=cat, container=cat.container)


def get_products():
    """Получение товаров по категориям последнего уровня
    """
    container = get_container()
    all_cats = container.blocks_set.select_related('container').all()
    for cat in all_cats:
        root_parents = cat.parents if cat.parents else ''
        parents = '%s_%s' % (root_parents, cat.id)
        children = Blocks.objects.filter(parents=parents).aggregate(Count('id'))['id__count']
        if children or not cat.tag or not '_' in cat.tag:
            continue
        fill_products(cat)


def load_images():
    """Загрузить картинки к товарам"""
    urla = 'https://cdn.sdvor.com/images/presets'
    by = 50
    query = Products.objects.filter(img__isnull=True)
    total_rows = query.aggregate(Count('id'))['id__count']
    total_pages = int(total_rows / by) + 1
    for i in range(total_pages):
        print('%s from %s' % (i, total_pages))
        rows = query[i*by:i*by+by]
        for row in rows:
            params = {'ids': row.code}
            r = requests.get(urla, params=params)
            print(urla, params)
            resp = r.json()
            data = resp.get('data', {})
            product_images = data.get(row.code, {})
            images = product_images.get('images', [])
            if images:
                row.upload_img(images[0]['urls']['big'])
            for imga in images[1:]:
                new_photo = ProductsPhotos.objects.create(product=row)
                new_photo.upload_img(imga['urls']['big'])
            logger.info('%s images uploaded (%s)' % (row.code, len(images)))


def remove_empty_cats():
    """Удаление пустых категорий"""
    fordel = []
    lower_than = 35
    greater_than = 55
    container = get_container()
    all_cats = container.blocks_set.all()
    for cat in all_cats:
        root_parents = cat.parents if cat.parents else ''
        parents = '%s_%s' % (root_parents, cat.id)
        children = Blocks.objects.filter(parents=parents).aggregate(Count('id'))['id__count']
        if children or not cat.tag or not '_' in cat.tag:
            continue
        linked_products = ProductsCats.objects.filter(cat=cat).aggregate(Count('id'))['id__count']
        if linked_products < lower_than or linked_products > greater_than:
            print('drop %s products from %s' % (linked_products, cat.name))
            for linked_product in ProductsCats.objects.select_related('product').filter(cat=cat):
                product = linked_product.product
                product.delete()
        if not linked_products:
            fordel.append(cat)
    logger.info('fordel %s' % len(fordel))
    for cat in fordel:
        cat.delete()


def remove_cat(cat_id: int):
    """Удаление категории"""
    fordel = []
    container = get_container()
    cat = container.blocks_set.filter(pk=cat_id).first()
    if not cat:
        return
    root_parents = cat.parents if cat.parents else ''
    parents = '%s_%s' % (root_parents, cat.id)
    children = Blocks.objects.filter(parents=parents).aggregate(Count('id'))['id__count']
    if children or not cat.tag or not '_' in cat.tag:
        print('children or not tag or not _ in tag')
        return
    for linked_product in ProductsCats.objects.select_related('product').filter(cat=cat):
        product = linked_product.product
        product.delete()


def load_properties():
    """Загрузить свойства к товарам"""
    urla = 'https://catalog-api.itlabs.io/products/{}/view/'
    params = {'city_id': 1000}
    by = 50
    query = Products.objects.all()
    total_rows = query.aggregate(Count('id'))['id__count']
    total_pages = int(total_rows / by) + 1
    for i in range(total_pages):
        rows = query[i*by:i*by+by]
        print('%s from %s' % (i, total_pages))
        for row in rows:
            r = requests.get(urla.format(row.code), params=params)
            resp = r.json()
            products = resp.get('products', [])
            if not products:
                continue
            product = products[0]
            #print(json_pretty_print(product))

            description = None
            descriptions = product.get('descriptions', [])
            if descriptions:
                description = descriptions[0]['text'].replace('https://www.sdvor.com/', '/').replace('https://sdvor.com/', '/')
            new_values = {
                'manufacturer': product.get('brand'),
                'info': description,
                'measure': product.get('unit'),
            }
            Products.objects.filter(pk=row.id).update(**new_values)
            # Свойства товара
            props = product.get('properties', [])
            fill_properties(row, props)


def fill_properties(product: Products, properties: list):
    """Заполнение свойствами товара
       :param product: экземпляр модели Products
       :param properties: свойства товара
    """
    for item in properties:
        prop_id = item['prop_id']
        prop = Property.objects.filter(code=prop_id).first()
        if not prop:
            prop = Property(code=prop_id)
        prop.name = item['prop']
        prop.save()

        pvalue = PropertiesValues.objects.filter(prop=prop, str_value=item['value']).first()
        if not pvalue:
            pvalue = PropertiesValues.objects.create(prop=prop, str_value=item['value'])

        analog = ProductsProperties.objects.filter(prop=pvalue, product=product).first()
        if not analog:
            ProductsProperties.objects.create(prop=pvalue, product=product)


class Command(BaseCommand):
    """Проверка формирования файла с заказами"""
    def add_arguments(self, parser):
        parser.add_argument('--fake',
            action = 'store',
            dest = 'fake',
            type = str,
            default = False,
            help = 'Set fake')
    def handle(self, *args, **options):
        #get_hierarchy()
        #get_products()
        remove_empty_cats()
        #load_images()
        load_properties()
