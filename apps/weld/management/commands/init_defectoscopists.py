# -*- coding: utf-8 -*-
import logging
import re

from openpyxl import load_workbook
from io import BytesIO

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.weld.welder_model import Defectoscopist

logger = logging.getLogger(__name__)

people = (
    ('Латюк С.В.', '0048-1962'),
    ('Болдырев М.А.', '0033-33733-2017'),
    ('Некрасов И.И.', '0048-1961'),
    ('Болотин С.В.', '0023-00-6040'),
    ('Масалов Р.В.', '0039-2759'),
    ('Кривокорытов С.Н.', 'НОАП-0001-61024'),
    ('Литвиннов Е.А.', '0005-03-8958'),
    ('Демин И.П.', '0034-39782-2019'),
    ('Проскоков Н.В.', 'НОАП-0001-57504'),
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for human in people:
            analog = Defectoscopist.objects.filter(stigma=human[1]).first()
            if not analog:
                Defectoscopist.objects.create(name=human[0], stigma=human[1])


