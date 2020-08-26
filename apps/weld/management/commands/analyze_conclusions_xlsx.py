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
from apps.main_functions.files import ListDir, isForD
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
from apps.weld.conclusion_model import JointConclusion, RKFrames

logger = logging.getLogger(__name__)

def clean_tables():
    """Очистка таблиц"""
    RKFrames.objects.all().delete()
    JointConclusion.objects.all().delete()

pass_folders = (
    'У101',
    'У102',
    'У201',
    'У202',
    'У300',
    'У500',
    'У600',
    'У800',
    'У910',
    'У920',
    'У940',
    'У960',
    'У980',
)
pass_folders = ()

def analyze_conclusions():
    """Пробуем разобраться в полном пиздеце всех заключений"""
    folder = 'conclusions'
    # Идем по папкам (титулам)
    for titul_str in ListDir(folder):
        if titul_str in pass_folders:
            logger.info('--- PASSING %s ---' % titul_str)
            continue
        titul_path = os.path.join(folder, titul_str)
        if isForD(titul_path) != 'dir':
            #logger.info('--- NOT FOLDER %s ---' % titul_path)
            continue
        titul = Titul.objects.filter(name=titul_str).first()
        if not titul:
            logger.info('--- TITUL ABSENT %s ---' % titul_str)
            continue
        logger.info('--- ANALYZE TITUL %s ---' % titul.name)
        # Титул нашли - идем по вложенным папкам (линиям)
        for line_str in ListDir(titul_path):
            line_path = os.path.join(titul_path, line_str)
            if isForD(line_path) != 'dir':
                #logger.info('--- NOT FOLDER %s ---' % line_path)
                continue
            # Линию найдем в файле как и все остальное,
            # титул есть - пока достаточно
            for conclusion in ListDir(line_path):
                conclusion_path = os.path.join(line_path, conclusion)
                analyze_conclusion(conclusion_path, titul)

def analyze_conclusion(path: str, titul: str):
    """Разбираем ибучее заключение из эксель файла
       :param path: путь до эксельки заключения
       :param titul: экземпляр Titul
    """
    if not path.endswith('.xlsx'):
        #logger.info('NOT XLSX file %s' % path)
        return
    wb = open_wb(path)
    sheet = None
    # ВИК есть всегда - ищем его,
    # по нему получим линию и мб еще что-то
    for item in wb:
        if item.title == 'ВИК':
            sheet = item
            analyze_vik(sheet, titul, path)
            #exit()

# Определяем шифт для титула по совпадениям
titul_code_decider = {}
def analyze_titul_code(titul, titul_code: str):
    """Записываем код для титула,
       но так как вносят хуй проссы как,
       то набираем 10 совпадений - тогда и пишем
       :param titul: экземпляр titul
       :param titul_code: шифр титула, который проверяем
    """
    if titul.code or not titul_code:
        return
    if not titul.name in titul_code_decider:
        titul_code_decider[titul.name] = {}
    if not titul_code in titul_code_decider[titul.name]:
        titul_code_decider[titul.name][titul_code] = 0
    titul_code_decider[titul.name][titul_code] += 1
    if titul_code_decider[titul.name][titul_code] > 10:
        titul.code = titul_code
        titul.save()

# Определяем описание для титула по совпадениям
titul_description_decider = {}
def analyze_titul_description(titul, titul_description: str):
    """Записываем описание для титула,
       но так как вносят хуй проссы как,
       то набираем 10 совпадений - тогда и пишем
       :param titul: экземпляр titul
       :param titul_description: описание титула, которое проверяем
    """
    if titul.description or not titul_description:
        return
    if not titul.description in titul_description_decider:
        titul_description_decider[titul.name] = {}
    if not titul_description in titul_description_decider[titul.name]:
        titul_description_decider[titul.name][titul_description] = 0
    titul_description_decider[titul.name][titul_description] += 1
    if titul_description_decider[titul.name][titul_description] > 10:
        titul.description = titul_description
        titul.save()

def get_welding_date(value):
    """Находим дату сварки
       :param value: значение даты
    """
    if not value:
        return
    welding_date_str = '%s' % value
    welding_date_str = welding_date_str.replace(',', '.')
    return str_to_date(welding_date_str.strip())

def get_size(size):
    """Находим ибучий размер трубы
       :param size: значение сечения
    """
    if not size:
        return
    size = '%s' % size.strip()
    # Специфический блевонтин
    if size.count('Ø') > 1:
      size = size.split('-Ø')[0]
      size = size.split('/Ø')[0]
    size = size.replace('8/9', '8')
    size = size.replace('9/12', '9')
    size = size.replace('/', 'x')
    # Обычный блевонтин
    size = size.replace('×', 'x')
    size = size.replace('х', 'x')
    size = size.replace(',', '.')
    size = size.replace('мм', '')
    size = size.strip()
    if size.endswith('.'):
        size = size[:-1]
    if 'Ø' in size or 'x' in size:
       diameter, side_thickness = size.split('x')
       diameter = diameter.replace('Ø', '').strip()
       side_thickness = side_thickness.strip()
       return diameter, side_thickness
    return None

def get_material(text):
    """Получить материал и тип сварного соединения
       примерно из такой строки
       Тип сварных соединений – С17, материал – 09Г2С
       welding_conn_view правильно будет, а не welding_type,
       но похуй пока
       :param text: строка, где ищем тип соденений и материал
    """
    material = None
    welding_type_str, material_str = text.split('материал')
    material_str = material_str.strip()
    material_str = material_str.split(' ')[-1]
    material_str = material_str.strip()
    if '09' in material_str:
        material = 1
    elif '12' in material_str:
        material = 2
    elif '08' in material_str:
        material = 3
    elif '358' in material_str:
        material = 4

    welding_type = None
    welding_type_str = welding_type_str.split('Тип сварных соединений')[-1]
    welding_type_str = welding_type_str.split(',')[0].strip()
    welding_type_str = welding_type_str.split(' ')[-1]
    if '17' in welding_type_str and '20' in welding_type_str:
        welding_type = 4
    elif '17' in welding_type_str:
        welding_type = 1
    elif '19' in welding_type_str:
        welding_type = 2
    elif '20' in welding_type_str:
        welding_type = 3
    return material, welding_type

def get_welding_type(text):
    """Поиск типа сварки
       :param text: строка, где ищем тип сварки
    """
    if 'аргонодуго' in text and ' дуго' in text:
        return 3
    if 'аргонодуго' in text:
        return 1
    if ' дуго' in text:
        return 2

def analyze_vik(sheet, titul: str, path: str):
    """Разбираем заибучее ВИК заключение,
       это первый лист в экселевском файле
       :param sheet: лист эксельки
       :param titul: экземпляр Titul
       :param path: путь до файла (для отладки)
    """
    # Не всегда в титуле есть код титула,
    # может быть просто название, например,
    # Эстакада трубопроводов
    # Может вообще не быть названия титула
    titul_description = sheet['F6'].value or sheet['G6'].value
    titul_name = None
    if titul_description:
        if not 'У' in titul_description:
            titul_name = sheet['I6'].value
        else:
            titul_name = 'У%s' % titul_description.split('У')[1]
            titul_description = titul_description.split('У')[0]
    # --------------------------------------
    # Захерачиваем описание титулу,
    # если не совпало имя титула, то алертим
    # --------------------------------------
    if titul_name:
        titul_name = titul_name.strip()
    if titul_name != titul.name:
        pass
        #logger.info('TITUL HAS INCORRECT NAME %s vs %s' % (titul.name, titul_name))
        #return
    # ---------------------------------------
    # Определяем описание титула накопительно
    # ---------------------------------------
    analyze_titul_description(titul, titul_description)
    # -----------------------------------
    # Определяем шифр титула накопительно
    # -----------------------------------
    titul_code = sheet['H7'].value or sheet['I7'].value
    analyze_titul_code(titul, titul_code)
    # ----------------
    # Определяем линию
    # ----------------
    line_str = sheet['A8'].value or sheet['B8'].value or sheet['A7'].value
    if not line_str:
        logger.info('--- LINE ABSENT %s---' % path)
        return
    line_str = line_str.replace('Линия', '').strip()
    line_str = line_str.replace('0 H', '0H')
    line_str = line_str.replace('  ', ' ')
    try:
        line_str = replace_rus2eng(line_str)
    except Exception as e:
        logger.info(e)
        return
    line = Line.objects.filter(name=line_str, titul=titul).first()
    if not line:
        logger.info('--- LINE NOT FOUND %s ---' % line_str)
        # Создаем линию, если название адекватное
        if len(line_str) < 5:
            return
        line = Line.objects.create(name=line_str, titul=titul)
    # -------------------
    # Находим дату сварки
    # -------------------
    welding_date = get_welding_date(sheet['G11'].value)
    if not welding_date:
        welding_date = get_welding_date(sheet['H11'].value)
    if not welding_date:
        welding_date = get_welding_date(sheet['G10'].value)
    if not welding_date:
        logger.info('--- DATE INCORRENT %s ---' % path)
    # --------------------------------
    # Находим толщину стенки и диаметр
    # --------------------------------
    side_thickness = diameter = None
    size_row_letter = 'I'
    is_completed_row = (sheet['I16'].value and sheet['I16'].value.strip() == 'выполнен') or (sheet['I14'].value and sheet['I14'].value.strip() == 'выполнен')
    if not sheet['A1'].value or is_completed_row:
        size_row_letter = 'J'

    size = None
    for i in (16, 17, 18):
        size_row_number = i
        size_row_value = sheet['%s%s' % (size_row_letter, size_row_number)].value
        if not size_row_value:
            continue
        #print('=', size_row_value)
        size = get_size(size_row_value)
        if size:
            break
    if not size:
        logger.info('--- SIDE_THICKNESS or DIAMETER NOT FOUND %s, %s ---' % (size_row_number, path))
    else:
        diameter, side_thickness = size
    # ------------------------
    # Находим номера стыков
    # У пидорасов на ВИК стыки
    # разделены точкой,
    # а на РК слешем
    # ------------------------
    joint_row_letter = 'B'
    if not sheet['A1'].value:
        joint_row_letter = 'C'
    joints_str = sheet['%s%s' % (joint_row_letter, size_row_number)].value
    if not joints_str:
        logger.info('--- JOINTS NOT FOUND %s, %s ---' % (size, path))
        return
    # Если есть говносмещение - мы найдем ячейку с №
    # вместо номеров стыков
    if joints_str == '№':
        if joint_row_letter == 'B':
            joint_row_letter = 'C'
        joints_str = sheet['%s%s' % (joint_row_letter, size_row_number)].value
    joints_str = '%s' % joints_str
    joints_arr = joints_str.split(',')

    # ----------------------------
    # Находим строчку с материалом
    # и типом сварных соединений
    # ----------------------------
    material = welding_conn_view = None
    material_str = None
    material_row_letter = 'A'
    if not sheet['A1'].value or (sheet['A18'].value is None and sheet['A19'].value is None and sheet['A20'].value is None and sheet['A21'].value is None):
        material_row_letter = 'B'
    material_q = ('Тип сварных соединений', 'материал')
    for i in (18, 19, 20, 21):
        material_row_number = i
        value = sheet['%s%s' % (material_row_letter, material_row_number)].value
        if not value:
            continue
        if material_q[0] in value and material_q[1] in value:
            material_str = value
            break
    if not material_str:
        logger.info('--- MATERIAL NOT FOUND %s ---' % path)
    else:
        material, welding_conn_view = get_material(material_str)
    if not material or not welding_conn_view:
        logger.info('--- MATERIAL NOT FOUND %s ---' % path)
    # -----------------
    # Поиск типа сварки
    # -----------------
    welding_type = None
    welding_type_row_letter = material_row_letter
    welding_type_row_number = material_row_number + 1
    welding_type_str = sheet['%s%s' % (
        welding_type_row_letter,
        welding_type_row_number
    )].value
    if not welding_type_str:
        logger.info('--- WELDING_TYPE NOT FOUND %s ---' % path)
    else:
        welding_type = get_welding_type(welding_type_str)
    if not welding_type:
        logger.info('--- WELDING_TYPE NOT FOUND %s ---' % path)

    for joint_str in joints_arr:
        joint_str = joint_str.replace('.', '/').replace('\\', '/').strip()
        if not joint_str:
            continue

        # Если нет цифр в номере стыка, тогда не создаем
        digits = kill_quotes(joint_str, 'int')
        if not digits:
            logger.info('--- BAD JOINT %s, %s ---' % (joint_str, path))
        else:
            joint = Joint.objects.filter(line=line, name=joint_str).first()
            if not joint:
                logger.info('--- JOINT NOT FOUND %s, %s ---' % (joint_str, line.name))
                # Ну создаем, блеать, раз линия найдена
                joint = Joint.objects.create(line=line, name=joint_str)
            # Стык найден - надо найти заключение,
            # если нету - создать или обновить
            welding_joints = WeldingJoint.objects.filter(joint=joint)
            if len(welding_joints) > 1:
                logger.info('--- MORE THAN 1 WeldingJoint %s' % joint)
                return
            if welding_joints:
                welding_joint = welding_joints[0]
            else:
                welding_joint = WeldingJoint(joint=joint)
            welding_joint.state = 3
            welding_joint.diameter = diameter
            welding_joint.side_thickness = side_thickness
            welding_joint.welding_date = welding_date
            welding_joint.material = material
            welding_joint.welding_conn_view = welding_conn_view
            welding_joint.welding_type = welding_type

"""
    repair
    join_type_from
    join_type_to
    workshift
    request_control_date
    control_type
    category
    control_result
    notice
    state
"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        clean_tables()
        analyze_conclusions()
