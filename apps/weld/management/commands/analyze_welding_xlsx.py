# -*- coding: utf-8 -*-
import os
import logging

from openpyxl import load_workbook
from io import BytesIO

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.date_time import str_to_date
from apps.main_functions.functions import object_fields
from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.api_helper import open_wb, search_header, accumulate_data
from apps.main_functions.files import ListDir
from apps.files.models import Files

from apps.weld.enums import (WELDING_TYPES,
                             CONCLUSION_STATES,
                             MATERIALS,
                             JOIN_TYPES,
                             replace_rus2eng,
                             replace_eng2rus, )
from apps.weld.welder_model import Welder
from apps.weld.company_model import Company, Subject, Titul, Base, Line
from apps.weld.models import WeldingJoint, Joint, JointWelder, WeldingJointState, recalc_joints

logger = logging.getLogger(__name__)

# Файлы excel для анализа
daily_report_weldings = 'daily_report_weldings.xlsx'

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
        if model in (Line, ):
            obj_name = replace_rus2eng(obj_name)
            first4letters = obj_name[:6]
            if not '-' in first4letters:
                obj_name = obj_name.replace(' ', '-')
                obj_name = '%s-%s' % (obj_name[:4], obj_name[4:])
                obj_name = obj_name.replace('--', '-')
                #print('obj_name', obj_name)
                if len(obj_name) < 5:
                    return
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

def get_welding_joint_analog(joint, new_joint: dict):
    """Ищем аналог joint по словарю new_joint
       :param joint: экземпляр модели WeldingJoint
       :param new_joint: словарь для новой заявки на стык
    """
    analog = WeldingJoint.objects.filter(joint=joint).first()
    if analog:
        # Пишем различия
        print(" ### analog ### ")
        analog_obj = object_fields(analog)
        for key, value in analog_obj.items():
            new_value = new_joint.get(key)
            if not value == new_value:
                print('diff %s %s' % (value, new_value))
        return analog
    return None

def more_lines_helper(subject: Subject, path: str):
    """Загрузка дополнительных узлов в дополнительным линиям
       :param subject: объект
       :param path: путь до эксельки
    """
    wb = open_wb(path)
    sheet = wb.active
    rows = sheet.rows
    cur_titul = None
    for row in rows:
        cell_values = [cell.value for cell in row]
        # 1 - линия
        # 2 - стык
        # 3 - диаметр х тощина стенки
        # 4 - дата сварки
        # 5 - клеймо
        # 6 - вид сварного соединения
        # 7 - тип сварки
        # 12 - статус (новый/готов)
        digit = row[0].value
        if not digit:
            continue
        digit = str(digit)
        if 'Титул ' in digit:
            titul_str = digit.split('Титул ')[1]
            titul_str = titul_str.split(' ')[0]
            titul_str = titul_str.split('.')[0]
            titul = Titul.objects.filter(name=titul_str).first()
            if not titul:
                #logger.info('[ERROR]: titul not found %s' % titul_str)
                cur_titul = Titul.objects.create(name=titul_str, subject=subject)
            else:
                cur_titul = titul

        diameter = side_thickness = date = stigma = welding_conn_view = welding_type = None
        joint_str = row[2].value
        size = row[3].value
        if size and ('х' in size or 'ъ' in size):
           size = str(size).strip()
           if 'ъ' in size:
               diameter, side_thickness = size.split('ъ')
           elif 'х' in size:
               diameter, side_thickness = size.split('х')
           elif 'x' in size:
               diameter, side_thickness = size.split('x')
        if row[4].value:
            date = str_to_date(str(row[4].value))
        if row[5].value:
            stigma = str(row[5].value).strip()
            try:
                stigma = replace_rus2eng(stigma)
            except Exception as e:
                print('[ERROR]: %s' % e)
                stigma = None
        if row[6].value:
            welding_conn_view_str = replace_eng2rus(row[6].value)
            welding_conn_view = get_choice(welding_conn_view_str, WeldingJoint.welding_conn_view_choices)
        if row[7].value:
            welding_type = row[7].value.replace('+', ' - ')
            welding_type = replace_eng2rus(welding_type)
            welding_type = welding_type.replace('  ', ' ')
            welding_type = get_choice(welding_type, WELDING_TYPES)

        line_str = row[1].value
        if not line_str or not 'Линия ' in line_str:
            #print(digit, line_str)
            continue
        line_str = line_str.split('Линия ')[1]
        line_str = line_str.strip()
        try:
            line_str = replace_rus2eng(line_str)
        except Exception:
            print('Русские буквы даже после всех замен %s, стык %s' % (line_str, joint_str))
            continue
        analogs = Line.objects.filter(name__startswith=line_str, titul=cur_titul)
        for item in analogs:
            if item.name.split('-')[0] == line_str:
                analogs = [item]
                break
        repair = None
        state = 1
        state_str = row[12].value
        if state_str:
            if 'готов' in state_str:
                state = 3
            elif 'ремонт' in state_str:
                repair = 1
            #print(state_str)
        if not analogs:
            #print('Линия не найдена %s в титуле %s, стык %s' % (line_str, cur_titul.name, joint_str))
            continue
        elif len(analogs) > 1:
            print('Найдено больше 1 линии по "%s", это %s в титуле %s, стык %s' % (line_str, [item.name for item in analogs], cur_titul.name, joint_str))
            pass
        else:
            line = analogs[0]
            #print('line %s' % line.name)
            #print(diameter, side_thickness, date, stigma, welding_conn_view, welding_type)
            joint = get_object(row, 2, Joint, {'line': line})

            welding_joint_obj = {
                'joint': joint,
                'diameter': diameter,
                'side_thickness': side_thickness,
                'request_control_date': date,
                'welding_conn_view': welding_conn_view,
                'welding_type': welding_type,
                'state': state,
                'repair': repair,
            }

            # Ищем аналог
            analog = get_welding_joint_analog(joint, welding_joint_obj)
            if analog:
                continue

            welding_joint = WeldingJoint.objects.create(**welding_joint_obj)

            welder = Welder.objects.filter(stigma__icontains=stigma).first()
            if not welder:
                print('welder not found %s' % stigma)
                continue
            JointWelder.objects.create(welding_joint=welding_joint, welder=welder, position=1)

def more_lines(subject: Subject):
    """Загрузка доп. линий из more_lines.xlsx
       папка more_lines должна содержать все файлы по доп. линиям
       :param subject: объект
    """
    wb = open_wb('more_lines.xlsx')
    sheet = wb.active
    rows = sheet.rows
    for row in rows:
        cell_values = [cell.value for cell in row]
        if not any(cell_values):
            logger.info('EOF reached')
            break

        titul_str = cell_values[0]
        line_str = cell_values[1]
        if not titul_str or not line_str or not '-' in line_str:
            continue
        # Титул
        titul = get_object(row, 0, Titul, {'subject': subject})
        if not titul:
            continue
        # Линия
        try:
            line = get_object(row, 1, Line, {'titul': titul})
        except Exception:
            print('Русские буквы даже после всех замен %s' % line_str)
            continue
    folder = 'more_lines'
    files = ListDir(folder)
    for item in files:
        if not item.endswith('.xlsx'):
            logger.info('non xlsx file %s' % item)
            continue
        path = os.path.join(folder, item)
        print('Анализ файла %s' % item)
        more_lines_helper(subject, path)

def analyze_daily_report_weldings():
    """Заполнение базы уникальными значениями из эксельки"""
    company = Company.objects.create(
        name = 'ООО "Транспромстрой"',
        customer = 'ООО "ИНК"',
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

        control_result = get_choice(control_result_str, CONCLUSION_STATES)

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

        # Ищем аналог
        analog = get_welding_joint_analog(joint, welding_joint_obj)
        if analog:
            continue

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

    # -----------------------------
    # Загрузка дополнительных линий
    # из more_lines.xlsx
    # -----------------------------
    more_lines(subject)

def clean_tables():
    """Похерить данные в таблицах перед заливочкой"""
    JointWelder.objects.all().delete()
    WeldingJoint.objects.all().delete()
    Base.objects.all().delete()
    Titul.objects.all().delete()
    Line.objects.all().delete()
    Joint.objects.all().delete()
    Company.objects.all().delete()
    Subject.objects.all().delete()
    WeldingJointState.objects.all().delete()
    for item in Files.objects.all():
        item.delete()

class Command(BaseCommand):
    def handle(self, *args, **options):
        clean_tables()
        analyze_daily_report_weldings()
        for line in Line.objects.all():
            recalc_joints(line)
