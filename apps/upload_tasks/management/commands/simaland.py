#-*- coding:utf-8 -*-
import json
import time
import logging
import datetime
import requests

from lxml import html

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.upload_tasks.simaland import SimaLand
from apps.products.models import (
    Products,
    ProductsPhotos,
    ProductsCats,
    Property,
)

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
        """Выгрузка товаров sima-land.ru"""
        #Products.objects.all().delete()

        simaland = SimaLand()
        simaland.get_jwt()
        #cart = simaland.get_cart()
        #print(json_pretty_print(cart))

        #print(simaland.add2cart(cart_id=cart['_cart']['cart_id'], items=[{'item_id': 8392, 'qty': 1}, ]))


        #simaland.get_categories()

        #started = time.time()
        #simaland.get_products()
        print(json_pretty_print(simaland.get_product(product_id=4119069)))
        #elapsed = time.time() - started
        #print('[ELAPSED]', '%.2f' % elapsed)

        #simaland.get_product(8282)
        #simaland.get_units()
        #print(simaland.units)

        #Property.objects.all().delete()
        #simaland.get_props()
        #simaland.get_attrs()
