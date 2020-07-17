# -*- coding: utf-8 -*-
import logging

from openpyxl import load_workbook
from io import BytesIO

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from django.conf import settings

from apps.main_functions.date_time import str_to_date
from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.files import open_file, full_path
from apps.weld.models import (WeldingJoint,
                              Base,
                              Contract,
                              Titul,
                              Line,
                              Scheme,
                              Joint,
                              Material,
                              JoinType,
                              Welder,
                              JointWelder, )

logger = logging.getLogger(__name__)

# Файлы excel для анализа
daily_report_weldings = 'daily_report_weldings.xlsx'
statement_joints = 'statement_joints.xlsx'

def open_wb(path):
    """Загружаем книжку
       :param path: путь до эксельки
    """
    with open_file(path, 'rb') as excel_file:
        wb = load_workbook(BytesIO(excel_file.read()))
    logger.info(wb.sheetnames)
    return wb

def search_header(rows):
    """Поиск строки заголовков
       обход по генератору
       :param rows: генератор для строк
    """
    for row in rows:
        i = 0
        for cell in row:
            value = cell.value
            if value and '№' in value:
                return i, row
            i += 1
    return None, None

def accumulate_data(row, i, data):
    """Добавление ячейки в массив данных
       :param row: строка эксельки
       :param i: номер ячейки в строке эксельки
       :param data: массив данных
    """
    value = row[i].value
    if value:
        value = '%s' % value
        value = value.strip()
        if value and not value in data:
            data.append(value)
    return value

def analyze_statement_joints():
    """Заполнение базы уникальными значениями из эксельки"""
    wb = open_wb(statement_joints)
    sheet = None
    for item in wb:
        if item.title in ('Новые стыки', ):
            sheet = item
    if not sheet:
        logger.info('[ERROR]: sheet not found')
        return

    rows = sheet.rows
    i, header = search_header(rows)
    if header is None:
        logger.info('[ERROR]: header not found')


    bases = []
    contracts = []
    lines = []
    schemes = []
    joints = []
    materials = []
    join_types = []
    workshifts = []
    welders = []
    control_types = []
    conn_types_views = []
    welding_types = []
    categories = []
    control_results = []
    welding_joints = []
    for row in rows: # Продолжаем обход по генератору
        cell_values = [cell.value for cell in row]
        if not any(cell_values):
            logger.info('EOF reached')
            break

        # Установка это i+1 ячейка
        base = accumulate_data(row, i+1, bases)
        # Договор это i+2 ячейка
        contract = accumulate_data(row, i+2, contracts)
        # Линия это i+3 ячейка
        line = accumulate_data(row, i+3, lines)
        # № Изометрической схемы это i+4 ячейка
        scheme = accumulate_data(row, i+4, schemes)
        # № стыка это i+5 ячейка
        joint = row[i+5].value
        if joint and line:
            joint = '%s' % joint
            joint = joint.strip()
            if joint and not joint in joints:
                joints.append((joint, line))
        # материал (сталь) это i+11 ячейка
        material = accumulate_data(row, i+11, materials)
        # свариваемые элементы это i+12 ячейка
        join_type = accumulate_data(row, i+12, join_types)
        # смена это i+14 ячейка
        workshift = accumulate_data(row, i+14, workshifts)
        welder = row[i+15].value # имя сварщика это i+15 ячейка
        stigma = row[i+16].value # клеймо сварщика это i+16 ячейка
        if stigma:
            stigma = '%s' % stigma
            stigma = stigma.strip()
        if welder:
            welder = '%s' % welder
            welder = welder.strip()
            if welder and not welder in welders:
                welders.append((welder, stigma))
        # контроль это i+19 ячейка
        control_type = accumulate_data(row, i+19, control_types)
        # вид сварного соединения это i+20 ячейка
        conn_type_view = accumulate_data(row, i+20, conn_types_views)
        # тип сварки это i+21 ячейка
        welding_type = accumulate_data(row, i+21, welding_types)
        # категория это i+22 ячейка
        category = accumulate_data(row, i+22, categories)
        # результат контроля это i+23 ячейка
        control_result = accumulate_data(row, i+23, control_results)

        repair = 1 if row[i+6].value else None
        if row[i+7].value:
            repair = 2
        cutout = True if row[i+8].value else None
        diameter = row[i+9].value if row[i+9].value else None
        if diameter:
            diameter = kill_quotes(str(diameter).replace(',', '.'), 'int')
            if not diameter:
                diameter = None
        side_thickness = row[i+10].value if row[i+10].value else None
        if side_thickness:
            side_thickness = kill_quotes(str(side_thickness).replace(',', '.'), 'int')
            if not side_thickness:
                side_thickness = None
        welding_date = row[i+13].value if row[i+13].value else None
        if welding_date:
            welding_date = str_to_date(str(welding_date))
        request_number = row[i+17].value if row[i+17].value else None
        request_control_date = row[i+18].value if row[i+18].value else None
        if request_control_date:
            request_control_date = str_to_date(str(request_control_date))
        conclusion_number = row[i+25].value if row[i+25].value else None
        conclusion_date = row[i+26].value if row[i+26].value else None
        if conclusion_date:
            conclusion_date = str_to_date(str(conclusion_date))
        notice = row[i+27].value if row[i+27].value else None
        dinc = row[i+28].value if row[i+28].value else None
        if dinc:
            dinc = kill_quotes(str(dinc).replace(',', '.'), 'int')
            if not dinc:
                dinc = None

        welding_joints.append({
            'base': base,
            'contract': contract,
            'line': line,
            'scheme': scheme,
            'joint': joint,
            'repair': repair,
            'cutout': cutout,
            'diameter': diameter,
            'side_thickness': side_thickness,
            'material': material,
            'join_type': join_type,
            'welding_date': welding_date,
            'workshift': workshift,
            'welder': welder,
            'request_number': request_number,
            'request_control_date': request_control_date,
            'control_type': control_type,
            'conn_type_view': conn_type_view,
            'welding_type': welding_type,
            'category': category,
            'control_result': control_result,
            'conclusion_number': conclusion_number,
            'conclusion_date': conclusion_date,
            'notice': notice,
            'dinc': dinc,
        })

    logger.info('Bases len %s' % len(bases))
    for base in bases:
        analog = Base.objects.filter(name=base).first()
        if not analog:
            analog = Base.objects.create(name=base)
    logger.info('Contracts len %s' % len(contracts))
    for contract in contracts:
        analog = Contract.objects.filter(name=contract).first()
        if not analog:
            analog = Contract.objects.create(name=contract)
    logger.info('Lines len %s' % len(lines))
    for line in lines:
        analog = Line.objects.filter(name=line).first()
        if not analog:
            analog = Line.objects.create(name=line)
    logger.info('Schemes len %s' % len(schemes))
    for scheme in schemes:
        analog = Scheme.objects.filter(name=scheme).first()
        if not analog:
            analog = Scheme.objects.create(name=scheme)
    logger.info('Joints len %s' % len(joints))
    for joint in joints:
        line = Line.objects.filter(name=joint[1]).first()
        if not line:
            logger.info('line not found %s' % joint[1])
            continue
        analog = Joint.objects.filter(name=joint[0], line=line).first()
        if not analog:
            analog = Joint.objects.create(name=joint[0], line=line)
    logger.info('Materials len %s' % len(materials))
    for material in materials:
        analog = Material.objects.filter(name=material).first()
        if not analog:
            analog = Material.objects.create(name=material)
    logger.info('JoinTypes len %s' % len(join_types))
    for join_type in join_types:
        analog = JoinType.objects.filter(name=join_type).first()
        if not analog:
            analog = JoinType.objects.create(name=join_type)
    logger.info('Workshifts: %s' % workshifts)
    logger.info('Welders len %s' % len(welders))
    for welder in welders:
        analog = Welder.objects.filter(name=welder[0]).first()
        if not analog:
            analog = Welder.objects.create(name=welder[0], stigma=welder[1])
    logger.info('ControlTypes: %s' % control_types)
    logger.info('ConnTypesViews: %s' % conn_types_views)
    logger.info('WeldingTypes: %s' % welding_types)
    logger.info('Categories: %s' % categories)
    logger.info('ControlResults: %s' % control_results)
    #logger.info('WeldingJoints: %s' % welding_joints)
    for item in welding_joints:

        workshift = None
        if item['workshift']:
            for choice in WeldingJoint.workshift_choices:
                if choice[1] == item['workshift'].upper():
                    workshift = choice[0]
        control_type = None
        if item['control_type']:
            for choice in WeldingJoint.control_choices:
                if choice[1] == item['control_type'].upper():
                    control_type = choice[0]
        welding_conn_view = None
        if item['conn_type_view']:
            for choice in WeldingJoint.welding_conn_view_choices:
                if choice[1] == item['conn_type_view'].upper():
                    welding_conn_view = choice[0]
        welding_type = None
        if item['welding_type']:
            for choice in WeldingJoint.welding_type_choices:
                if choice[1] == item['welding_type'].upper():
                    welding_type = choice[0]
        category = None
        if item['category']:
            for choice in WeldingJoint.category_choices:
                if choice[1] == item['category'].upper():
                    category = choice[0]
        control_result = None
        if item['control_result']:
            for choice in WeldingJoint.control_result_choices:
                if choice[1] == item['control_result'].upper():
                    control_result = choice[0]

        line = Line.objects.filter(name=item['line']).first()
        if not line or not item['joint']:
            continue
        welding_joint = WeldingJoint.objects.create(**{
            'base': Base.objects.filter(name=item['base']).first(),
            'contract': Contract.objects.filter(name=item['contract']).first(),
            'scheme': Scheme.objects.filter(name=item['scheme']).first(),
            'joint': Joint.objects.filter(name=item['joint'][0], line=line).first(),
            'repair': item['repair'],
            'cutout': item['cutout'],
            'diameter': item['diameter'],
            'side_thickness': item['side_thickness'],
            'material': Material.objects.filter(name=item['material']).first(),
            'join_type': JoinType.objects.filter(name=item['join_type']).first(),
            'welding_date': item['welding_date'],
            'workshift': workshift,
            'request_number': request_number,
            'request_control_date': request_control_date,
            'control_type': control_type,
            'welding_conn_view': welding_conn_view,
            'welding_type': welding_type,
            'category': category,
            'control_result': control_result,
            'conclusion_number': conclusion_number,
            'conclusion_date': conclusion_date,
            'notice': notice,
            'dinc': dinc,
        })
        if item['welder']:
            JointWelder.objects.create(**{
                'welding_joint': welding_joint,
                'welder':  Welder.objects.filter(name=item['welder'][0]).first(),
            })


def analyze_daily_report_weldings():
    """Заполнение базы уникальными значениями из эксельки"""
    wb = open_wb(daily_report_weldings)

    sheet = None
    for item in wb:
        if item.title in ('Отчет по стыкам ГФУ', ):
            sheet = item
    if not sheet:
        logger.info('[ERROR]: sheet not found')
        return

    rows = sheet.rows
    i, header = search_header(rows)
    if header is None:
        logger.info('[ERROR]: header not found')


    tituls = []
    lines = []
    joints = []
    materials = []
    join_types = []
    workshifts = []
    welders = []
    control_types = []
    conn_types_views = []
    welding_types = []
    categories = []
    control_results = []
    for row in rows: # Продолжаем обход по генератору
        cell_values = [cell.value for cell in row]
        if not any(cell_values):
            logger.info('EOF reached')
            break

        # Титул это i+1 ячейка
        titul = accumulate_data(row, i+1, tituls)
        # Линия это i+2 ячейка
        line = accumulate_data(row, i+2, lines)
        # № стыка это i+3 ячейка
        joint = row[i+3].value
        if joint and line:
            joint = '%s' % joint
            joint = joint.strip()
            if joint and not joint in joints:
                joints.append((joint, line))
        # материал (сталь) это i+9 ячейка
        material = accumulate_data(row, i+9, materials)
        # свариваемые элементы это i+10 ячейка
        join_type = accumulate_data(row, i+10, join_types)
        # смена это i+12 ячейка
        workshift = accumulate_data(row, i+12, workshifts)
        welder = row[i+13].value # имя сварщика это i+15 ячейка
        stigma = row[i+14].value # клеймо сварщика это i+16 ячейка
        if stigma:
            stigma = '%s' % stigma
            stigma = stigma.strip()
        if welder:
            welder = '%s' % welder
            welder = welder.strip()
            if welder and not welder in welders:
                welders.append((welder, stigma))
        # контроль это i+17 ячейка
        control_type = accumulate_data(row, i+17, control_types)
        # вид сварного соединения это i+18 ячейка
        conn_type_view = accumulate_data(row, i+18, conn_types_views)
        # тип сварки это i+19 ячейка
        welding_type = accumulate_data(row, i+19, welding_types)
        # категория это i+20 ячейка
        category = accumulate_data(row, i+20, categories)
        # результат контроля это i+22 ячейка
        control_result = accumulate_data(row, i+22, control_results)

    logger.info('Tituls len %s' % len(tituls))
    for titul in tituls:
        analog = Titul.objects.filter(name=titul).first()
        if not analog:
            analog = Titul.objects.create(name=titul)
    logger.info('Lines len %s' % len(lines))
    for line in lines:
        analog = Line.objects.filter(name=line).first()
        if not analog:
            analog = Line.objects.create(name=line)
    logger.info('Joints len %s' % len(joints))
    for joint in joints:
        line = Line.objects.filter(name=joint[1]).first()
        if not line:
            logger.info('line not found %s' % joint[1])
            continue
        analog = Joint.objects.filter(name=joint[0], line=line).first()
        if not analog:
            analog = Joint.objects.create(name=joint[0], line=line)
    logger.info('Materials len %s' % len(materials))
    for material in materials:
        analog = Material.objects.filter(name=material).first()
        if not analog:
            analog = Material.objects.create(name=material)
    logger.info('JoinTypes len %s' % len(join_types))
    for join_type in join_types:
        analog = JoinType.objects.filter(name=join_type).first()
        if not analog:
            analog = JoinType.objects.create(name=join_type)
    logger.info('Workshifts: %s' % workshifts)
    logger.info('Welders len %s' % len(welders))
    for welder in welders:
        analog = Welder.objects.filter(name=welder[0]).first()
        if not analog:
            analog = Welder.objects.create(name=welder[0], stigma=welder[1])
    logger.info('ControlTypes: %s' % control_types)
    logger.info('ConnTypesViews: %s' % conn_types_views)
    logger.info('WeldingTypes: %s' % welding_types)
    logger.info('Categories: %s' % categories)
    logger.info('ControlResults: %s' % control_results)

class Command(BaseCommand):
    def handle(self, *args, **options):
        JointWelder.objects.all().delete()
        WeldingJoint.objects.all().delete()
        analyze_statement_joints()
        analyze_daily_report_weldings()

