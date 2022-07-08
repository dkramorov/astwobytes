#-*- coding:utf-8 -*-
import os
import datetime
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import extension, copy_file
from apps.flatcontent.models import Containers, Blocks, LinkContainer

logger = logging.getLogger('main')

def fix_links():
    main_container = Containers.objects.filter(tag='mainmenu', state=1).first()
    portfolio_container = Containers.objects.filter(tag='portfolio', state=1).first()
    portfolio_menus = portfolio_container.blocks_set.filter(parents='')
    for portfolio_menu in portfolio_menus:
        main_menu = main_container.blocks_set.filter(link=portfolio_menu.link).first()

        submenus = Blocks.objects.filter(parents='%s_%s' % (portfolio_menu.parents, portfolio_menu.id)).order_by('position')
        for submenu in submenus:
            submenu.container = main_container
            submenu.parents = '%s_%s' % (main_menu.parents, main_menu.id)
            if not submenu.link.startswith('/portfolio/'):
                submenu.link = '/portfolio%s' % (submenu.link)
            submenu.save()

        linked2main_menu = main_menu.linkcontainer_set.select_related('container').all().first()

        linked = linked2main_menu.container.blocks_set.filter(link__isnull=False).exclude(link='').order_by('position')
        for i, subitem in enumerate(linked):
            print(submenus, subitem)
            if not subitem.link.startswith('/portfolio/'):
                subitem.link = '/portfolio%s' % (subitem.link)
                subitem.save()

def fix_menu_photos():
    """Обновление фоток с квадратанов на прямоугольник"""
    portfolio_menu = Blocks.objects.filter(tag='portfolio', link='/portfolio/', state=4).first()
    menus = Blocks.objects.filter(parents='%s_%s' % (portfolio_menu.parents, portfolio_menu.id))
    for menu in menus:
        # На этом уровне привязан контейнер с работами, в них правильный порядок
        link_positions = []
        portfolio = {}
        menu_container = LinkContainer.objects.select_related('container').filter(block=menu).first()
        if menu_container:
            menu_blocks = menu_container.container.blocks_set.all()
            for menu_block in menu_blocks:
                if not menu_block.img:
                    continue
                link_positions.append(menu_block.link)
                portfolio[menu_block.link] = menu_block
        #print(portfolio)
        submenus = Blocks.objects.filter(parents='%s_%s' % (menu.parents, menu.id))
        if not submenus:
            print(menu.name, 'passing')
            continue
        position = 1
        for submenu in submenus:
            submenu.drop_img()
            link = LinkContainer.objects.select_related('container').filter(block=submenu).first()
            container = link.container
            container.tag = 'project2'
            container.save()
            # Берем из первого блока картинку и ее подставляем в менюшку
            block = container.blocks_set.filter(img__isnull=False).order_by('position').first()
            block_text = container.blocks_set.filter(img__isnull=True).order_by('position').first()

            src = os.path.join(block.get_folder(), block.img)
            ext = extension(block.img)
            img_name = '%s%s' % (submenu.id, ext)
            dest = os.path.join(submenu.get_folder(), img_name)

            copy_file(src, dest)
            submenu.img = img_name
            pos = link_positions.index(submenu.link) + 1
            submenu.html = block_text.html
            submenu.class_name = 'portfolio'
            submenu.position = pos
            submenu.save()

            # Квадратные фотки меняем на прямоуголки из портфолио
            portfolio_block = portfolio[submenu.link]
            portfolio_block.drop_img()
            img_name = '%s%s' % (portfolio_block.id, ext)
            dest = os.path.join(portfolio_block.get_folder(), img_name)
            copy_file(src, dest)
            portfolio_block.img = img_name
            portfolio_block.save()
            #print(portfolio_block.id, src)

class Command(BaseCommand):
    """Исправление портфолио"""
    def add_arguments(self, parser):
        parser.add_argument('--fake_str',
            action = 'store',
            dest = 'fake_str',
            type = str,
            default = False,
            help = 'Set fake str')
        parser.add_argument('--fix_links',
            action = 'store_true',
            dest = 'fix_links',
            default = False,
            help = 'Fix portfolio links')
        parser.add_argument('--fix_menu_photos',
            action = 'store_true',
            dest = 'fix_menu_photos',
            default = False,
            help = 'Fix portfolio menu photos')

    def handle(self, *args, **options):
        if options.get('fix_links'):
            fix_links()
        if options.get('fix_menu_photos'):
            fix_menu_photos()




