#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.upload_tasks.vkontakte import VK

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--start',
            action = 'store',
            dest = 'start',
            type = str,
            default = False,
            help = 'Set start date')
        parser.add_argument('--end',
            action = 'store',
            dest = 'end',
            type = str,
            default = False,
            help = 'Set end date')

    def handle(self, *args, **options):
        """Выгрузка товаров на vkontakte"""
        group_1 = 81179930
        group_2 = 120157851

        vk = VK(group_id = group_1)
        #print(json_pretty_print(vk.get_categories()))
        #return
        category_id = 404

        # Например,
        img_path = 'images/dashboard-header.jpg'
        extra_images = ['images/poster.jpg', 'placeholder02.jpg', 'placeholder01.jpg']
        print(vk.drop_product(4605552))
        return
        print(vk.new_product(img_path, extra_images,
                    category_id, 0.3, 0.6,
                    'Супер товар', 'Только сегодня такое выгодное предложение',
                    False))
        #print(vk.edit_product(4008148, extra_images[0], extra_images,
        #                      category_id, 0.6, 0.9,
        #                      'Супер товар2', 'Только сегодня такое выгодное предложение2',
        #                      False))

