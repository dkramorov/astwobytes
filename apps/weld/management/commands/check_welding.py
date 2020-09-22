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
from apps.weld.conclusion_model import JointConclusion

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

def drop_till_september():
    """Удалить все до сентября 20,
       но не надо удалять 920 титул
    """
    sept = datetime.date(2020, 9, 1)
    for joint in Joint.objects.select_related('line', 'line__titul').filter(Q(welding_date__lt=sept)|Q(welding_date__isnull=True)|Q(name__startswith='\'')):
        if not joint.line:
            print('узел', joint.name, 'без линии')
        elif not joint.line.titul:
            print('узел', joint.line.name, joint.name, 'без титула')
        elif joint.line.titul.name == 'У920':
            print('Не удаляем', joint.line.titul.name, 'узел', joint.line.name, joint.name, 'дата сварки', joint.welding_date)
            continue
        for welding_joint in WeldingJoint.objects.filter(joint=joint):
            for conclusion in JointConclusion.objects.filter(welding_joint=welding_joint):
                conclusion.delete()
            welding_joint.delete()
        joint.delete()

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
    wb = open_wb('more_lines.xlsx')
    sheet = wb.active
    rows = sheet.rows
    cur_titul = None
    for row in rows:
        value = row[1].value
        if not value:
            continue
        value = '%s' % value
        value = value.strip()
        if value.startswith('У'):
            titul = Titul.objects.filter(name=value).first()
            if not titul:
                #logger.info('[ERROR]: titul not found %s' % value)
                cur_titul = Titul.objects.create(name=value, subject=subject)
            else:
                cur_titul = titul
        else:
            if not cur_titul:
                continue
            line = Line.objects.filter(name=value).first()
            if not line:
                #logger.info('[ERROR]: line not found %s' % value)
                cur_line = Line.objects.create(name=value, titul=cur_titul)
            else:
                cur_line = line

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
        line_str = cell_values[1].replace('ЖСР', '').strip()
        joint_str = '%s' % cell_values[2]
        joint_str = joint_str.strip()
        diameter = '%s' % cell_values[5]
        diameter = diameter.strip().replace(',', '.')
        side_thickness = '%s' % cell_values[6]
        side_thickness = side_thickness.strip().replace(',', '.')
        welding_date = '%s' % cell_values[6]
        welding_date = welding_date.strip()
        welding_date = str_to_date(welding_date)

        line = Line.objects.filter(name=line_str).first()
        if line:
            joint = Joint.objects.filter(name=joint_str, line=line).first()
            if not joint:
                Joint.objects.create(
                    line=line,
                    name=joint_str,
                    diameter=diameter,
                    side_thickness=side_thickness,
                    welding_date=welding_date,
                )
        else:
            print('линия не найдена %s стык %s' % (line_str, joint_str))

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('')
        #prepare_migrate_joints()
        #migrate_joints()
        #drop_till_september()
        #load_lines()
        load_titul()