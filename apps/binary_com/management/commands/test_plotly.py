#-*- coding:utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from apps.binary_com.plotly_builder import save_with_plotly
from apps.telegram.telegram import TelegramBot
from apps.main_functions.files import open_file, drop_file

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
        ticks_data = []

        output_img = save_with_plotly(ticks=ticks_data, image='png')
        with open_file(output_img, 'r') as f:
            TelegramBot().send_photo(f)
        if output_img.endswith('.png'):
            drop_file(output_img)
