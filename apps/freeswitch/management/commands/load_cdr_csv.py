# -*- coding: utf-8 -*-
import logging
import time

from django.db.models import Count
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.fortasks import search_process
from apps.freeswitch.services import analyze_logs
from apps.freeswitch.models import Redirects, CdrCsv, PhonesWhiteList

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--link_redirects2clients',
            action = 'store_true',
            dest = 'link_redirects2clients',
            default = False,
            help = 'Link all redirects calls to client from PhonesWhiteList')
        parser.add_argument('--fix_redirects2clients',
            action = 'store_true',
            dest = 'fix_redirects2clients',
            default = False,
            help = 'Fix all redirects calls to client from PhonesWhiteList')
        #parser.add_argument('--single',
        #    action = 'store_true',
        #    dest = 'single',
        #    default = False,
        #    help = 'Send to single account')
    def handle(self, *args, **options):
        """Загрузка cdr_csv информации о звонках в базу"""
        is_running = search_process(q = ('load_cdr_csv', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        # Разовая операция, нужна, чтобы привязать
        # звонки на наши номера, например, 73952546133,
        # а в белом списке этот телефон стоит как 83952546133
        if options.get('link_redirects2clients'):
            # Достаем и подготавливаем редиректы
            redirects = Redirects.objects.all().values_list('phone', flat=True)
            redirects = [kill_quotes(redirect, 'int') for redirect in redirects]
            redirects = ['7%s' % redirect[1:] for redirect in redirects]
            rows = CdrCsv.objects.filter(dest__in=redirects, client_id__isnull=True).values('id', 'dest')
            for row in rows:
                dest = '8%s' % row['dest'][1:]
                client = PhonesWhiteList.objects.filter(phone=dest).first()
                if client:
                    CdrCsv.objects.filter(pk=row['id']).update(client_id=client.tag, client_name=client.name)
                    print(row['id'], row['dest'], client.name, client.tag)
            return

        # Разовая операция, нужна, чтобы задать правильный путь
        # для звонков через переадресацию, т/к они встают как uuid
        # без пути к файлу и расширения
        if options.get('fix_redirects2clients'):
            # Достаем и подготавливаем редиректы
            redirects = Redirects.objects.all().values_list('phone', flat=True)
            redirects = [kill_quotes(redirect, 'int') for redirect in redirects]
            print(redirects)
            rows = CdrCsv.objects.filter(dest__in=redirects, context='redirects_context')
            for row in rows:
                new_dest = '7%s' % row.dest[1:]
                CdrCsv.objects.filter(pk=row.id).update(dest=new_dest)
                print(row.id, new_dest)
            return

        analyze_logs()

        # ----------------------------
        # Определяем нахер че за фирма
        # ----------------------------
        #company = db.get_company_by_phone(new_cdr.dest)
        #if company:
            #new_cdr.client_id = company['id']
            #new_cdr.client_name = company['name']
