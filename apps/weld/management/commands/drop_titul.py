# -*- coding: utf-8 -*-
import logging
import datetime
import re
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.weld.company_model import Joint, Titul, Line

logger = logging.getLogger(__name__)

def drop_titul(titul_name: str):
    """Удалить все по титулу,
       но сам титул удалять не надо
       :param titul_name: название титула
    """
    titul = Titul.objects.filter(name=titul_name).first()
    if not titul:
        logger.info('Titul not found')
        return
    for line in titul.line_set.all():
        for joint in line.joint_set.all():
            joint.delete()
        line.delete()
    titul.delete()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--titul',
            action = 'store',
            dest = 'titul',
            type = str,
            default = False,
            help = 'Set titul for drop')
    def handle(self, *args, **options):
        if options.get('titul'):
            drop_titul(options['titul'])