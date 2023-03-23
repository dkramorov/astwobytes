#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count
from django.db import connections

from apps.main_functions.catcher import json_pretty_print
from apps.products.models import Products, ProductsCats, ProductsPhotos, Property, PropertiesValues, ProductsProperties
from apps.flatcontent.models import Containers, Blocks

# Сериализация/десериализация объекта
import phpserialize

logger = logging.getLogger('main')
CRM_DB = 'vallomcrm'


class CRMAbstract:
    def get_count_query(self, table: str):
        return 'select count(id) from %s' % table

    def get_query(self, table: str, fields: list,
                  limit: int = 10, offset: int = 0, order_by: str = 'id'):
        """Запрос в базень"""
        query = 'SELECT %s FROM %s' % (','.join(fields), table)
        if order_by:
            query += ' ORDER BY %s' % order_by
        if limit:
            query += ' LIMIT %s' % limit
        if offset:
            query += ' OFFSET %s' % offset
        return query

    def rows2dict(self, fields: list, rows: list):
        """Получение из базени полей словарем"""
        result = {}
        for row in rows:
            item = {field_name: None for field_name in fields}
            for i, value in enumerate(row):
                field_name = fields[i]
                item[field_name] = value
            result[item['id']] = item
        return result

class CRMCatalogue(CRMAbstract):
    table = 'product_categories'
    fields = (
        'id',
        'pid', # parent_id
        'name', 'link',
        'base_markup',
        'sort_order',
        'blocked',
        'table_id',
    )

class CRMProperties(CRMAbstract):
    table = 'product_categories_char'
    fields = (
        'id',
        'name',
        'sys_name',
        'type',
        'cat_id',
        'in_filter',
        'in_short_card',
        'in_full_card',
    )

class CRMChars(CRMAbstract):
    table = 'product_categories_char_values'
    fields = (
        'id',
        'char_id',
        'name',
        'value',
    )

class CRMProductsChars(CRMAbstract):
    table = 'products_characteristics'
    fields = (
        'id',
        'product_id',
        'char_id',
        'value',
    )

class CRMProducts(CRMAbstract):
    table = 'products'
    fields = (
        'id', 'name', 'oem', 'brand',
        'cat_id',
        'quantity', 'price', 'price_total',
        'lot_id', 'autolot_id', 'additional_lots',
        'description',
        'images', 'images_from_lot',
        'repairs_markup',
        'to_drom', 'to_avito', 'to_japancar', 'to_vk', 'to_2gis', 'upload2drom_year',
        'avito_category', 'avito_subcategory', 'model_avito',
        'store_id',
        'updated',
        'is_calculated',
        'comments',
        'sticker_count',
        'flag',
        'address_id',
        'is_personal',
        'is_new',
        'frozen_price',
        'video_link',
        'custom_id',
    )

def load_categories():
    """Подгружаем все рубрики"""
    catalogue = Containers.objects.filter(tag='catalogue', state=7).first()
    crm_catalogue = CRMCatalogue()
    with connections[CRM_DB].cursor() as cursor:
        cursor.execute(crm_catalogue.get_count_query(table=crm_catalogue.table))
        rows = cursor.fetchall()[0]
        logger.info('total categories in CRM %s' % rows)
        by = 100
        total_pages = int(rows[0] / by) + 1
        logger.info('total categories pages %s, by %s' % (total_pages, by))
        for i in range(total_pages):
            query = crm_catalogue.get_query(table=crm_catalogue.table, fields=crm_catalogue.fields, limit=by, offset=i*by)
            cursor.execute(query)
            rows = cursor.fetchall()
            categories = crm_catalogue.rows2dict(fields=crm_catalogue.fields, rows=rows)
            #logger.info(json_pretty_print(categories))
            # Находим аналоги в базе
            # TODO: находить не встретившиеся -------------------------- и удалять
            ids = categories.keys()
            if not ids:
                break
            analogs = Blocks.objects.filter(tag__in=ids, container=catalogue, state=4)
            catalogue_map = {
                analog.tag: analog for analog in analogs
            }
            for cat_id, cat in categories.items():
                instance = Blocks(tag=cat_id, container=catalogue, state=4)
                tag = str(cat_id)
                if tag in catalogue_map:
                    instance = catalogue_map[tag]

                # TODO: проверять, что были изменения перед сохранением
                instance.name = cat['name']
                if cat['pid']:
                    parent = Blocks.objects.filter(tag=cat['pid'], container=catalogue, state=4).first()
                    if not parent:
                        logger.error('Catalogue parent not found for %s' % json_pretty_print(cat))
                        continue
                    instance.parents = '%s_%s' % (parent.parents, parent.id)
                instance.save()

def load_products():
    """Подгружаем все товары"""
    catalogue = Containers.objects.filter(tag='catalogue', state=7).first()
    cats =  catalogue.blocks_set.all()
    cats_mapping = {
        cat.tag: cat for cat in cats
    }
    crm_products = CRMProducts()
    with connections[CRM_DB].cursor() as cursor:
        cursor.execute(crm_products.get_count_query(table=crm_products.table))
        rows = cursor.fetchall()[0]
        logger.info('total products in CRM %s' % rows)
        by = 500
        total_pages = int(rows[0] / by) + 1
        logger.info('total products pages %s, by %s' % (total_pages, by))
        for i in range(total_pages):
            logger.info('processing %s / %s' % (i, total_pages))
            query = crm_products.get_query(table=crm_products.table, fields=crm_products.fields, limit=by, offset=i*by)
            cursor.execute(query)
            rows = cursor.fetchall()
            products = crm_products.rows2dict(fields=crm_products.fields, rows=rows)
            #logger.info(json_pretty_print(products))
            # Находим аналоги в базе
            # TODO: находить не встретившиеся -------------------------- и удалять
            ids = products.keys()
            if not ids:
                break
            analogs = Products.objects.filter(pk__in=ids)
            products_map = {
                analog.id: analog for analog in analogs
            }
            for product_id, product in products.items():
                instance = Products(id=product_id)
                if product_id in products_map:
                    instance = products_map[product_id]
                # TODO: проверять, что были изменения перед сохранением
                instance.name = product['name']
                instance.code = product['custom_id'] or product['id']
                instance.manufacturer = product['brand']
                instance.count = product['quantity']
                instance.price = product['price_total']
                instance.info = product['description']
                instance.code = product['custom_id'] or product_id
                instance.is_active = False
                if instance.count and instance.count > 0:
                    instance.is_active = True
                instance.save()
                # Категория товара
                cat_id = str(product['cat_id'])
                if cat_id in cats_mapping:
                    cat = cats_mapping[cat_id]
                    cat_link = ProductsCats.objects.filter(product=instance, cat=cat, container=catalogue).first()
                    if not cat_link:
                        ProductsCats.objects.create(product=instance, cat=cat, container=catalogue)
                # Изображения
                lot_id = None
                if product['images_from_lot'] == 1:
                    lot_id = product['lot_id']
                images = get_images(product['images'], lot_id=lot_id)
                if not images:
                    Products.objects.filter(pk=instance.id).update(is_active=False)
                for  i in range(len(images)):
                    if i == 0:
                        Products.objects.filter(pk=instance.id).update(img='/products/%s' % images[i])
                        continue
                    photos = ProductsPhotos.objects.filter(product=instance).values_list('name', flat=True)
                    if images[i] in photos:
                        continue
                    ProductsPhotos.objects.create(product=instance, name=images[i], img='/products/%s' % images[i])

def load_properties():
    """Подгружаем свойства товаров"""
    catalogue = Containers.objects.filter(tag='catalogue', state=7).first()
    cats =  catalogue.blocks_set.all()
    cats_mapping = {
        cat.tag: cat for cat in cats
    }

    crm_properties = CRMProperties()
    with connections[CRM_DB].cursor() as cursor:
        cursor.execute(crm_properties.get_count_query(table=crm_properties.table))
        rows = cursor.fetchall()[0]
        logger.info('total properties in CRM %s' % rows)
        by = 500
        total_pages = int(rows[0] / by) + 1
        logger.info('total properties pages %s, by %s' % (total_pages, by))
        for i in range(total_pages):
            logger.info('processing %s / %s' % (i, total_pages))
            query = crm_properties.get_query(table=crm_properties.table, fields=crm_properties.fields, limit=by, offset=i*by)
            cursor.execute(query)
            rows = cursor.fetchall()
            props = crm_properties.rows2dict(fields=crm_properties.fields, rows=rows)
            ids = props.keys()
            if not ids:
                break
            analogs = Property.objects.filter(pk__in=ids)
            props_map = {
                analog.id: analog for analog in analogs
            }
            for prop_id, prop in props.items():
                instance = Property(id=prop_id)
                if prop_id in props_map:
                    instance = props_map[prop_id]
                # TODO: проверять, что были изменения перед сохранением
                instance.name = prop['name']
                instance.code = prop['sys_name'] or prop['id']
                if prop['type'] == 'select':
                    instance.ptype = 1
                elif prop['type'] == 'multiselect':
                    instance.ptype = 2
                elif prop['type'] == 'radio':
                    instance.ptype = 3
                elif prop['type'] == 'text':
                    instance.ptype = 5
                else:
                    print('absent category for prop', json_pretty_print(prop))
                    continue
                # Категория товара
                cat_id = str(prop['cat_id'])
                if cat_id in cats_mapping:
                    cat = cats_mapping[cat_id]
                    instance.cat = cat
                else:
                    assert False
                instance.save()

    crm_chars = CRMChars()
    with connections[CRM_DB].cursor() as cursor:
        cursor.execute(crm_chars.get_count_query(table=crm_chars.table))
        rows = cursor.fetchall()[0]
        logger.info('total chars in CRM %s' % rows)
        by = 500
        total_pages = int(rows[0] / by) + 1
        logger.info('total chars pages %s, by %s' % (total_pages, by))
        for i in range(total_pages):
            logger.info('processing %s / %s' % (i, total_pages))
            query = crm_chars.get_query(table=crm_chars.table, fields=crm_chars.fields, limit=by, offset=i*by)
            cursor.execute(query)
            rows = cursor.fetchall()
            chars = crm_chars.rows2dict(fields=crm_chars.fields, rows=rows)
            ids = chars.keys()
            if not ids:
                break
            analogs = PropertiesValues.objects.filter(pk__in=ids)
            chars_map = {
                analog.id: analog for analog in analogs
            }
            for char_id, char in chars.items():
                #if not char['char_id'] == 33:
                #    continue
                #print(char)

                prop = Property.objects.filter(pk=char['char_id']).first()
                if not prop:
                    print('prop does not exists for char', json_pretty_print(char))
                    continue
                instance = PropertiesValues(id=char_id, prop=prop)
                if char_id in chars_map:
                    instance = chars_map[char_id]
                # TODO: проверять, что были изменения перед сохранением
                instance.str_value = char['name']
                instance.code = char['value'] or char['name']
                instance.save()

def load_products_links():
    """Подгружаем свойства товаров (линковки)"""
    crm_product_chars = CRMProductsChars()
    with connections[CRM_DB].cursor() as cursor:
        cursor.execute(crm_product_chars.get_count_query(table=crm_product_chars.table))
        rows = cursor.fetchall()[0]
        logger.info('total product chars in CRM %s' % rows)
        by = 500
        total_pages = int(rows[0] / by) + 1
        logger.info('total product pages %s, by %s' % (total_pages, by))
        for i in range(total_pages):
            logger.info('processing %s / %s' % (i, total_pages))
            query = crm_product_chars.get_query(table=crm_product_chars.table, fields=crm_product_chars.fields, limit=by, offset=i*by)
            cursor.execute(query)
            rows = cursor.fetchall()
            chars = crm_product_chars.rows2dict(fields=crm_product_chars.fields, rows=rows)
            for char_id, char in chars.items():
                print(char)
                if not char['value'] or len(char['value']) > 100:
                    print('empty value for cahr', json_pretty_print(char))
                    continue
                product = Products.objects.filter(pk=char['product_id']).first()
                if not product:
                    print('product does not exists for char', json_pretty_print(char))
                    continue
                prop = Property.objects.filter(pk=char['char_id']).first()
                if not prop:
                    print('prop does not exists for char', json_pretty_print(char))
                    continue
                if prop.ptype == 5:
                    # Это текстом, нужно проверить или завести значение свойства
                    pvalue = PropertiesValues.objects.filter(code=char['value'], prop=prop).first()
                    if not pvalue:
                        pvalue = PropertiesValues.objects.create(code=char['value'], prop=prop, str_value=char['value'])
                    analog = ProductsProperties.objects.filter(product=product, prop=pvalue)
                    if not analog:
                        ProductsProperties.objects.create(product=product, prop=pvalue)
                else:
                    # Такие должны уже существовать значения свойств
                    pvalue_ids = [char['value']]
                    if prop.ptype == 2 or ',' in char['value']:
                        pvalue_ids = char['value'].split(',')
                    for pvalue_id in pvalue_ids:
                        pvalue = PropertiesValues.objects.filter(pk=pvalue_id).first()
                        if not pvalue:
                            print('pvalue does not exists for char', json_pretty_print(char))
                            continue
                        analog = ProductsProperties.objects.filter(product=product, prop=pvalue)
                        if not analog:
                            ProductsProperties.objects.create(product=product, prop=pvalue)


def get_images(voca: dict, lot_id: int = None):
    """Фотографии товара
       Если передавать lot_id подтягиваем фото лота
    """
    if not voca:
        return []
    lot_images = []
    bytes_text = bytes(voca, 'utf-8')
    items = phpserialize.loads(bytes_text)
    images = [x[1].decode('utf-8') for x in sorted(items.items())]
    if lot_id:
        lot_images = get_lot_images(lot_id)
    result = images + lot_images
    return [item for item in result if not 'jsmnew.doko.link' in item]

def get_lot_images(lot_id: int):
    """Фотографии лота"""
    with connections[CRM_DB].cursor() as cursor:
        cursor.execute('select images from lots where id=%s' % lot_id)
        rows = cursor.fetchall()

    def object_hook(name, d):
        class stdClass(object):
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
        d = phpserialize.convert_member_dict(d)
        obj = {}
        for k, v in d.items():
            if not isinstance(v, bytes):
                continue
            #print(k, v)
            obj[k.decode('utf-8')] = v.decode('utf-8')
        return stdClass(**obj)

    bytes_text = bytes(rows[0][0], 'utf-8')
    result = phpserialize.loads(bytes_text, object_hook=object_hook)
    if not result:
        return []
    return [x[1].link for x in sorted(result.items())]

class Command(BaseCommand):
    """Работа с товарами CRM
       ln -s /Users/jocker/django/SITES/vallomcrm/media/products media/
       ln -s /home/v/vallom/vallomsu/public_html/vallomcrm/media/products media/
    """
    def add_arguments(self, parser):
        parser.add_argument('--folder',
            action = 'store',
            dest = 'folder',
            type = str,
            default = False,
            help = 'Set folder with spinner files')
        parser.add_argument('--catalogue',
            action = 'store_true',
            dest = 'catalogue',
            default = False,
            help = 'Load catalogue')
        parser.add_argument('--products',
            action = 'store_true',
            dest = 'products',
            default = False,
            help = 'Load products')
        parser.add_argument('--properties',
            action = 'store_true',
            dest = 'properties',
            default = False,
            help = 'Load properties')
        parser.add_argument('--products_links',
            action = 'store_true',
            dest = 'products_links',
            default = False,
            help = 'Load products links')
    def handle(self, *args, **options):
        if options.get('catalogue'):
            load_categories()
        if options.get('products'):
            load_products()
        #print(get_lot_images(6012)) # 6012 5932 5603 4640
        if options.get('properties'):
            load_properties()
        if options.get('products_links'):
            load_products_links()

