# -*- coding: utf-8 -*-
import logging
import re

from openpyxl import load_workbook
from io import BytesIO

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.date_time import str_to_date
from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.api_helper import open_wb, search_header, accumulate_data
from apps.weld.enums import WELDING_TYPES, replace_rus2eng, replace_eng2rus
from apps.weld.welder_model import (Welder,
                                    LetterOfGuarantee,
                                    Vik,
                                    ControlK,
                                    HoldingKSS,
                                    MechTest,
                                    NAX,
                                    AdmissionSheet, )
from apps.weld.company_model import Company
from apps.weld.material_model import Material

logger = logging.getLogger(__name__)

# Файлы excel для анализа
welders_xlsx = 'welders.xlsx'

def get_notice(row, i: int):
    """Получить примечание
       :param row: строка
       :param i: номер ячейки
    """
    notice = row[i].value
    if notice:
        notice = notice.strip()
    return notice

def get_welder(row, i: int, notice: str = None, fired: bool = False):
    """Создать/обновить сварщика
       :param row: строка
       :param i: номер ячейки
       :param notice: примечание
    """
    welder = None
    welder_str = row[i].value
    # клеймо - следующая ячейка после ФИО сварщика
    stigma = row[i+1].value
    if welder_str and stigma:
        welder_str = str(welder_str).strip()
        stigma = str(stigma).strip()
        welder = Welder.objects.filter(name=welder_str).first()
        if not welder:
            welder = Welder()
        welder.name = welder_str
        welder.stigma = stigma
        welder.notice = notice
        if fired:
            welder.is_active = False
        welder.save()
    return welder

def get_vik(row, i: int, welder):
    """Создать/обновить Акт ВИК
       :param row: строка
       :param i: номер ячейки
       :param welder: сварщик
    """
    vik = None
    vik_number = row[i].value
    # дата - следующая ячейка после номера
    vik_date = row[i+1].value
    if vik_number and vik_date:
        vik_number = str(vik_number).strip()
        vik_date = str(vik_date).strip().replace('г', '')
        vik_date = str_to_date(vik_date)
        vik = Vik.objects.filter(number=vik_number).first()
        if not vik:
            vik = Vik(number=vik_number)
        vik.date = vik_date
        vik.welder = welder
        vik.save()
    return vik

def get_controlk(row, i: int, welder):
    """УЗК/РК контроль
       :param row: строка
       :param i: номер ячейки
       :param welder: сварщик
    """
    controlk = None
    control_number = row[i].value
    # дата - следующая ячейка после номера
    control_date = row[i+1].value
    if control_number and control_date:
        control_number = str(control_number).strip()
        control_date = str(control_date).strip().replace('г', '')
        control_date = str_to_date(control_date)
        controlk = ControlK.objects.filter(number=control_number).first()
        if not controlk:
            controlk = ControlK(number=control_number)
        controlk.date = control_date
        controlk.welder = welder
        controlk.save()
    return controlk

def get_holding_kss(row, i: int, welder,
                    materials: list,
                    holding_choices: list = None,
                    spent_length_choices: list = None,
                    holding_value: str = None,
                    with_spent_len: bool = False):
    """Проведение КСС
       :param row: строка
       :param i: номер ячейки
       :param welder: сварщик
       :param materials: материалы из таблицы (сталь)
       :param holding_choices: ТТ/МК
       :param spent_length_choices: затрачиваемая длина 150мм*2
       :param holding_value: передать значение из (пред) объединенных ячеек
       :param with_spent_len: если до номера идет затрачиваемая длина
    """
    holding_kss = None
    if not holding_choices:
        holding_choices = []
    if not spent_length_choices:
        spent_length_choices = []

    standard_size = row[i].value
    spent_len = None
    # Марка стали идет следом за типоразмером
    # если есть spent_len, значит он идет за маркой стали,
    # иначе номер КСС
    steel = row[i+1].value
    kss_number = row[i+2].value
    kss_state = row[i+4].value

    if with_spent_len:
        spent_len = kss_number
        kss_number = row[i+3].value
        kss_state = None

    if spent_len:
        spent_len = str(spent_len).strip()
        if not spent_len in spent_length_choices:
            spent_length_choices.append(spent_len)

    if kss_state:
        kss_state = str(kss_state).strip()
        if not kss_state in holding_choices:
            holding_choices.append(kss_state)

    if kss_number:
        kss_number = str(kss_number).strip()

    if standard_size and steel:
        standard_size = str(standard_size).strip()
        steel = str(steel).strip()
        steel = replace_eng2rus(steel)

        material = None
        for item in materials:
            if item.name == steel:
                material = item
                break
        if not material:
            material = Material.objects.create(name=steel)
            materials.append(material)
        holding_state = None
        if kss_state:
            for holding_choice in HoldingKSS.holding_choices:
                if holding_choice[1] == kss_state:
                    holding_state = holding_choice[0]

        spent_length = None
        if spent_len:
            for spent_length_choice in HoldingKSS.spent_length_choices:
                if spent_length_choice[1] == spent_len:
                    spent_length = spent_length_choice[0]

        if material:
            holding_kss = HoldingKSS.objects.filter(
                standard_size=standard_size,
                material=material,
                welder=welder).first()
            if not holding_kss:
                holding_kss = HoldingKSS(
                    standard_size=standard_size,
                    material=material,
                    welder=welder)
            holding_kss.spent_length = spent_length
            holding_kss.number = kss_number
            holding_kss.state = holding_state or holding_value
            holding_kss.save()
    return holding_kss

def get_mechtest(row, i: int, welder):
    """Мехиспытание
       :param row: строка
       :param i: номер ячейки
       :param welder: сварщик
    """
    mechtest = None
    mechtest_number = row[i].value
    # дата - следующая ячейка после номера
    mechtest_date = row[i+1].value
    if mechtest_number and mechtest_date:
        mechtest_number = str(mechtest_number).strip()
        mechtest_date = str(mechtest_date).strip().replace('г', '')
        mechtest_date = str_to_date(mechtest_date)
        mechtest = MechTest.objects.filter(number=mechtest_number).first()
        if not mechtest:
            mechtest = MechTest(number=mechtest_number)
        mechtest.date = mechtest_date
        mechtest.welder = welder
        mechtest.save()
    return mechtest

def get_nax(row, i: int, welder, wrong_order: bool = False):
    """Аттестат (НАКС)
       :param row: строка
       :param i: номер ячейки
       :param welder: сварщик
       :param wrong_order: другой порядок полей
    """
    nax = None
    # Номер удостоверения
    nax_number = row[i].value
    # способ сварки - следующая ячейка после номера
    nax_welding_type = row[i+1].value
    # годен до - следующая ячейка после способа сварки
    nax_best_before = row[i+2].value
    # НГДО/СК - следующая ячейка после годен до
    nax_acl = row[i+3].value
    # место удостоверения - следующая ячейка после НГДО/СК
    nax_identification = row[i+4].value
    # полугодовая отметка - следующая ячейка после места удостоверения
    nax_half_year_mark = row[i+5].value

    if wrong_order:
        # способ сварки
        nax_welding_type = row[i].value
        # Номер удостоверения - следующая ячейка после способа сварки
        nax_number = row[i+1].value
        # НГДО/СК
        nax_acl = None
        # место удостоверения
        nax_identification = None
        # полугодовая отметка
        nax_half_year_mark = None

    if nax_number and nax_best_before and nax_welding_type:
        number = str(nax_number).strip()
        nax_welding_type = str(nax_welding_type).strip().replace(' ', '')
        nax_best_before = str(nax_best_before).strip().replace('г', '')
        if nax_acl:
            nax_acl = str(nax_acl).strip()
        if nax_identification:
            nax_identification = str(nax_identification).strip()
        if nax_half_year_mark:
            nax_half_year_mark = str(nax_half_year_mark).strip()

        welding_type = None
        for item in WELDING_TYPES:
            if item[1] == nax_welding_type:
                welding_type = item[0]
        best_before = str_to_date(nax_best_before)
        if welding_type and best_before:
            nax = NAX.objects.filter(number=number).first()
            if not nax:
                nax = NAX(number=number)
            nax.best_before = best_before
            nax.welder = welder
            nax.identification = 1 if nax_identification else None
            nax.welding_type = welding_type
            nax.half_year_mark = True if nax_half_year_mark else False
            nax.acl = nax_acl
            nax.save()
        else:
            logger.info('something wrong: welding_type %s, best_before %s' % (nax_welding_type, nax_best_before))
    return nax

def get_admission_sheet(row, i: int, welder, with_date: bool = False):
    """Допускной лист
       :param row: строка
       :param i: номер ячейки
       :param welder: сварщик
       :param with_date: столбик с датой
    """
    admission_sheet = None
    admission_number = row[i].value
    admission_date = None
    if admission_number:
        if with_date:
            # дата - следующая ячейка после номера
            admission_date = row[i+1].value
            admission_date = str(admission_date).strip().replace('г', '')
            admission_date = str_to_date(admission_date)

        admission_number = str(admission_number).strip()
        admission_sheet = AdmissionSheet.objects.filter(number=admission_number).first()
        if not admission_sheet:
            admission_sheet = AdmissionSheet(number=admission_number)
        admission_sheet.welder = welder
        admission_sheet.date = admission_date
        admission_sheet.save()
    return admission_sheet

def analyze_fired_welders():
    """Заполнение базы уволенными сварщиками из эксельки"""
    wb = open_wb(welders_xlsx)
    sheet = None
    for item in wb:
        if item.title in ('Уволенные сварщики-перев.в монт', ):
            sheet = item
    if not sheet:
        logger.info('[ERROR]: sheet not found')
        return

    rows = sheet.rows
    i, header = search_header(rows)
    if header is None:
        logger.info('[ERROR]: header not found')

    materials = [item for item in Material.objects.all()]

    prev_welder = None # для объединенных ячеек
    for row in rows: # Продолжаем обход по генератору
        cell_values = [cell.value for cell in row]
        if not any(cell_values):
            logger.info('EOF reached')
            break

        # Примечание это i+18 ячейка
        notice = get_notice(row, i+18)

        # Сварщик это i+1, клеймо i+2 ячейка
        welder = get_welder(row, i+1, notice, fired = True)
        if welder:
            prev_welder = welder
        else:
            welder = prev_welder

        # Акт ВИК номер это i+3, дата это i+6 ячейка
        vik = get_vik(row, i+3, welder)

        # УЗК/РК номер это i+5, дата это i+6 ячейка
        controlk = get_controlk(row, i+5, welder)

        # Проведение КСС типоразмер это i+7, марка стали это i+8
        # ксс номер это i+10,
        # затрачиваемая длина 150мм*2 это i+9 ячейка
        holding_kss = get_holding_kss(row, i+7, welder,
                                      materials,
                                      holding_choices = None,
                                      spent_length_choices = None,
                                      holding_value = None,
                                      with_spent_len = True)

        # Мехиспытание номер это i+11, дата это i+12 ячейка
        mechtest = get_mechtest(row, i+11, welder)

        # НАКС аттестат номер удостоверения это i+16,
        # способ сварки это i+17 ячейка, годен до это i+18
        # НГДО/СК это i+19, место удостоверения это i+20,
        # полугодовая отметка это i+21
        nax = get_nax(row, i+15, welder, wrong_order = True)

        # Допускной лист номер это i+13
        admission_sheet = get_admission_sheet(row, i+13, welder, with_date = True)


def analyze_welders():
    """Заполнение базы сварщиками из эксельки"""
    wb = open_wb(welders_xlsx)
    sheet = None
    for item in wb:
        if item.title in ('Актуальный список сварщиков', ):
            sheet = item
    if not sheet:
        logger.info('[ERROR]: sheet not found')
        return

    rows = sheet.rows
    i, header = search_header(rows)
    if header is None:
        logger.info('[ERROR]: header not found')

    holding_choices = []
    spent_length_choices = []
    materials = [item for item in Material.objects.all()]

    prev_welder = None # для объединенных ячеек
    prev_holding_value = None # для объединенных ячеек
    prev_welding_type = None # для объединенных ячеек
    for row in rows: # Продолжаем обход по генератору
        cell_values = [cell.value for cell in row]
        if not any(cell_values):
            logger.info('EOF reached')
            break

        # Компания это i+23 ячейка
        company = None
        company_str = row[i+23].value
        if company_str:
            company_str = str(company_str).strip()
            company = Company.objects.filter(name=company_str).first()
            if not company:
                company = Company.objects.create(name=company_str)

        # Примечание это i+24 ячейка
        notice = get_notice(row, i+24)

        # Сварщик это i+3, клеймо i+4 ячейка
        welder = get_welder(row, i+3, notice)
        if welder:
            prev_welder = welder
        else:
            welder = prev_welder

        # Гарантийные письма это i+1 ячейка
        letter_str = row[i+1].value
        if letter_str:
            letter_str = str(letter_str).strip()
            letter = LetterOfGuarantee.objects.filter(name=letter_str).first()
            if not letter:
                letter = LetterOfGuarantee.objects.create(
                    name=letter_str,
                    welder=welder)

        # Акт ВИК номер это i+5, дата это i+6 ячейка
        vik = get_vik(row, i+5, welder)

        # УЗК/РК номер это i+7, дата это i+8 ячейка
        controlk = get_controlk(row, i+7, welder)

        # Проведение КСС типоразмер это i+9, марка стали это i+10
        # ксс номер это i+11, ТТ/МК это i+13 ячейка
        holding_kss = get_holding_kss(row, i+9, welder,
                                      materials,
                                      holding_choices,
                                      spent_length_choices,
                                      holding_value = prev_holding_value,
                                      with_spent_len = False)
        if holding_kss:
            prev_holding_value = holding_kss.state

        # Мехиспытание номер это i+14, дата это i+15 ячейка
        mechtest = get_mechtest(row, i+14, welder)

        # НАКС аттестат номер удостоверения это i+16,
        # способ сварки это i+17 ячейка, годен до это i+18
        # НГДО/СК это i+19, место удостоверения это i+20,
        # полугодовая отметка это i+21
        nax = get_nax(row, i+16, welder, wrong_order = False)

        # Допускной лист номер это i+22
        admission_sheet = get_admission_sheet(row, i+22, welder, with_date = False)

def clear_tables():
    """Очистить таблицы"""
    Welder.objects.all().delete()
    LetterOfGuarantee.objects.all().delete()
    Vik.objects.all().delete()
    ControlK.objects.all().delete()
    HoldingKSS.objects.all().delete()
    MechTest.objects.all().delete()
    NAX.objects.all().delete()
    AdmissionSheet.objects.all().delete()

class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_tables()
        analyze_welders()
        analyze_fired_welders()

