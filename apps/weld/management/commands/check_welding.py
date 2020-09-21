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

from apps.weld.company_model import Joint
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

class Command(BaseCommand):
    def handle(self, *args, **options):
        #prepare_migrate_joints()
        #migrate_joints()
        drop_till_september()
