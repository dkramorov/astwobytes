#-*- coding:utf-8 -*-
import logging

import xml.sax

from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)

class RRHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.isOffers = False
        self.isOffer = False
        self.ids = {}
        self.position = 0
        self.first_duplicate_position = 0

    def startElement(self, tag, attributes):
        if self.isOffers:
            if tag == 'offer':
                self.position += 1
                self.isOffer = True
                product_id = attributes.get('id')
                if product_id in self.ids:
                    if not self.first_duplicate_position:
                        self.first_duplicate_position = self.position
                    return
                self.ids[product_id] = True
        elif tag == 'offers':
            self.isOffers = True

    def endElement(self, tag):
        if tag == 'offer':
            self.isOffer = False
        elif tag == 'offers':
            self.isOffers = False

    def characters(self, content):
        pass

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
        feeds = ('9o8.xml', '91u1.xml', 'b831.xml')

        parser = xml.sax.make_parser()
        rr_handler = RRHandler()
        parser.setContentHandler(rr_handler)
        parser.parse('/Users/jocker/Downloads/%s' % feeds[0])
        print(len(rr_handler.ids), rr_handler.first_duplicate_position)

        parser = xml.sax.make_parser()
        rr_handler = RRHandler()
        parser.setContentHandler(rr_handler)
        parser.parse('/Users/jocker/Downloads/%s' % feeds[1])
        print(len(rr_handler.ids), rr_handler.first_duplicate_position)

        parser = xml.sax.make_parser()
        rr_handler = RRHandler()
        parser.setContentHandler(rr_handler)
        parser.parse('/Users/jocker/Downloads/%s' % feeds[2])
        print(len(rr_handler.ids), rr_handler.first_duplicate_position)


