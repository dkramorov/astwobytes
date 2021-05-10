#-*- coding:utf-8 -*-
import logging

import xml.sax

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print

logger = logging.getLogger(__name__)

class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.all_tags = []
        self.opened_tags = []

        self.tags_tree = {}

    def startElement(self, tag, attributes):
        if not tag in self.all_tags:
            self.all_tags.append(tag)

        cur_node = None
        for item in self.opened_tags:
            if not cur_node:
                cur_node = self.tags_tree[item]
            else:
                cur_node = cur_node[item]

        if not cur_node:
            self.tags_tree[tag] = {}
        else:
            cur_node[tag] = {}

        self.opened_tags.append(tag)


    def endElement(self, tag):
        if self.opened_tags and not tag == self.opened_tags[-1]:
            print("[ERROR]: XML NOT VALID")
            exit()
        self.opened_tags.pop()

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
        parser = xml.sax.make_parser()
        xml_handler = XMLHandler()
        parser.setContentHandler(xml_handler)
        parser.parse('/home/jocker/Documents/SEVA/1cv8_unloading.xml')
        #print(json_pretty_print(xml_handler.all_tags))
        print(json_pretty_print(xml_handler.tags_tree))
