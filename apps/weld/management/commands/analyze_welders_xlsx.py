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
        notice = row[i+24].value
        if notice:
            notice = notice.strip()

        # Сварщик это i+3, клеймо i+4 ячейка
        welder_str = row[i+3].value
        stigma = row[i+4].value
        if welder_str and stigma:
            welder_str = str(welder_str).strip()
            stigma = str(stigma).strip()
            welder = Welder.objects.filter(name=welder_str).first()
            if not welder:
                welder = Welder()
            welder.name = welder_str
            welder.stigma = stigma
            welder.company = company
            welder.notice = notice
            welder.save()

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
        vik_number = row[i+5].value
        vik_date = row[i+6].value
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

        # УЗК/РК номер это i+7, дата это i+8 ячейка
        control_number = row[i+7].value
        control_date = row[i+8].value
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

        # Проведение КСС типоразмер это i+9, марка стали это i+10
        # ксс номер это i+11, ТТ/МК это i+13 ячейка
        standard_size = row[i+9].value
        steel = row[i+10].value
        kss_number = row[i+11].value
        if kss_number:
            kss_number = str(kss_number).strip()
        kss_state = row[i+13].value
        if kss_state:
            kss_state = str(kss_state).strip()
        if standard_size and steel:
            standard_size = str(standard_size).strip()
            steel = str(steel).strip()
            steel = replace_eng2rus(steel)

            if not kss_state in holding_choices:
                holding_choices.append(kss_state)
            material = None
            for item in materials:
                if item.name == steel:
                    material = item
                    break
            if not material:
                material = Material.objects.create(name=steel)
                materials.append(material)
            holding_state = None
            for holding_choice in HoldingKSS.holding_choices:
                if holding_choice[1] == kss_state:
                    holding_state = holding_choice[0]
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
                holding_kss.number = kss_number
                holding_kss.state = holding_state
                holding_kss.save()

        # Мехиспытание номер это i+14, дата это i+15 ячейка
        mechtest_number = row[i+14].value
        mechtest_date = row[i+15].value
        if mechtest_number and mechtest_date:
            mechtest_number = str(mechtest_number).strip()
            mechtest_date = str(mechtest_date).strip().replace('г', '')
            mechtest_date = str_to_date(mechtest_date)
            mechtest = MechTest.objects.filter(number=mechtest_number).first()
            if not mechtest:
                mechtest = MechTest(number=mechtest_number)
            mechtest.date = control_date
            mechtest.welder = welder
            mechtest.save()

        # НАКС аттестат номер удостоверения это i+16,
        # способ сварки это i+17 ячейка, годен до это i+18
        # НГДО/СК это i+19, место удостоверения это i+20,
        # полугодовая отметка это i+21
        nax_number = row[i+16].value
        nax_welding_type = row[i+17].value
        nax_best_before = row[i+18].value
        nax_acl = row[i+19].value
        nax_identification = row[i+20].value
        nax_half_year_mark = row[i+21].value
        if nax_number and nax_best_before and nax_welding_type:
            number = str(nax_number).strip()
            nax_welding_type = str(nax_welding_type).strip().replace(' ', '')
            nax_best_before = str(nax_best_before).strip().replace('г', '')
            nax_acl = str(nax_acl).strip()
            nax_identification = str(nax_identification).strip()
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

        # Допускной лист номер это i+22
        admission_number = row[i+22].value
        if admission_number:
            admission_number = str(admission_number).strip()
            admission_sheet = AdmissionSheet.objects.filter(number=admission_number).first()
            if not admission_sheet:
                admission_sheet = AdmissionSheet(number=admission_number)
            admission_sheet.welder = welder
            admission_sheet.save()

class Command(BaseCommand):
    def handle(self, *args, **options):
        Material.objects.all().delete()
        #Company.objects.all().delete()
        #Welder.objects.all().delete()
        analyze_welders()

