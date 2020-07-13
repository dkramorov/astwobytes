# -*- coding: utf-8 -*-
import os
import logging
import json
import shutil

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.main_functions.functions import object_fields
from apps.main_functions.files import (make_folder,
                                       copy_file,
                                       open_file,
                                       check_path,
                                       ListDir,
                                       isForD, )
from apps.flatcontent.models import Containers, Blocks

logger = logging.getLogger(__name__)

def export_templates():
    """Экспорт шаблонов"""
    templates = Containers.objects.filter(state__in=(99, 100), tag__isnull=False)
    for template in templates:
        make_folder('export')
        path = os.path.join('export', template.tag)
        make_folder(path)
        if template.img:
            copy_file(os.path.join(template.get_folder(), template.img),
                      os.path.join(path, template.img)
            )
        obj = object_fields(template)
        obj['blocks'] = []
        blocks = template.blocks_set.all()
        blocks_path = os.path.join(path, 'blocks')
        make_folder(blocks_path)
        for block in blocks:
            if block.img:
                copy_file(os.path.join(block.get_folder(), block.img),
                          os.path.join(blocks_path, block.img)
                )
            obj['blocks'].append(object_fields(block, pass_fields=('container', )))

        json_path = os.path.join(path, 'template.json')
        with open_file(json_path, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(obj))

        template_fname = '%s.html' % template.tag
        template_src = os.path.join(settings.BASE_DIR,
                                    'apps/site/templates/web/containers/',
                                    template_fname)
        template_dest = os.path.join(settings.MEDIA_ROOT, path, template_fname)
        shutil.copy2(template_src, template_dest)

def recursive_fill_blocks(container,
                          blocks: list,
                          parent_block,
                          parents: str,
                          blocks_path: str):
    """Рекурсивное создание блоков контейнера
       :param container: контейнер блоков
       :param blocks: блоки, которые надо создать в контейнере
       :param parent_block: родительский блок
       :param parents: родительский блок
       :param blocks_path: путь к изображениям блоков
    """
    for json_obj in blocks:
        if not parents == json_obj['parents']:
            continue
        block = Blocks(container=container)
        for k, v in json_obj.items():
            if k in ('img', 'id', 'parents', 'container'):
                continue
            setattr(block, k, v)
        if parent_block:
            parents = parent_block.parents or ''
            parents += '_%s' % parent_block.id
            block.parents = parents
        block.save()
        imga = json_obj.get('img')
        if imga:
            copy_file(os.path.join(blocks_path, imga),
                      os.path.join(block.get_folder(), imga)
            )
            Blocks.objects.filter(pk=block.id).update(img=imga)
        # Теперь надо найти подблоки этого блока
        recursive_fill_blocks(container,
                              blocks,
                              block,
                              '%s_%s' % (json_obj['parents'], json_obj['id']),
                              blocks_path)

def import_templates():
    """Импорт шаблонов"""
    import_path = 'import'
    if check_path(import_path):
        logger.info('[ERROR]: There is not folder import in media')
        return
    for item in ListDir(import_path):
        template_path = os.path.join(import_path, item)
        json_path = os.path.join(template_path, 'template.json')
        blocks_path = os.path.join(template_path, 'blocks')
        with open_file(json_path, 'r', encoding='utf-8') as f:
            json_obj = json.loads(f.read())
        template = Containers.objects.filter(tag=json_obj['tag'], state=json_obj['state']).first()
        if not template:
            template = Containers()
            for k, v in json_obj.items():
                if k in ('blocks', 'img', 'id', 'position'):
                    continue
                setattr(template, k, v)
            template.save()
        if not template.img:
            imga = json_obj.get('img')
            if imga:
                src = os.path.join(template_path, imga)
                dest = os.path.join(template.get_folder(), imga)
                copy_file(src, dest)
                Containers.objects.filter(pk=template.id).update(img=imga)
        blocks = json_obj.get('blocks')
        if template.blocks_set.all().aggregate(Count('id'))['id__count'] > 0:
            #logger.info('pass template %s, it is already with blocks' % template.tag)
            pass
        else:
            recursive_fill_blocks(template, blocks, None, None, blocks_path)

        template_fname = '%s.html' % template.tag
        template_src = os.path.join(settings.MEDIA_ROOT, template_path, template_fname)
        template_dest = os.path.join(settings.BASE_DIR,
                                     'apps/site/templates/web/containers/',
                                     template_fname)
        if not os.path.exists(template_dest):
            shutil.copy2(template_src, template_dest)



class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--export',
            action = 'store_true',
            dest = 'export',
            default = False,
            help = 'Export templates')
        parser.add_argument('--import',
            action = 'store_true',
            dest = 'import',
            default = False,
            help = 'Import templates')
    def handle(self, *args, **options):
        """Экспорт/Импорт шаблонов"""
        if options.get('export'):
            export_templates()
        if options.get('import'):
            import_templates()


