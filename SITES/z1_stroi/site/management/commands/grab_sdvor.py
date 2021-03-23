#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import os
import requests
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.flatcontent.models import Containers, Blocks
from apps.products.models import Products, ProductsCats, ProductsPhotos

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
            ProductsCats.objects.create(product=analog, cat=cat)


def get_products():
    """Получение товаров по категориям последнего уровня
    """
    container = get_container()
    all_cats = container.blocks_set.all()
    for cat in all_cats:
        root_parents = cat.parents if cat.parents else ''
        parents = '%s_%s' % (root_parents, cat.id)
        children = Blocks.objects.filter(parents=parents).aggregate(Count('id'))['id__count']
        if children or not cat.tag or not '_' in cat.tag:
            continue
        fill_products(cat)


def load_images():
    """Загрузить картинки к товарам"""
    urla = 'https://www.sdvor.com/images/presets'
    by = 50
    query = Products.objects.filter(img__isnull=True)
    total_rows = query.aggreagate(Count('id'))['id__count']
    total_pages = int(total_rows / by) + 1
    for i in range(total_pages):
        rows = query[i*by:i*by+by]
        for row in rows:
            params = {'ids': product.code}
            r = requests.get(urla, params=params)
            resp = r.json()
            data = resp.get('data', {})
            product_images = data.get(row.code, {})
            images = product_images.get('images', [])
            if images:
                row.upload_img(images[0]['big'])
            for imga in images[1:]:
                new_photo = ProductsPhotos.objects.create(product=row)
                new_photo.upload_img(imga['big'])
            logger.info('%s images uploaded (%s)' % (row.code, len(images)))


def load_properties():
    """Загрузить свойства к товарам"""
    urla = 'https://catalog-api.itlabs.io/products/{}/view/'
    params = {'city_id': 1000}
    by = 50
    query = Products.objects.all()
    total_rows = query.aggreagate(Count('id'))['id__count']
    total_pages = int(total_rows / by) + 1
    for i in range(total_pages):
        rows = query[i*by:i*by+by]
        for row in rows:
            pass


def remove_empty_cats():
    """Удаление пустых категорий"""
    fordel = []
    container = get_container()
    all_cats = container.blocks_set.all()
    for cat in all_cats:
        root_parents = cat.parents if cat.parents else ''
        parents = '%s_%s' % (root_parents, cat.id)
        children = Blocks.objects.filter(parents=parents).aggregate(Count('id'))['id__count']
        if children or not cat.tag or not '_' in cat.tag:
            continue
        linked_products = ProductsCats.objects.filter(cat=cat).aggregate(Count('id'))['id__count']
        if not linked_products:
            fordel.append(cat)
    for cat in fordel:
        cat.delete()


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

