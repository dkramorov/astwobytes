#-*- coding:utf-8 -*-
import os
import json
import logging
import datetime
import xml.sax

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count, Q

from apps.telegram.telegram import TelegramBot
from apps.flatcontent.models import Containers, Blocks
from apps.products.models import (
    Products,
    Property,
    PropertiesValues,
    ProductsProperties,
    ProductsCats,
    ProductsPhotos,
)

from apps.main_functions.fortasks import search_process
from apps.main_functions.string_parser import kill_html, kill_quotes
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import (
    ListDir,
    check_path,
    open_file,
    make_folder,
    full_path,
    copy_file,
)

logger = logging.getLogger(__name__)

with_encode = False

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--get_cats',
            action = 'store_true',
            dest = 'get_cats',
            default = False,
            help = 'Get categories')
        parser.add_argument('--get_props',
            action = 'store_true',
            dest = 'get_props',
            default = False,
            help = 'Get properties')
        parser.add_argument('--get_products',
            action = 'store_true',
            dest = 'get_products',
            default = False,
            help = 'Get products')
        parser.add_argument('--import_xml_path',
            action = 'store',
            dest = 'import_xml_path',
            type = str,
            default = False,
            help = 'Set import.xml file path')

        parser.add_argument('--get_prices',
            action = 'store_true',
            dest = 'get_prices',
            default = False,
            help = 'Get prices')
        parser.add_argument('--offers_xml_path',
            action = 'store',
            dest = 'offers_xml_path',
            type = str,
            default = False,
            help = 'Set offers.xml file path')

        parser.add_argument('--with_encode',
            action = 'store_true',
            dest = 'with_encode',
            default = False,
            help = 'Encode to utf-8 for hosting (python 3.4)')

    def handle(self, *args, **options):
        """
python manage.py import_from_1cv8 --get_cats --import_xml_path=exchange_1cv8/all/import0_1.xml --with_encode

python manage.py import_from_1cv8 --get_props --import_xml_path=exchange_1cv8/all/import0_1.xml --with_encode

python manage.py import_from_1cv8 --get_products --import_xml_path=exchange_1cv8/all/import0_1.xml --with_encode

python manage.py import_from_1cv8 --get_prices --offers_xml_path=exchange_1cv8/all/offers0_1.xml --with_encode
        """
        global with_encode
        is_running = search_process(q = ('import_from_1cv8', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            #exit()

        if options.get('with_encode'):
            with_encode = True

        import_xml = 'exchange_1cv8/import0_1.xml'
        if options.get('import_xml_path'):
            import_xml = options['import_xml_path']
        if options.get('get_cats'):
            #for cat in Blocks.objects.filter(container__tag='catalogue'):
            #    cat.save()
            get_cats(import_xml)
        if options.get('get_props'):
            #for prop in Property.objects.all():
            #    prop.delete()
            get_props(import_xml)
        if options.get('get_products'):
            #for product in Products.objects.all():
            #    product.delete()
            get_products(import_xml)

        offers_xml = 'exchange_1cv8/offers0_1.xml'
        if options.get('offers_xml_path'):
            offers_xml = options['offers_xml_path']
        if options.get('get_prices'):
            get_prices(offers_xml)

def get_cats(path: str):
    """Получить каталог по xml выгрузке
       :param path: относительный путь (media) к файлу xml
    """
    with open_file(path, 'r', encoding='utf-8') as f:
        content = f.read()
        if with_encode:
            content = content.encode('utf-8')

    handler = ExchangeCatalogueParser()
    xml.sax.parseString(content, handler)
    if not handler.result:
        print('[ERROR]: %s empty' % path)
        return
    dest = 'catalogue.json'
    #with open_file(dest, 'w+', encoding='utf-8') as f:
    #    f.write(json.dumps(handler.result))
    #print(json_pretty_print(handler.result), len(handler.result))

    result = []
    recursive_fill_cats(handler.result, result, 1)
    #print(json_pretty_print(result))
    catalogue = Containers.objects.filter(tag='catalogue').first()
    recursive_update_cats(result, catalogue)


def recursive_update_cats(result, catalogue, parents=''):
    """Обновление дерева каталога"""
    for item in result:
        analog = Blocks.objects.filter(tag=item['id']).first()
        if not analog:
            analog = Blocks.objects.create(
                name=item['name'],
                tag=item['id'],
                parents=parents,
                container=catalogue,
                state=4,
            )
        if item['sub']:
            new_parents = '%s_%s' % (parents, analog.id)
            recursive_update_cats(item['sub'], catalogue, new_parents)

def recursive_fill_cats(objs, result, lvl, is_root=True):
    parents = []
    parent = None

    for i, obj in enumerate(objs):

        if lvl == obj['level']:
            obj['sub'] = []
            result.append(obj)
        elif lvl == obj['level'] - 1:
            if result[-1]['sub'] and obj in result[-1]['sub']:
                continue
            recursive_fill_cats(objs[i:], result[-1]['sub'], obj['level'], False)
        elif lvl > obj['level']:
            break

class ExchangeCatalogueParser(xml.sax.ContentHandler):
    """Парсер xml выгрузки в файл для 1с v8
       Парсер для каталога
    """
    def __init__(self):
        self.result = []
        self.level = 0
        self.cat_level = 0

        self.root_el_name = 'КоммерческаяИнформация'
        self.in_root_el = False # <КоммерческаяИнформация>

        self.cls_el_name = 'Классификатор'
        self.in_cls_el = False # <Классификатор>

        self.in_groups_el = False
        self.groups_el_name = 'Группы' # 4 уровень и ниже
        self.in_group_el = False
        self.group_el_name = 'Группа' # 5...

        self.id_el_name = 'Ид'
        self.in_id_el = False # <Ид>
        self.id_el_value = ''

        self.name_el_name = 'Наименование'
        self.in_name_el = False # <Наименование>
        self.name_el_value = ''

    def add_cat(self):
        if self.id_el_value and self.name_el_value:
            self.result.append({
                'id': self.id_el_value.strip(),
                'name': self.name_el_value.strip(),
                'level': self.cat_level,
            })
            self.id_el_value = ''
            self.name_el_value = ''

    def startElement(self, name, attributes):
        self.level += 1
        if name == self.root_el_name:
            self.in_root_el = True

        if name == self.cls_el_name:
            self.in_cls_el = True

        # Если группы начинаются, это значит - children
        if name == self.groups_el_name:
            self.add_cat()
            self.cat_level += 1
            self.in_groups_el = True

        # Если группа начинается, это значит тот же уровень
        if name == self.group_el_name:
            self.in_group_el = True

        if name == self.id_el_name:
            self.in_id_el = True

        if name == self.name_el_name:
            self.in_name_el = True

    def characters(self, content):

        if not self.in_cls_el:
            return

        if not self.in_group_el:
            return

        if self.in_id_el:
            self.id_el_value += content

        if self.in_name_el:
            self.name_el_value += content

    def endElement(self, name):
        self.level -= 1
        if name == self.root_el_name:
            self.in_root_el = False

        if name == self.cls_el_name:
            self.in_cls_el = False

        # Если группы заканчиваются, значит, уровень выше смотрим
        if name == self.groups_el_name:
            self.in_groups_el = False
            self.cat_level -= 1

        # Если группа заканчивается, значит, тот же уровень
        if name == self.group_el_name:
            self.add_cat()
            self.in_group_el = False

        if name == self.id_el_name:
            self.in_id_el = False

        if name == self.name_el_name:
            self.in_name_el = False

def get_props(path: str):
    """Получить свойства по xml выгрузке
       :param path: относительный путь (media) к файлу xml
    """
    with open_file(path, 'r', encoding='utf-8') as f:
        content = f.read()
        if with_encode:
            content = content.encode('utf-8')

    handler = ExchangePropsParser()
    xml.sax.parseString(content, handler)
    if not handler.result:
        print('[ERROR]: %s empty' % path)
        return
    dest = 'props.json'
    #with open_file(dest, 'w+', encoding='utf-8') as f:
    #    f.write(json.dumps(handler.result))
    #print(json_pretty_print(handler.result), len(handler.result))
    update_props(handler.result)

def update_props(result):
    """Заполнение свойств товаров"""
    for item in result:
        analog = Property.objects.filter(code=item['id']).first()
        if not analog:
            ptype = None
            if item['type'] == 'Справочник':
                ptype = 2
            analog = Property.objects.create(
                name=item['name'],
                code=item['id'],
                ptype=ptype
            )
        if item['directory']:
            for prop in item['directory']:
                panalog = PropertiesValues.objects.filter(prop=analog, code=prop['id']).first()
                if not panalog:
                    panalog = PropertiesValues.objects.create(
                        prop=analog,
                        code=prop['id'],
                        str_value=prop['value'],
                    )

class ExchangePropsParser(xml.sax.ContentHandler):
    """Парсер xml выгрузки в файл для 1с v8
       Парсер для свойств
    """
    def __init__(self):
        self.result = []
        self.directory = []

        self.root_el_name = 'КоммерческаяИнформация'
        self.in_root_el = False # <КоммерческаяИнформация>

        self.cls_el_name = 'Классификатор'
        self.in_cls_el = False # <Классификатор>

        self.in_props_el = False
        self.props_el_name = 'Свойства'
        self.in_prop_el = False
        self.prop_el_name = 'Свойство'
        self.in_variants_el = False
        self.variants_el_name = 'ВариантыЗначений'
        self.in_directory_el = False
        self.directory_el_name = 'Справочник'

        self.id_el_name = 'Ид'
        self.in_id_el = False # <Ид>
        self.id_el_value = ''

        self.name_el_name = 'Наименование'
        self.in_name_el = False # <Наименование>
        self.name_el_value = ''

        self.type_el_name = 'ТипЗначений'
        self.in_type_el = False # <ТипЗначений>
        self.type_el_value = ''

        self.idvalue_el_name = 'ИдЗначения'
        self.in_idvalue_el = False # <ИдЗначения>
        self.idvalue_el_value = ''

        self.value_el_name = 'Значение'
        self.in_value_el = False # <Значение>
        self.value_el_value = ''

    def startElement(self, name, attributes):
        if name == self.root_el_name:
            self.in_root_el = True

        if name == self.cls_el_name:
            self.in_cls_el = True

        if name == self.props_el_name:
            self.in_props_el = True

        if name == self.prop_el_name:
            self.in_prop_el = True

        if name == self.variants_el_name:
            self.in_variants_el = True

        if name == self.directory_el_name:
            self.in_directory_el = True

        if name == self.id_el_name:
            self.in_id_el = True

        if name == self.name_el_name:
            self.in_name_el = True

        if name == self.type_el_name:
            self.in_type_el = True

        if name == self.idvalue_el_name:
            self.in_idvalue_el = True

        if name == self.value_el_name:
            self.in_value_el = True

    def characters(self, content):

        if not self.in_cls_el:
            return

        if not self.in_props_el:
            return

        if not self.in_prop_el:
            return

        if self.in_id_el:
            self.id_el_value += content

        if self.in_name_el:
            self.name_el_value += content

        if self.in_type_el:
            self.type_el_value += content

        if self.in_idvalue_el:
            self.idvalue_el_value += content

        if self.in_value_el:
            self.value_el_value += content

    def endElement(self, name):
        if name == self.root_el_name:
            self.in_root_el = False

        if name == self.cls_el_name:
            self.in_cls_el = False

        if name == self.props_el_name:
            self.in_props_el = False

        if name == self.prop_el_name:
            self.in_prop_el = False

            self.result.append({
                'id': self.id_el_value,
                'name': self.name_el_value,
                'type': self.type_el_value,
                'directory': self.directory,
            })
            self.id_el_value = ''
            self.name_el_value = ''
            self.type_el_value = ''
            self.directory = []

        if name == self.variants_el_name:
            self.in_variants_el = False

        if name == self.directory_el_name:
            self.in_directory_el = False
            self.directory.append({
                'id': self.idvalue_el_value,
                'value': self.value_el_value,
            })
            self.idvalue_el_value = ''
            self.value_el_value = ''

        if name == self.id_el_name:
            self.in_id_el = False

        if name == self.name_el_name:
            self.in_name_el = False

        if name == self.type_el_name:
            self.in_type_el = False

        if name == self.idvalue_el_name:
            self.in_idvalue_el = False

        if name == self.value_el_name:
            self.in_value_el = False

def get_products(path: str):
    """Получить товары по xml выгрузке
       :param path: относительный путь (media) к файлу xml
    """
    with open_file(path, 'r', encoding='utf-8') as f:
        content = f.read()
        if with_encode:
            content = content.encode('utf-8')

    handler = ExchangeProductsParser()
    xml.sax.parseString(content, handler)
    if not handler.result:
        print('[ERROR]: %s empty' % path)
        return
    dest = 'products.json'
    #with open_file(dest, 'w+', encoding='utf-8') as f:
    #    f.write(json.dumps(handler.result))
    #print(json_pretty_print(handler.result), len(handler.result))
    update_products(handler.result)


def update_products(result):
    """Заполнение товаров"""
    catalogue = Containers.objects.filter(tag='catalogue').first()
    for item in result:
        analog = Products.objects.filter(code=item['id']).first()
        if not analog:
            analog = Products.objects.create(
                name=item['name'],
                code=item['id'],
                manufacturer=item.get('brand'),
                mini_info=item['desc'],
                altname=item['article'],
            )
        for group in item['groups']:
            cat = Blocks.objects.filter(tag=group).first()
            if not cat:
                print('cat not found with tag %s' % group)
                continue
            ganalog = analog.productscats_set.filter(cat=cat).first()
            if not ganalog:
                ganalog = ProductsCats.objects.create(
                    container=catalogue,
                    product=analog,
                    cat=cat,
                )
        for prop in item['props']:
            if not prop['value'] or len(prop['value']) > 150:
                continue
            panalog = Property.objects.filter(code=prop['id']).first()
            if not panalog:
                print('property not found with prop %s' % prop)
                continue

            pvalue = panalog.propertiesvalues_set.filter(Q(code=prop['value'])|Q(str_value=prop['value'])).first()
            if not pvalue:
                print('pvalue not found with prop %s' % prop)
                pvalue = PropertiesValues.objects.create(
                    prop=panalog,
                    str_value = prop['value'],
                )
            vanalog = ProductsProperties.objects.filter(prop=pvalue, product=analog).first()
            if not vanalog:
                vanalog = ProductsProperties.objects.create(
                    prop=pvalue,
                    product=analog,
                )
        if not analog.img:
            for i, image in enumerate(item['images']):
                src = 'exchange_1cv8/picture/%s' % image
                if i == 0:
                    fname = '%s.%s' % (analog.id, src.split('.')[-1])
                    dest = os.path.join(analog.get_folder(), fname)
                    copy_file(src, dest)
                    Products.objects.filter(pk=analog.id).update(img=fname)
                else:
                    fname = '%s.%s' % (i, src.split('.')[-1])
                    photo = ProductsPhotos.objects.create(
                        product=analog,
                        img=fname,
                    )
                    dest = os.path.join(photo.get_folder(), fname)
                    copy_file(src, dest)

class ExchangeProductsParser(xml.sax.ContentHandler):
    """Парсер xml выгрузки в файл для 1с v8
       Парсер для товаров
    """
    def __init__(self):
        self.result = []
        self.product = {
            'groups': [],
            'images': [],
            'props': [],
        }
        self.level = 0
        self.product_level = 0

        self.root_el_name = 'КоммерческаяИнформация'
        self.in_root_el = False # <КоммерческаяИнформация>

        self.cat_el_name = 'Каталог'
        self.in_cat_el = False # <Каталог>

        self.in_products_el = False
        self.products_el_name = 'Товары'
        self.in_product_el = False
        self.product_el_name = 'Товар'

        self.id_el_name = 'Ид'
        self.in_id_el = False # <Ид>
        self.id_el_value = ''

        self.article_el_name = 'Артикул'
        self.in_article_el = False # <Артикул>
        self.article_el_value = ''

        self.groups_el_name = 'Группы'
        self.in_groups_el = False # <Группы>

        self.name_el_name = 'Наименование'
        self.in_name_el = False # <Наименование>
        self.name_el_value = ''

        self.desc_el_name = 'Описание'
        self.in_desc_el = False # <Описание>
        self.desc_el_value = '';

        self.img_el_name = 'Картинка'
        self.in_img_el = False # <Картинка>
        self.img_el_value = '';

        self.props_el_name = 'ЗначенияСвойств'
        self.in_props_el = False # <ЗначенияСвойств>
        self.prop_el_name = 'ЗначенияСвойства'
        self.in_prop_el = False # <ЗначенияСвойства>

        self.brand_el_name = 'Изготовитель'
        self.in_brand_el = False # <Изготовитель>

        self.value_el_name = 'Значение'
        self.in_value_el = False # <Значение>
        self.value_el_value = ''

    def startElement(self, name, attributes):
        self.level += 1
        if name == self.root_el_name:
            self.in_root_el = True

        if name == self.cat_el_name:
            self.in_cat_el = True

        if name == self.products_el_name:
            self.in_products_el = True

        if name == self.product_el_name:
            self.in_product_el = True
            if not self.product_level:
                self.product_level = self.level

        if name == self.id_el_name:
            self.in_id_el = True

        if name == self.desc_el_name:
            self.in_desc_el = True

        if name == self.article_el_name:
            self.in_article_el = True

        if name == self.groups_el_name:
            self.in_groups_el = True

        if name == self.name_el_name:
            self.in_name_el = True

        if name == self.img_el_name:
            self.in_img_el = True

        if name == self.props_el_name:
            self.in_props_el = True

        if name == self.prop_el_name:
            self.in_prop_el = True

        if name == self.value_el_name:
            self.in_value_el = True

        if name == self.brand_el_name:
            self.in_brand_el = True

    def characters(self, content):

        if not self.in_cat_el:
            return

        if not self.in_products_el:
            return

        if not self.in_product_el:
            return

        if self.in_id_el:
            self.id_el_value += content

        if self.in_article_el:
            self.article_el_value += content

        if self.in_name_el:
            self.name_el_value += content

        if self.in_desc_el:
            self.desc_el_value += content

        if self.in_img_el:
            self.img_el_value += content

        if self.in_value_el:
            self.value_el_value += content

    def endElement(self, name):
        self.level -= 1
        if name == self.root_el_name:
            self.in_root_el = False

        if name == self.cat_el_name:
            self.in_cat_el = False

        if name == self.products_el_name:
            self.in_products_el = False

        if name == self.product_el_name:
            self.in_product_el = False

            self.result.append(self.product)
            self.product = {
                'groups': [],
                'images': [],
                'props': [],
            }

        if name == self.id_el_name:
            self.in_id_el = False
            if self.in_groups_el and self.level == self.product_level + 1:
                self.product['groups'].append(self.id_el_value)
            elif self.level == self.product_level:
                self.product['id'] = self.id_el_value
            # Не чистим если в свойстве, почистим, когда закончится
            if self.in_prop_el:
                return
            self.id_el_value = ''

        if name == self.article_el_name:
            self.in_article_el = False
            if self.level == self.product_level:
                self.product['article'] = self.article_el_value
            self.article_el_value = ''

        if name == self.groups_el_name:
            self.in_groups_el = False

        if name == self.name_el_name:
            self.in_name_el = False
            if self.level == self.product_level:
                self.product['name'] = self.name_el_value
            elif self.in_brand_el:
                self.product['brand'] = self.name_el_value
            self.name_el_value = ''

        if name == self.desc_el_name:
            self.in_desc_el = False
            if self.level == self.product_level:
                self.product['desc'] = self.desc_el_value
            self.desc_el_value = ''

        if name == self.img_el_name:
            self.in_img_el = False
            if self.level == self.product_level:
                self.product['images'].append(self.img_el_value)
            self.img_el_value = ''

        if name == self.props_el_name:
            self.in_props_el = False

        if name == self.prop_el_name:
            self.in_prop_el = False
            self.product['props'].append({
                'id': self.id_el_value,
                'value': self.value_el_value,
            });
            self.id_el_value = ''
            self.value_el_value = ''

        if name == self.value_el_name:
            self.in_value_el = False
            # Не чистим если в свойстве, почистим, когда закончится
            if self.in_prop_el:
                return
            self.value_el_value = ''

        if name == self.brand_el_name:
            self.in_brand_el = False

def get_prices(path: str):
    """Получить цены по xml выгрузке
       :param path: относительный путь (media) к файлу xml
    """
    with open_file(path, 'r', encoding='utf-8') as f:
        content = f.read()
        if with_encode:
            content = content.encode('utf-8')

    handler = ExchangePricesParser()
    xml.sax.parseString(content, handler)
    if not handler.result:
        print('[ERROR]: %s empty' % path)
        return
    dest = 'prices.json'
    #with open_file(dest, 'w+', encoding='utf-8') as f:
    #    f.write(json.dumps(handler.result))
    #print(json_pretty_print(handler.result), len(handler.result))
    update_prices(handler.result)

def update_prices(result):
    """Заполнение цен/остатков"""
    for item in result:
        analog = Products.objects.filter(code=item['id']).first()
        if not analog:
            print('not found product for %s' % item)
            continue
        Products.objects.filter(pk=analog.id).update(
            price=item['price'],
            count=int(float(item['count'])) if item['count'] else 0,
            measure=item.get('unit'),
        )

class ExchangePricesParser(xml.sax.ContentHandler):
    """Парсер xml выгрузки в файл для 1с v8
       Парсер для цен и остатков
    """
    def __init__(self):
        self.result = []

        self.root_el_name = 'КоммерческаяИнформация'
        self.in_root_el = False # <КоммерческаяИнформация>

        self.cat_el_name = 'ПакетПредложений'
        self.in_cat_el = False # <ПакетПредложений>

        self.in_offers_el = False
        self.offers_el_name = 'Предложения'
        self.in_offer_el = False
        self.offer_el_name = 'Предложение'

        self.id_el_name = 'Ид'
        self.in_id_el = False # <Ид>
        self.id_el_value = ''

        self.prices_el_name = 'Цены'
        self.in_prices_el = False # <Цены>
        self.price_el_name = 'Цена'
        self.in_price_el = False # <Цена>
        self.cost_el_name = 'ЦенаЗаЕдиницу'
        self.in_cost_el = False # <ЦенаЗаЕдиницу>
        self.cost_el_value = ''

        self.unit_el_name = 'БазоваяЕдиница'
        self.in_unit_el = False # <БазоваяЕдиница>
        self.unit_el_value = ''

        self.count_el_name = 'Количество'
        self.in_count_el = False # <Количество>
        self.count_el_value = ''


    def startElement(self, name, attributes):
        if name == self.root_el_name:
            self.in_root_el = True

        if name == self.cat_el_name:
            self.in_cat_el = True

        if name == self.offers_el_name:
            self.in_offers_el = True

        if name == self.offer_el_name:
            self.in_offer_el = True

        if name == self.id_el_name:
            self.in_id_el = True

        if name == self.count_el_name:
            self.in_count_el = True

        if name == self.cost_el_name:
            self.in_cost_el = True

        if name == self.unit_el_name:
            self.unit_el_value = attributes.get('НаименованиеПолное')

    def characters(self, content):

        if not self.in_cat_el:
            return

        if not self.in_offers_el:
            return

        if not self.in_offer_el:
            return

        if self.in_count_el:
            self.count_el_value += content

        if self.in_cost_el:
            self.cost_el_value += content

        if self.in_id_el:
            self.id_el_value += content

        if self.in_unit_el:
            self.unit_el_value += content

    def endElement(self, name):
        if name == self.root_el_name:
            self.in_root_el = False

        if name == self.cat_el_name:
            self.in_cat_el = False

        if name == self.offers_el_name:
            self.in_offers_el = False

        if name == self.offer_el_name:
            self.in_offer_el = False
            self.result.append({
                'id': self.id_el_value,
                'price': self.cost_el_value,
                'count': self.count_el_value,
                'unit': self.unit_el_value,
            })
            self.id_el_value = ''
            self.count_el_value = ''
            self.cost_el_value = ''
            self.unit_el_value = ''

        if name == self.id_el_name:
            self.in_id_el = False

        if name == self.count_el_name:
            self.in_count_el = False

        if name == self.cost_el_name:
            self.in_cost_el = False

        if name == self.unit_el_name:
            self.in_unit_el = False
