#-*- coding:utf-8 -*-
import datetime
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.flatcontent.models import Containers, Blocks

logger = logging.getLogger('main')


class Command(BaseCommand):
    """Исправление ссылок портфолио"""
    def add_arguments(self, parser):
        parser.add_argument('--fake_action',
            action = 'store',
            dest = 'fake_action',
            type = str,
            default = False,
            help = 'Set fake action')
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Fake action')

    def handle(self, *args, **options):
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




