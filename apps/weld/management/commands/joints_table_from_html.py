# -*- coding: utf-8 -*-
import os
import logging
import re

import xlsxwriter
import io

from django.core.management.base import BaseCommand
from django.conf import settings

from lxml import html as lxml_html

from apps.main_functions.files import open_file, ListDir, full_path

logger = logging.getLogger(__name__)

def accumulate_result(table, name):
    """Парсинг хтмл таблицы (lxml)
       № п/п (0), № стыка(1), Клеймо(2), Материал(3),
       Диаметр,мм(4), Толщина,мм(4), Дата(5)
       :param table: таблица lxml
    """
    result = []
    trs = table.xpath('.//tbody/tr')
    for tr in trs:
        joint = {'file': name}
        tds = tr.xpath('.//td')
        number_p = tds[0].xpath('.//p')
        number_joint = tds[1].xpath('.//p')
        stigma = tds[2].xpath('.//p')
        material = tds[3].xpath('.//p')
        size = tds[4].xpath('.//p')
        date = tds[5].xpath('.//p')
        welding_type = tds[6].xpath('.//p')
        if number_p:
            joint['n'] = number_p[0].text
        if number_joint:
            parts = number_joint[0].text.split(' ')
            number_joint = parts[0]
            joint['number'] = number_joint
            conn_view = parts[1]
            joint['conn_view'] = conn_view
        if stigma:
            stigma = stigma[0].text
            stigma = stigma.split(' ')[-1]
            joint['stigma'] = stigma
        if material:
            joint['material'] = material[0].text
        if size:
            cur_size = None
            elements = []
            for item in size:
                text = item.text.replace('-', ' ').replace('х', 'x')
                sarr = text.split(' ')
                for part in sarr:
                    if 'x' in part:
                        cur_size = part
                    else:
                        if len(part) >= 5:
                            elements.append(part)
            joint['elements'] = elements
            if cur_size:
                joint['size'] = cur_size
        if date:
            joint['date'] = date[0].text
        if welding_type:
            joint['welding_type'] = welding_type[0].text
        result.append(joint)
    return result

class Command(BaseCommand):
    def handle(self, *args, **options):
        html_path = 'mammoth'
        html_files = ListDir(html_path)
        result = []
        for html_file in html_files:
            if not html_file.endswith('.html'):
                continue
            cur_html = os.path.join(html_path, html_file)
            content = ''
            with open_file(cur_html, 'r') as f:
                content = f.read()
            tree = lxml_html.fromstring(content)
            tables = tree.xpath('//table')
            for table in tables:
                ths = table.xpath('.//thead/tr/th/p')
                if ths:
                    th = ths[0]
                    if '№ п/п' in th.text:
                        result += accumulate_result(table, html_file.replace('.html', ''))

        dest = full_path('joint_table_from_html.xlsx')
        book = xlsxwriter.Workbook(dest)
        sheet = book.add_worksheet('Лист 1')
        row_number = 0
        sheet.write(row_number, 0, 'Файл')
        sheet.write(row_number, 1, '№ п/п')
        sheet.write(row_number, 2, '№ стыка')
        sheet.write(row_number, 3, 'Клеймо')
        sheet.write(row_number, 4, 'Материал')
        sheet.write(row_number, 5, 'Диаметр,мм')
        sheet.write(row_number, 6, 'Толщина,мм')
        sheet.write(row_number, 7, 'Дата')
        sheet.write(row_number, 8, 'Тип сварки')
        sheet.write(row_number, 9, 'Вид соединения')
        sheet.write(row_number, 10, 'Соединение')
        for item in result:
            row_number += 1
            size = item.get('size', 'x').split('/')[0]
            sizes = size.split('x')
            diameter = sizes[0]
            side_thickness = sizes[1]
            sheet.write(row_number, 0, item.get('file'))
            sheet.write(row_number, 1, item.get('n'))
            sheet.write(row_number, 2, item.get('number'))
            sheet.write(row_number, 3, item.get('stigma'))
            sheet.write(row_number, 4, item.get('material'))
            sheet.write(row_number, 5, diameter)
            sheet.write(row_number, 6, side_thickness)
            sheet.write(row_number, 7, item.get('date'))
            sheet.write(row_number, 8, item.get('welding_type'))
            sheet.write(row_number, 9, item.get('conn_view'))
            sheet.write(row_number, 10, ' - '.join(item.get('elements', [])))

        book.close()
