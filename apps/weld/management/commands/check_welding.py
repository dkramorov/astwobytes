# -*- coding: utf-8 -*-
import logging
import re
import json

from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file
from apps.main_functions.date_time import str_to_date

from apps.weld.company_model import Joint
from apps.weld.models import WeldingJoint

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

class Command(BaseCommand):
    def handle(self, *args, **options):
        #prepare_migrate_joints()
        migrate_joints()
