# -*- coding: utf-8 -*-
import logging

from openpyxl import load_workbook
from io import BytesIO

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.date_time import str_to_date
from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.api_helper import open_wb, search_header, accumulate_data
from apps.weld.enums import WELDING_TYPES, MATERIALS, JOIN_TYPES
from apps.weld.welder_model import Welder
from apps.weld.company_model import Company, Subject, Titul, Base, Line
from apps.weld.models import WeldingJoint, Joint, JointWelder

logger = logging.getLogger(__name__)

# Файлы excel для анализа
daily_report_weldings = 'daily_report_weldings.xlsx'
statement_joints = 'statement_joints.xlsx'

def get_object(row, i: int, model, cond: dict = None):
    """Создать/обновить простой объект (только название)
       :param row: строка
       :param i: номер ячейки
       :param cond: условие для выборки
    """
    if not cond:
        cond = {}
    obj = None
    obj_name = row[i].value
    if obj_name:
        obj_name = str(obj_name).strip()
        if '*' in obj_name:
            return None
        obj = model.objects.filter(name=obj_name).filter(**cond).first()
        if not obj:
            obj = model(name=obj_name)
            for k, v in cond.items():
                setattr(obj, k, v)
        obj.save()
    return obj

def get_choice(item, choices):
    """Найти соответствующий вариант из вариантов модели
       :param item: значение, которое ищем
       :param choices: Варианты из модели
    """
    if item:
        for choice in choices:
            if choice[1].upper() == item.upper():
                return choice[0]
    return None

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

    workshifts = []
    control_types = []
    conn_types_views = []
    welding_types = []
    categories = []
    control_results = []
    materials = []

    z = 0
    for row in rows: # Продолжаем обход по генератору
        z += 1
        cell_values = [cell.value for cell in row]
        if not any(cell_values):
            logger.info('EOF reached')
            break

        # Установка это i+1 ячейка
        base = get_object(row, i+1, Base)
        # Договор это i+2 ячейка
        contract = get_object(row, i+2, Contract)
        # Линия это i+3 ячейка
        line = get_object(row, i+3, Line)
        # № Изометрической схемы это i+4 ячейка
        #scheme = get_object(row, i+4, Scheme)

        # № стыка это i+5 ячейка
        joint = None
        joint_str = row[i+5].value
        if line and joint_str:
            joint_str = '%s' % joint_str
            joint_str = joint_str.strip()
            if '*' in joint_str:
                continue
            joint = Joint.objects.filter(name=joint_str, line=line).first()
            if not joint:
                joint = Joint.objects.create(name=joint_str, line=line)
        else:
            continue

        # -----------------------------
        # Поправка по кривому материалу
        # -----------------------------
        if row[i+11] and row[i+11].value:
            if '316/316L' in row[i+11].value:
                logger.info('[ERROR]: bad material %s' % material)
                continue

        # материал (сталь) это i+11 ячейка
        material_str = accumulate_data(row, i+11, materials)

        # свариваемые элементы это i+12 ячейка
        join_type = get_object(row, i+12, JoinType)

        # смена это i+14 ячейка
        workshift_str = accumulate_data(row, i+14, workshifts)

        # Сварщик
        welder = None
        stigma = row[i+16].value # клеймо сварщика это i+16 ячейка
        if stigma:
            stigma = '%s' % stigma
            stigma = stigma.strip()
            welder = Welder.objects.filter(stigma=stigma).first()

        # контроль это i+19 ячейка
        control_type_str = accumulate_data(row, i+19, control_types)

        # вид сварного соединения это i+20 ячейка
        conn_type_view_str = accumulate_data(row, i+20, conn_types_views)

        # тип сварки это i+21 ячейка
        welding_type_str = accumulate_data(row, i+21, welding_types)

        # категория это i+22 ячейка
        category_str = accumulate_data(row, i+22, categories)

        # результат контроля это i+23 ячейка
        control_result_str = accumulate_data(row, i+23, control_results)

        repair = 1 if row[i+6].value else None
        if row[i+7].value:
            repair = 2

        cutout = True if row[i+8].value else None

        diameter = row[i+9].value if row[i+9].value else None
        if diameter:
            diameter = str(diameter).replace(',', '.')
            try:
                diameter = float(diameter)
            except ValueError:
                diameter = None
                logger.info('[ERROR]: diameter %s' % diameter)

        side_thickness = row[i+10].value if row[i+10].value else None
        if side_thickness:
            side_thickness = str(side_thickness).replace(',', '.')
            try:
                side_thickness = float(side_thickness)
            except ValueError:
                side_thickness = None
                logger.info('[ERROR]: side_thickness %s' % side_thickness)

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
            dinc = str(dinc).replace(',', '.')
            try:
                dinc = float(dinc)
            except ValueError:
                dinc = None
                logger.info('[ERROR]: dinc %s' % dinc)

        workshift = get_choice(workshift_str, WeldingJoint.workshift_choices)

        control_type = get_choice(control_type_str, WeldingJoint.control_choices)

        welding_conn_view = get_choice(conn_type_view_str, WeldingJoint.welding_conn_view_choices)

        welding_type = get_choice(welding_type_str, WELDING_TYPES)

        category = get_choice(category_str, WeldingJoint.category_choices)

        material = get_choice(material_str, MATERIALS)

        control_result = get_choice(control_result_str, WeldingJoint.control_result_choices)

        welding_joint_obj = {
            'base': base,
            'contract': contract,
            #'scheme': scheme,
            'joint': joint,
            'repair': repair,
            'cutout': cutout,
            'diameter': diameter,
            'side_thickness': side_thickness,
            'material': material,
            'join_type': join_type,
            'welding_date': welding_date,
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
        }
        welding_joint = WeldingJoint.objects.create(**welding_joint_obj)
        JointWelder.objects.create(**{
            'welding_joint': welding_joint,
            'welder':  welder,
        })
    logger.info('Workshifts: %s' % workshifts)
    logger.info('ControlTypes: %s' % control_types)
    logger.info('ConnTypesViews: %s' % conn_types_views)
    logger.info('WeldingTypes: %s' % welding_types)
    logger.info('Categories: %s' % categories)
    logger.info('ControlResults: %s' % control_results)
    #logger.info('WeldingJoints: %s' % welding_joints)


def analyze_daily_report_weldings():
    """Заполнение базы уникальными значениями из эксельки"""
    company = Company.objects.create(
        name = 'ООО "ИНК"',
        location = 'г. Усть-Кут',
        contractor = 'ООО "Транспромстрой"',
        fitter = 'ООО "Транспромстрой"',
        code = 'ТПС',
    )
    subject = Subject.objects.create(
      name = 'Усть-Кутская ГФУ',
      code = 'ГФУ',
      company = company,
    )

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

    workshifts = []
    control_types = []
    conn_types_views = []
    welding_types = []
    categories = []
    control_results = []
    materials = []
    join_types = []

    for row in rows: # Продолжаем обход по генератору
        cell_values = [cell.value for cell in row]
        if not any(cell_values):
            logger.info('EOF reached')
            break

        # Титул это i+1 ячейка
        titul = get_object(row, i+1, Titul, {'subject': subject})
        if not titul:
            continue

        diameter = row[i+7].value if row[i+7].value else None
        if diameter:
            diameter = str(diameter).replace(',', '.')
            try:
                diameter = float(diameter)
            except ValueError:
                diameter = None
                logger.info('[ERROR]: diameter %s' % diameter)

        side_thickness = row[i+8].value if row[i+8].value else None
        if side_thickness:
            side_thickness = str(side_thickness).replace(',', '.')
            try:
                side_thickness = float(side_thickness)
            except ValueError:
                side_thickness = None
                logger.info('[ERROR]: side_thickness %s' % side_thickness)

        # Линия это i+2 ячейка
        line = get_object(row, i+2, Line, {'titul': titul})
        if not line:
            #logger.info('line is empty {}'.format(row))
            continue

        # № стыка это i+3 ячейка
        joint = None
        joint_str = row[i+3].value
        if line and joint_str:
            joint_str = '%s' % joint_str
            joint_str = joint_str.strip()
            if '*' in joint_str:
                continue
            joint = Joint.objects.filter(name=joint_str, line=line).first()
            if not joint:
                joint = Joint.objects.create(name=joint_str, line=line)

        # материал (сталь) это i+9 ячейка
        material_str = accumulate_data(row, i+9, materials)

        # свариваемые элементы это i+10 ячейка
        #join_type = get_object(row, i+10, JoinType, {'line': line})
        join_type = accumulate_data(row, i+10, join_types)

        # смена это i+12 ячейка
        workshift_str = accumulate_data(row, i+12, workshifts)

        # Сварщик
        welders = []
        stigma = row[i+14].value # клеймо сварщика это i+14 ячейка
        if stigma:
            stigma_arr = stigma.split('+')
            for stigma in stigma_arr:
                stigma = '%s' % stigma
                stigma = stigma.strip()
                welder = Welder.objects.filter(stigma=stigma).first()
                if welder:
                    welders.append(welder)

        # контроль это i+17 ячейка
        control_type_str = accumulate_data(row, i+17, control_types)

        # вид сварного соединения это i+18 ячейка
        conn_type_view_str = accumulate_data(row, i+18, conn_types_views)

        # тип сварки это i+19 ячейка
        welding_type_str = accumulate_data(row, i+19, welding_types)

        # категория это i+20 ячейка
        category_str = accumulate_data(row, i+20, categories)

        # результат контроля это i+22 ячейка
        control_result_str = accumulate_data(row, i+22, control_results)

        repair = 1 if row[i+4].value else None
        if row[i+5].value:
            repair = 2

        cutout = True if row[i+6].value else None

        welding_date = row[i+11].value if row[i+11].value else None
        if welding_date:
            welding_date = str_to_date(str(welding_date))

        request_number = row[i+15].value if row[i+15].value else None

        request_control_date = row[i+16].value if row[i+16].value else None
        if request_control_date:
            request_control_date = str_to_date(str(request_control_date))

        notice = row[i+23].value if row[i+23].value else None

        dinc = row[i+24].value if row[i+24].value else None
        if dinc:
            dinc = str(dinc).replace(',', '.')
            try:
                dinc = float(dinc)
            except ValueError:
                dinc = None
                logger.info('[ERROR]: dinc %s' % dinc)

        workshift = get_choice(workshift_str, WeldingJoint.workshift_choices)

        control_type = get_choice(control_type_str, WeldingJoint.control_choices)

        welding_conn_view = get_choice(conn_type_view_str, WeldingJoint.welding_conn_view_choices)

        welding_type = get_choice(welding_type_str, WELDING_TYPES)

        category = get_choice(category_str, WeldingJoint.category_choices)

        control_result = get_choice(control_result_str, WeldingJoint.control_result_choices)

        material = get_choice(material_str, MATERIALS)

        join_type_from = None
        join_type_to = None
        if join_type:
            join_type_arr = join_type.split('/')
            if len(join_type_arr) == 2:
                for item in JOIN_TYPES:
                    if item[1][:-1] in join_type_arr[0]:
                        join_type_from = item[0]
                    if item[1][:-1] in join_type_arr[1]:
                        join_type_to = item[0]
        #print(join_type_from, join_type_to, join_type)

        state = 1
        if repair:
            state = 4

        welding_joint_obj = {
            'joint': joint,
            'repair': repair,
            'cutout': cutout,
            'material': material,
            'welding_date': welding_date,
            'workshift': workshift,
            'request_number': request_number,
            'request_control_date': request_control_date,
            'control_type': control_type,
            'welding_conn_view': welding_conn_view,
            'welding_type': welding_type,
            'category': category,
            'control_result': control_result,
            'notice': notice,
            'join_type_from': join_type_from,
            'join_type_to': join_type_to,
            'diameter': diameter,
            'side_thickness': side_thickness,
            'state': state,
        }

        welding_joint = WeldingJoint.objects.create(**welding_joint_obj)
        for w, welder in enumerate(welders):
            JointWelder.objects.create(**{
                'welding_joint': welding_joint,
                'welder':  welder,
                'position': w+1,
            })
    logger.info('Workshifts: %s' % workshifts)
    logger.info('ControlTypes: %s' % control_types)
    logger.info('ConnTypesViews: %s' % conn_types_views)
    logger.info('WeldingTypes: %s' % welding_types)
    logger.info('Categories: %s' % categories)
    logger.info('ControlResults: %s' % control_results)
    #logger.info('WeldingJoints: %s' % welding_joints)
    logger.info('JoinTypes: %s' % join_types)

def clean_tables():
    JointWelder.objects.all().delete()
    WeldingJoint.objects.all().delete()
    Base.objects.all().delete()
    Titul.objects.all().delete()
    Line.objects.all().delete()
    Joint.objects.all().delete()
    Company.objects.all().delete()
    Subject.objects.all().delete()

class Command(BaseCommand):
    def handle(self, *args, **options):
        clean_tables()
        #analyze_statement_joints()
        analyze_daily_report_weldings()
