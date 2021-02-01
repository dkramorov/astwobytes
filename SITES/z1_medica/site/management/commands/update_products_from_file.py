#-*- coding:utf-8 -*-
import os
import logging
import xml.sax
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.string_parser import kill_quotes
from apps.products.models import Products

logger = logging.getLogger(__name__)


class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.isPrice = False
        self.isProduct = False
        self.Price = 'Прайс'
        self.Product = 'Товар'
        self.Name = 'Номенклатура'
        self.Articul = 'Артикул'
        self.Count = 'Количество'
        self.Manufacturer = 'Производитель'
        self.Cost = 'Цена'
        self.updated = []


    def update_product(self, attributes):
        """Обновление товара
           :param attributes: атрибуты товара
        """
        articul = '_%s' % attributes.get(self.Articul)
        count = attributes.get(self.Count)
        manufacturer = attributes.get(self.Manufacturer)
        price = attributes.get(self.Cost)
        price = kill_quotes(price, 'int')
        price = price.replace(',', '.')
        name = attributes.get(self.Name)
        analog = Products.objects.filter(code=articul).first()
        if not analog:
            #logger.info('[ERROR]: product not exists: %s' % articul)
            return
        params = {
            'name': name,
            'count': count,
            'price': price,
            'manufacturer': manufacturer,
        }
        Products.objects.filter(pk=analog.id).update(**params)
        self.updated.append(analog.id)

    def startElement(self, tag, attributes):
        if self.isPrice:
            if tag == self.Product:
                self.isProduct = True
                self.update_product(attributes)
        elif tag == self.Price:
            self.isPrice = True

    def endElement(self, tag):
        if tag == self.Price:
            self.isPrice = False
        elif tag == self.Product:
            self.isProduct = False

    def characters(self, content):
        pass

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
        #path = '/home/jocker/Downloads/price.xml'
        path = '/home/d/dsarhirus/obmen/price/Price_{}.xml' # 28.01.2021
        now = datetime.date.today()
        path = path.format(now.strftime('%d.%m.%Y'))
        if not os.path.exists(path):
            logger.info('[ERROR]: file %s not exists' % path)
            return

        parser = xml.sax.make_parser()
        handler = XMLHandler()
        parser.setContentHandler(handler)
        parser.parse(path)
        logger.info('[UPDATED]: %s' % handler.updated)


