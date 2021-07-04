#-*- coding:utf-8 -*-
import os
import json
import logging
import datetime
import requests
import xlsxwriter

from requests.auth import HTTPBasicAuth
from openpyxl import load_workbook
from io import BytesIO

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.api_helper import open_wb, search_header, accumulate_data

logger = logging.getLogger(__name__)


def exel2json_old_search_facets(root_folder: str):
    """Преобразуем эксельку в джисонину для работы
       :param root_folder: папка где берем и куда ложим файлы
    """
    wb = open_wb('%ssearch_facets.xlsx' % root_folder)
    sheet = None
    for item in wb:
        if item.title in ('Sheet1', ):
            sheet = item
    if not sheet:
        logger.info('[ERROR]: sheet not found')
        return
    result = []
    rows = list(sheet.rows)
    titles = (
        'rt_id',
        'rt_name',
        'attr_id',
        'attr_name',
    )
    for row in rows[1:]:
        rt = {}
        for i, title in enumerate(titles):
            value = row[i].value
            rt[title] = value
        result.append(rt)
    #print(json_pretty_print(result))
    dest = '%ssearch_facets.json' % root_folder
    with open(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(result))


def exel2json_cls2cat(root_folder: str):
    """Преобразуем эксельку в джисонину для работы
       :param root_folder: папка где берем и куда ложим файлы
    """
    wb = open_wb('%scls2cat.xlsx' % root_folder)
    sheet = None
    for item in wb:
        if item.title in ('Лист 1', ):
            sheet = item
    if not sheet:
        logger.info('[ERROR]: sheet not found')
        return
    result = []
    rows = list(sheet.rows)
    titles = (
        'cat',
        'cls_cat',
        'name',
    )
    for row in rows[2:]:
        rt = {}
        cat_parts = row[0].value.split('-')
        if not cat_parts[-1].isdigit():
            continue
        rt['cat_id'] = cat_parts[-1]

        for i, title in enumerate(titles):
            value = row[i].value
            rt[title] = value
        result.append(rt)
    #print(json_pretty_print(result))
    dest = '%scls2cat.json' % root_folder
    with open(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(result))


def exel2json_classification(root_folder: str):
    """Преобразуем эксельку в джисонину для работы
       :param root_folder: папка где берем и куда ложим файлы
    """
    wb = open_wb('%sclassification.xlsx' % root_folder)
    sheet = None
    for item in wb:
        if item.title in ('Лист 1', ):
            sheet = item
    if not sheet:
        logger.info('[ERROR]: sheet not found')
        return
    result = []
    rows = list(sheet.rows)
    titles = (
        'attr_name',
        'attr_code',
        'name',
        'cls_cat',
    )
    for row in rows[2:]:
        rt = {}
        for i, title in enumerate(titles):
            value = row[i].value
            rt[title] = value
        result.append(rt)

    dest = '%sclassification.json' % root_folder
    with open(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(result))


def exel2json_cls_attrs_assignment(root_folder: str):
    """Преобразуем эксельку в джисонину для работы
       :param root_folder: папка где берем и куда ложим файлы
    """
    wb = open_wb('%scls_attrs_assignment.xlsx' % root_folder)
    sheet = None
    for item in wb:
        if item.title in ('Лист 1', ):
            sheet = item
    if not sheet:
        logger.info('[ERROR]: sheet not found')
        return
    result = []
    rows = list(sheet.rows)
    titles = (
        'attr_name',
        'attr_code',
        'cls_cat',
        'searchable',
    )
    for row in rows[3:]:
        rt = {}
        for i, title in enumerate(titles):
            value = row[i].value
            rt[title] = value
        result.append(rt)
    #print(json_pretty_print(result))
    dest = '%scls_attrs_assignment.json' % root_folder
    with open(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(result))



def load_hier(root_folder: str):
    """Загрузить иерархию
       :param root_folder: папка где берем и куда ложим файлы
    """
    result = {}
    hier_file = '%shier.json' % root_folder
    if os.path.exists(hier_file):
        with open(hier_file, 'r', encoding='utf-8') as f:
            result = json.loads(f.read())
            return {int(k): v for k, v in result.items()}
    urla = 'https://catalog-hierarchy.itlabs.io/api/hierarchy'
    r = requests.get(urla)
    resp = r.json()
    with open(hier_file, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(resp))


def rt2cat_link(root_folder: str):
    """Связать РТ с категорией (по иерархии)
       :param root_folder: папка где берем и куда ложим файлы
    """
    with open('%shier.json' % root_folder, 'r', encoding='utf-8') as f:
        hier = json.loads(f.read())
    result = {}

    def recursive_fill(branches: list):
        for branch in branches:
            if 'branches' in branch:
                recursive_fill(branch['branches'])
            if 'gen_product' in branch:
                rt_id = branch['gen_product']['erp_id']
                if not rt_id in result:
                    result[rt_id] = []
                result[rt_id].append({
                    'name': branch['name'],
                    'cat_id': branch['id'],
                    'rt_id': rt_id,
                    'additional': branch['gen_product']['additional'],
                    'partial': branch['gen_product']['partial'],
                    'parent_id': branch['parent_id'],
                })
    recursive_fill(hier['branches'])
    with open('%srt2cat.json' % root_folder, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(result))

def rt2cat2cls_link(root_folder: str):
    """Собрать РТ, категорию и классификационную категорию в одном месте
       :param root_folder: папка где берем и куда ложим файлы
    """
    with open('%srt2cat.json' % root_folder, 'r', encoding='utf-8') as f:
        rt2cat = json.loads(f.read())
    with open('%scls2cat.json' % root_folder, 'r', encoding='utf-8') as f:
        cls2cat = json.loads(f.read())
    for cat in cls2cat:
        cat_id = int(cat['cat_id'])
        for rt_id, rt in rt2cat.items():
            for rt_cat in rt:
                if rt_cat['cat_id'] == cat_id:
                    cat['rt_id'] = rt_id
    with open('%srt_cat_cls.json' % root_folder, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(cls2cat))

def search_attrs2rt(root_folder: str):
    """Подтянуть все поисковые атрибуты к РТ
       :param root_folder: папка где берем и куда ложим файлы
    """
    with open('%ssearch_facets.json' % root_folder, 'r', encoding='utf-8') as f:
        search_facets = json.loads(f.read())
    with open('%srt_cat_cls.json' % root_folder, 'r', encoding='utf-8') as f:
        rt_cat_cls = json.loads(f.read())
    for search_facet in search_facets:
        for item in rt_cat_cls:
            if not 'rt_id' in item:
                continue
            if item['rt_id'] == search_facet['rt_id']:
                if not 'attrs' in item:
                    item['attrs'] = []
                    item['rt_name'] = search_facet['rt_name']
                item['attrs'].append({
                    'attr_id': search_facet['attr_id'],
                    'attr_name': search_facet['attr_name'],
                    'searchable': True,
                })
    with open('%srt_cat_cls_with_attrs.json' % root_folder, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(rt_cat_cls))


def cls_attrs2rt_link(root_folder: str):
    """Слинковать классификационные атрибуты с атрибутами в РТ
       :param root_folder: папка где берем и куда ложим файлы
    """
    with open('%srt_cat_cls_with_attrs.json' % root_folder, 'r', encoding='utf-8') as f:
        rt_with_attrs = json.loads(f.read())
    with open('%scls_attrs_assignment.json' % root_folder, 'r', encoding='utf-8') as f:
        cls_attrs = json.loads(f.read())

    for rt_attr in rt_with_attrs:
        for cls_attr in cls_attrs:
            if not 'attrs' in rt_attr:
                continue
            if not cls_attr['cls_cat'] == rt_attr['cls_cat']:
                continue

            for attr in rt_attr['attrs']:
                if attr['attr_name'].upper() == cls_attr['attr_name'].upper():
                    if 'attr_code' in attr:
                        print('------------------')
                    attr['attr_code'] = cls_attr['attr_code']

    with open('%sfull_data.json' % root_folder, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(rt_with_attrs))

def create_impex(root_folder: str):
    """Создаем импекс для обновления данных
       :param root_folder: папка где берем и куда ложим файлы

$classificationCatalog = sdClassificationCatalog
$classificationCatalogVersion = catalogVersion(catalog(id[default = $classificationCatalog]), version[default = '1.0'])[default = $classificationCatalog: 1.0]
$classificationSystemVersion = systemVersion(catalog(id[default = $classificationCatalog]), version[default = '1.0'])[default = $classificationCatalog: 1.0]

UPDATE ClassAttributeAssignment	;ClassificationClass(ClassificationClass.code,$classificationCatalogVersion)[unique=true];ClassificationAttribute(code,$classificationSystemVersion)[unique=true];searchable[default=true]
								;cl-l3-shtukaturki                                                                       ;attr-nazvanie                                                          ;True

    """
    result = []
    with open('%sfull_data.json' % root_folder, 'r', encoding='utf-8') as f:
        rt = json.loads(f.read())
    with open('%sclassification.json' % root_folder, 'r', encoding='utf-8') as f:
        attrs = json.loads(f.read())
    for attr in attrs:
        for item in rt:

            if not 'cls_cat' in attr or attr['cls_cat'].startswith('cl-l1') or attr['cls_cat'].startswith('cl-l2'):
                continue

            if not 'attrs' in item or not 'cls_cat' in item:
                continue
            if not item['cls_cat'] == attr['cls_cat']:
                continue

            attr['cat_id'] = item.get('cat_id')
            attr['cat_code'] = item.get('cat')
            attr['cat_name'] = item.get('name')
            attr['rt_id'] = item.get('rt_id')
            attr['rt_name'] = item.get('rt_name')

            for prop in item['attrs']:
                if not 'attr_code' in prop:
                    continue
                if prop['attr_code'] == attr['attr_code']:
                    attr['searchable'] = prop.get('searchable')

            #if attr['cls_cat'] == 'cl-l3-pigmenty-dlja-betona':
            #    print(json_pretty_print(item))
            #    print(json_pretty_print(attr))

    with open('%svera.json' % root_folder, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(attrs))


    dest = '%svera.xlsx' % root_folder
    book = xlsxwriter.Workbook(dest)
    sheet = book.add_worksheet('Лист 1')
    row_number = 0
    sheet.write(row_number, 0, 'Название свойства')
    sheet.write(row_number, 1, 'Код свойства')
    sheet.write(row_number, 2, 'Название свойства')
    sheet.write(row_number, 3, 'Доступно для поиска')
    sheet.write(row_number, 4, 'Код классификационной категории')
    sheet.write(row_number, 5, 'Ид категории')
    sheet.write(row_number, 6, 'Название категории')
    sheet.write(row_number, 7, 'Код категории')
    sheet.write(row_number, 8, 'Ид РТ')
    sheet.write(row_number, 9, 'Название РТ')

    for item in attrs:
        row_number += 1
        searchable = item.get('searchable')
        if searchable:
            searchable = 1
        else:
            searchable = 0
        sheet.write(row_number, 0, item.get('attr_name'))
        sheet.write(row_number, 1, item.get('attr_code'))
        sheet.write(row_number, 2, item.get('name'))
        sheet.write(row_number, 3, searchable)
        sheet.write(row_number, 4, item.get('cls_cat'))
        sheet.write(row_number, 5, item.get('cat_id'))
        sheet.write(row_number, 6, item.get('cat_name'))
        sheet.write(row_number, 7, item.get('cat_code'))
        sheet.write(row_number, 8, item.get('rt_id'))
        sheet.write(row_number, 9, item.get('rt_name'))

        result.append('%s;%s ;%s ;%s' % (
            ' ' * len('UPDATE ClassAttributeAssignment	;'),
            item['cls_cat'],
            item['attr_code'],
            'True' if searchable == 1 else 'False',
        ))
    book.close()

    head = """
$classificationCatalog = sdClassificationCatalog
$classificationCatalogVersion = catalogVersion(catalog(id[default = $classificationCatalog]), version[default = '1.0'])[default = $classificationCatalog: 1.0]
$classificationSystemVersion = systemVersion(catalog(id[default = $classificationCatalog]), version[default = '1.0'])[default = $classificationCatalog: 1.0]

UPDATE ClassAttributeAssignment	;ClassificationClass(ClassificationClass.code,$classificationCatalogVersion)[unique=true];ClassificationAttribute(code,$classificationSystemVersion)[unique=true];searchable[default=true]
"""

    with open('%svera.impex' % root_folder, 'w+', encoding='utf-8') as f:
        f.write(head)
        f.write('\n'.join(result))




class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--start',
            action = 'store',
            dest = 'start',
            type = str,
            default = False,
            help = 'Set start date')
        parser.add_argument('--end',
            action = 'store',
            dest = 'end',
            type = str,
            default = False,
            help = 'Set end date')

    def handle(self, *args, **options):
        """Анализируем поисковые фасеты sdvor.com
        """
        root_folder = '/home/jocker/Documents/HYBRIS/mytasks/vera-search_facets/'
        #exel2json_cls2cat(root_folder)
        #exel2json_old_search_facets(root_folder)
        #exel2json_cls_attrs_assignment(root_folder)
        #exel2json_classification(root_folder)
        #rt2cat_link(root_folder)
        #rt2cat2cls_link(root_folder)
        #search_attrs2rt(root_folder)
        #cls_attrs2rt_link(root_folder)
        create_impex(root_folder)
