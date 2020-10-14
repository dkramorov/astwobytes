# -*- coding: utf-8 -*-
import logging
import datetime
import re
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file
from apps.main_functions.date_time import str_to_date
from apps.main_functions.api_helper import open_wb

from apps.weld.company_model import Joint, Subject, Titul, Line
from apps.weld.models import WeldingJoint
from apps.weld.scripts_views import search_elements
from apps.weld.conclusion_model import JointConclusion
from apps.weld.enums import (MATERIALS,
                             JOIN_TYPES,
                             WELDING_TYPES,
                             replace_rus2eng,
                             replace_eng2rus, )

logger = logging.getLogger(__name__)

def prepare_migrate_joints():
    """Выполняется только до миграции"""
    f = open_file('migrate_joints.json', 'w+')
    data = []
    for welding_joint in WeldingJoint.objects.select_related('joint').all():
        data.append({
            'id': welding_joint.joint.id,
            'diameter': '%s' % welding_joint.diameter if welding_joint.diameter else None,
            'side_thickness': '%s' % welding_joint.side_thickness if welding_joint.side_thickness else None,
            'welding_date': welding_joint.welding_date.strftime('%Y-%m-%d') if welding_joint.welding_date else None,
        })
    f.write(json.dumps(data))
    f.close()

def migrate_joints():
    """Выполняется после миграции"""
    f = open_file('migrate_joints.json')
    data = json.loads(f.read())
    f.close()
    for welding_joint in data:
        joint = Joint.objects.filter(pk=welding_joint['id']).first()
        if not joint:
            logger.info('joint is absent %s' % welding_joint['id'])
            continue
        if welding_joint['diameter']:
            joint.diameter = welding_joint['diameter']
        if welding_joint['side_thickness']:
            joint.side_thickness = welding_joint['side_thickness']
        joint.welding_date = str_to_date(welding_joint['welding_date'])
        joint.save()

def drop_lines():
    """Удалить все,
       но не надо удалять 920 титул
    """
    for joint in Joint.objects.select_related('line', 'line__titul').exclude(line__titul__name='У920'):
        if not joint.line:
            print('узел', joint.name, 'без линии')
        elif not joint.line.titul:
            print('узел', joint.line.name, joint.name, 'без титула')
        for welding_joint in WeldingJoint.objects.filter(joint=joint):
            for conclusion in JointConclusion.objects.filter(welding_joint=welding_joint):
                conclusion.delete()
            welding_joint.delete()
        joint.delete()
    for line in Line.objects.exclude(titul__name='У920'):
        line.delete()

def load_lines():
    """Загрузка линий"""
    for conclusion in JointConclusion.objects.all():
        conclusion.delete()
    for welding_joint in WeldingJoint.objects.all():
        welding_joint.delete()
    for joint in Joint.objects.all():
        joint.delete()
    for line in Line.objects.all():
        line.delete()
    for titul in Titul.objects.all():
        titul.delete()

    subject = Subject.objects.all().first()
    titul = Titul.objects.create(name='У920', subject=subject)

    wb = open_wb('more_lines.xlsx')
    sheet = wb['Линии']

    rows = sheet.rows
    for row in rows:
        value = row[2].value
        if not value:
            continue
        value = '%s' % value
        value = value.strip()
        line = Line.objects.filter(name=value, titul=titul).first()
        if not line:
            #logger.info('[ERROR]: line not found %s' % value)
            Line.objects.create(name=value, titul=titul)

def search_choice(text, choices):
    """Поиск текста в списке
       :param text: искомый текст
       :param choices: список вариантов выбора для модели
    """
    for choice in choices:
        if choice[1] == text:
            return choice[0]

def load_titul():
    cur_titul = Titul.objects.filter(name='У920').first()
    if not cur_titul:
        logger.info('[ERROR]: titul У920 not found')
        return
    i = 0
    wb = open_wb('920.xlsx')
    sheet = wb.active
    rows = sheet.rows
    for row in rows:
        if i < 2:
            i += 1
            continue
        cell_values = [cell.value for cell in row]
        line_str = cell_values[0].strip()
        joint_str = '%s' % cell_values[1]
        joint_str = joint_str.strip()
        stigma = None
        if cell_values[2]:
            stigma = cell_values[2].strip()
        material = cell_values[3].strip()
        diameter = '%s' % cell_values[4]
        diameter = diameter.strip().replace(',', '.')
        side_thickness = '%s' % cell_values[5]
        side_thickness = side_thickness.strip().replace(',', '.')
        welding_date = '%s' % cell_values[6]
        welding_date = welding_date.strip()
        if welding_date.endswith('/20'):
            welding_date = '%s2020' % welding_date[:-2]
        welding_date = str_to_date(welding_date)
        welding_type = cell_values[7].strip()
        conn_view = cell_values[8].strip()
        el1 = cell_values[9].strip()
        el2 = cell_values[10].strip()

        line = Line.objects.filter(name=line_str).first()
        if line:
            joint = Joint.objects.filter(name=joint_str, line=line).first()
            if not joint:
                joint = Joint(
                    line=line,
                    name=joint_str,
                )
            joint.diameter = diameter
            joint.side_thickness = side_thickness
            joint.welding_date = welding_date
            joint.material = search_choice(replace_eng2rus(material.upper()), MATERIALS)
            joint.welding_type = search_choice(replace_eng2rus(welding_type.upper()), WELDING_TYPES)
            joint.welding_conn_view = search_choice(replace_eng2rus(conn_view.upper()), Joint.welding_conn_view_choices)
            joint.join_type_from = search_choice(replace_eng2rus(el1.lower()), JOIN_TYPES)
            joint.join_type_to = search_choice(replace_eng2rus(el2.lower()), JOIN_TYPES)
            joint.save()
        else:
            print('линия не найдена %s стык %s' % (line_str, joint_str))

def test_search_elements():
    """Преобразуем текст в 2 элемента
       Труба 57х5 – Тройник П 57х5
       Тройник П 57х5 – Переход ПК 57х5-32х5
       Переход ПК 57х5-32х4,5 – Труба 32х4,5
    """
    demo_data = (
        ('Труба 57х5 –', 'Тройник П 57х5'),
        ('Тройник П 57х5 –', 'Переход ПК 57х5-32х5'),
        ('Переход ПК 57х5-32х4,5 –', 'Труба 32х4,5'),
        ('Тройник П 108х6 –', 'Переход П К 108х6/8-57х5'),
        ('Штуцер 25-10,0– ', 'Фланец'),
    )
    for item in demo_data:
        print(search_elements(item))

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('')
        #load_lines()
        #load_titul()
        test_search_elements()