#-*- coding:utf-8 -*-
import os
import time
import logging
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file, copy_file

logger = logging.getLogger(__name__)

default_folder = settings.MEDIA_ROOT

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--demo_mode',
            action = 'store_true',
            dest = 'demo_mode',
            default = False,
            help = 'Set demo mode')
        parser.add_argument('--cat_id',
            action = 'store',
            dest = 'cat_id',
            type = str,
            default = False,
            help = 'Set cat tag for update')

    def handle(self, *args, **options):
        started = time.time()

        rubrics_file = '2gis/rubrics.json'
        with open_file(rubrics_file, 'r', encoding='utf-8') as f:
            rubrics = json.loads(f.read())
        create_rubrics(rubrics)

def create_rubrics(rubrics: dict, parent: Blocks = None):
    """Создание дерева рубрик
       :param rubrics: дерево рубрик словарем
       :param parent: родительская рубрика
    """
    catalogue = Containers.objects.filter(tag='catalogue').first()
    if not catalogue:
        catalogue = Containers.objects.create(name='Каталог компаний', tag='catalogue', state=7)
    for rubric_name, data in rubrics.items():
        parents = ''
        if parent:
            parents = '%s_%s' % (parent.parents, parent.id)
        rubric = Blocks.objects.filter(tag=data['id'],
                                       parents=parents,
                                       state=4,
                                       container=catalogue).first()
        if not rubric:
            rubric = Blocks.objects.create(tag=data['id'],
                                           name=data['rname'],
                                           parents=parents,
                                           state=4,
                                           container=catalogue)
        icon = data.get('icon_url')
        #if icon:
        #    icon_name = os.path.split(icon)[-1]
        #    Blocks.objects.filter(pk=rubric.id).update(class_name=icon_name)
        if icon and not rubric.img:
            icon_name = os.path.split(icon)[-1]
            source = os.path.join('2gis_icons', icon_name)
            imga = '%s.svg' % rubric.id
            dest = os.path.join(rubric.get_folder(), imga)
            copy_file(source, dest)
            Blocks.objects.filter(pk=rubric.id).update(img=imga, class_name=icon_name)

        if 'subrubrics' in data and data['subrubrics']:
            create_rubrics(data['subrubrics'], rubric)

