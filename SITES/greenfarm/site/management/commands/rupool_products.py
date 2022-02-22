#-*- coding:utf-8 -*-
import re
import os
import time
import json
import logging
import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.products.models import (
    Products,
    PropertyGroup,
    Property,
    PropertiesValues,
    ProductsProperties,
    ProductsCats,
    CostsTypes,
    Costs, )
from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.files import open_file, make_folder
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.string_parser import kill_quotes

logger = logging.getLogger(__name__)

"""Обновление товаров
   товары получены с rupool rupool_report скриптом

   TODO: обновление категорий товаров
"""

def rebuild_catalogue():
    """Удаление старого каталога и создание нового"""
    folder = 'rupool'
    catalogue = Containers.objects.filter(tag='catalogue').first()
    if not catalogue:
        catalogue = Containers.objects.create(tag='catalogue', state=7)
    #for item in catalogue.blocks_set.all():
    #    item.delete()
    src = os.path.join(folder, 'cats.json')
    with open_file(src, 'r', encoding='utf-8') as f:
        cats = json.loads(f.read())

    def recursive_fill(parent: int = None, pass_img: bool = False):
        """Рекурсивное заполнение категорий"""
        for item in cats:
            item_parents = item['parents']

            # Идем в этом случае по корневой
            if not parent and item_parents:
                continue
            # Если код есть, корень пропускаем
            if parent and not item_parents:
                continue
            # Не соответствующий parent
            if item_parents:
                cur_parent = item_parents[-1]['id']
                if not parent == cur_parent:
                    continue

            cat_name = item.get('name')
            if not cat_name:
                #print('[ERROR]: cat name empty %s' % item)
                continue

            cat = Blocks.objects.filter(tag=item['id'], container=catalogue).first()
            if not cat:
                parents = ''
                if parent:
                    cat_parent = Blocks.objects.filter(tag=parent).first()
                    parents = '%s_%s' % (cat_parent.parents, cat_parent.id)
                cat = Blocks.objects.create(
                    name=cat_name,
                    tag=item['id'],
                    container=catalogue,
                    html=item['desc'],
                    parents=parents,
                    state=4, )
            if not cat.img and item['img'] and not pass_img:
                urla = 'https://www.rupool.ru%s' % item['img']
                r = requests.get(urla)
                fname = urla.split('/')[-1]
                dest = os.path.join(cat.get_folder(), fname)
                make_folder(cat.get_folder())
                with open_file(dest, 'wb+') as f:
                    f.write(r.content)
                cat.img = fname
                Blocks.objects.filter(pk=cat.id).update(img=fname)
            recursive_fill(item['id'])

    recursive_fill()

def drop_products():
    """Очистка товаров"""
    def drop_helper(objs):
        """Вспомогательная функция для удаления"""
        for i, obj in enumerate(objs):
            if i % 1000 == 0:
                print(type(obj), i, '/', len(objs))
            obj.delete()

    products = Products.objects.all()
    drop_helper(products)
    props = Property.objects.all()
    drop_helper(props)

def update_products():
    """Загружаем товары из файлов"""
    folder = 'rupool'
    products_data = {}
    for i in range(2):
        fname = 'products%s.json' % ('' if i == 0 else i)
        src = os.path.join(folder, fname)
        with open_file(src, 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
        for item in content:
            if item['id'] in products_data:
                assert False
            products_data[int(item['id'])] = item
            #print(json_pretty_print(item))
            #return

    by = 500
    query = Products.objects.filter(is_active=True)
    total_rows = query.aggregate(Count('id'))['id__count']
    pages = (int(total_rows/by)) + 1

    # Помечаем товары удаленными
    for i in range(pages):
        print('products for drop: %s/%s' % (i+1, pages))
        products = query[i*by: i*by+by]
        for product in products:
            product_code = int(product.code)
            if not product_code in products_data:
                print(product.code, 'for drop')
                #Products.objects.filter(pk=product.id).update(is_active=False)
                product.delete()

    opt_price = CostsTypes.objects.all().first()
    # Заполняем товары / обновляем
    i = 0
    for product_code, data in products_data.items():
        if not data:
            return
        i += 1
        if i % 1000 == 0:
            print(i, '/', len(products_data))
        product = Products.objects.filter(code=product_code).first()
        if not product:
            product = Products.objects.create(code=product_code)
        product.mini_info = data.get('mini_info')
        product.price = int(kill_quotes(data.get('price', '0'), 'int'))
        discount = int(kill_quotes(data.get('discount', '0'), 'int'))
        if discount and product.price:
            discount = int(discount)
            cost = Costs.objects.filter(product=product, cost_type=opt_price).first()
            if not cost:
                cost = Costs(product=product, cost_type=opt_price)
            cost.cost = product.price - (product.price / 100 * discount)
            cost.save()
        product.name = data.get('name')

        # Заполняем привязки к категориям
        cat_code = data.get('cat')
        cat = Blocks.objects.filter(tag=cat_code).first()
        if not cat:
            print('[ERROR]: cat not found %s for %s' % (cat_code, data))
        else:
            cat_link = ProductsCats.objects.filter(product=product, cat=cat).first()
            if not cat_link:
                ProductsCats.objects.create(product=product, cat=cat)

        # Заполняем свойства
        product.save()
        props = data.get('props', [])
        for item in props:
            prop_group = PropertyGroup.objects.filter(name=item['group']).first()
            if not prop_group:
                prop_group = PropertyGroup.objects.create(name=item['group'])
            prop = Property.objects.filter(name=item['name'], group=prop_group).first()
            if not prop:
                prop = Property.objects.create(name=item['name'], ptype=4, search_facet=True, group=prop_group)
            prop_value = PropertiesValues.objects.filter(prop=prop, str_value=item['value']).first()
            if not prop_value:
                try:
                    prop_value = PropertiesValues.objects.create(prop=prop, str_value=item['value'])
                except Exception as e:
                    print(e, item)
                    continue
            link = ProductsProperties.objects.filter(prop=prop_value, product=product)
            if not link:
                ProductsProperties.objects.create(prop=prop_value, product=product)

def update_stocks():
    """Загружаем остатки из файлов"""
    folder = 'rupool'
    stocks_data = []
    for i in range(2):
        fname = 'stocks%s.json' % ('' if i == 0 else i)
        src = os.path.join(folder, fname)
        with open_file(src, 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
        stocks_data += content
    for item in stocks_data:
        code = item['id']
        Products.objects.filter(code=code).update(stock_info=item['stock'])

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--rebuild_catalogue',
            action = 'store_true',
            dest = 'rebuild_catalogue',
            default = False,
            help = 'Drop catalogue structure and recreate it')
        parser.add_argument('--update_products',
            action = 'store_true',
            dest = 'update_products',
            default = False,
            help = 'Update products data')
        parser.add_argument('--drop_products',
            action = 'store_true',
            dest = 'drop_products',
            default = False,
            help = 'Update products data')
        parser.add_argument('--update_stocks',
            action = 'store_true',
            dest = 'update_stocks',
            default = False,
            help = 'Update stocks data')
        parser.add_argument('--cat_id',
            action = 'store',
            dest = 'cat_id',
            type = str,
            default = False,
            help = 'Set cat tag for update')
    def handle(self, *args, **options):

        started = time.time()

        if options.get('drop_products'):
            drop_products()

        if options.get('rebuild_catalogue'):
            rebuild_catalogue()

        if options.get('update_products'):
            update_products()

        if options.get('update_stocks'):
            update_stocks()

        elapsed = time.time() - started
        print('%.2f' % elapsed)

