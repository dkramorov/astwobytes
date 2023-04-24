#-*- coding:utf-8 -*-
import os
import logging
import time
import datetime

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count
from django.db import connections

from apps.main_functions.atomic_operations import bulk_create
from apps.net_tools.models import IPRange, IPAddress
from apps.mongo.base import get_collection
from apps.site.miners.scanner import scan_ips
from apps.site.miners.whatsminer import WhatsMinerApi
from apps.site.miners.models import Comp

logger = logging.getLogger('main')

def rescan(ip_ports):
    collection = get_collection()
    by = 1
    query = IPRange.objects.all()
    ip_ranges = query.aggregate(Count('id'))['id__count']
    pages = int(ip_ranges / by) + 1
    for i in range(pages):
        rows = query[i*by:i*by+by]
        for row in rows:
            ip_range = row.get_ips()
            result = list(scan_ips(ip_range=ip_range, ports=ip_ports, exclude_ips=[]))

            ips = [item['ip'].strip() for item in result if item['open']]
            print('scanned', '(%s)' % row, len(result))

            print('\tlive ips', len(ips))
            exists_ips = IPAddress.objects.filter(ip__in=ips).values_list('ip', flat=True)
            new_ips = []
            for item in ips:
                if not item in exists_ips:
                    new_ips.append(IPAddress(ip=item))
            print('\tnew_ips', len(new_ips))
            bulk_create(IPAddress, new_ips)
            # IPAddress созданы, но Comp просто так не создать, надо ip+mac связку, поэтому сканим api
            exists_ips = IPAddress.objects.filter(ip__in=ips)
            for ip in exists_ips:
                api = WhatsMinerApi(ip=ip.ip, passwd='admin')
                summary = api.exec('summary')
                version = api.exec('get_version')
                psu = api.exec('get_psu')
                dev = api.exec('devdetails')

                collection.insert_one({
                    'ip': ip.ip,
                    'ip_id': ip.id,
                    'action': 'summary',
                    'summary': summary,
                    'version': version,
                    'psu': psu,
                    'dev': dev,
                    'date': datetime.datetime.utcnow(),
                })


class Command(BaseCommand):
    """
       vpn connect then
       sudo route add 10.10.11.0/24 10.10.6.1
       sudo route add 10.10.10.0/24 10.10.6.1
    """
    def add_arguments(self, parser):
        parser.add_argument('--test',
            action = 'store_true',
            dest = 'test',
            default = False,
            help = 'test')
        parser.add_argument('--ip_ports',
            action = 'store',
            dest = 'ip_ports',
            type = str,
            default = False,
            help = 'IP ports separated by comma')

    def handle(self, *args, **options):

        ip_ports = []
        if options.get('ip_ports'):
            ip_ports = [int(port) for port in options['ip_ports'].split(',') if port]
        else:
            ip_ports = [4028]
        for i in range(1):
            rescan(ip_ports)
            time.sleep(1)







