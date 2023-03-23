#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import os
import logging

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count
from django.db import connections

from apps.main_functions.atomic_operations import bulk_create
from apps.net_tools.models import IPAddress
from apps.site.miners.scanner import scan_ips

logger = logging.getLogger('main')

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
        parser.add_argument('--cache_key',
            action = 'store',
            dest = 'cache_key',
            type = str,
            default = False,
            help = 'Cache key for receive result')
        parser.add_argument('--ip_range',
            action = 'store',
            dest = 'ip_range',
            type = str,
            default = False,
            help = 'IP addresses separated by dash')
        parser.add_argument('--exclude_ips',
            action = 'store',
            dest = 'exclude_ips',
            type = str,
            default = False,
            help = 'IP addresses separated by comma for exclude from ip_range')
        parser.add_argument('--ip_ports',
            action = 'store',
            dest = 'ip_ports',
            type = str,
            default = False,
            help = 'IP ports separated by comma')

    def handle(self, *args, **options):
        cache_key = 'scanner_ports_result'
        #print('cache: ', cache.get(cache_key))
        if options.get('cache_key'):
            cache_key = options['cache_key']
        ip_range = []
        if options.get('ip_range'):
            #ip_range = make_list_from_range(options['ip_range'])
            ip_range = options['ip_range']
        ip_ports = []
        if options.get('ip_ports'):
            ip_ports = [int(port) for port in options['ip_ports'].split(',') if port]
        exclude_ips = []
        if options.get('exclude_ips'):
            exclude_ips = [int(port) for port in options['exclude_ips'].split(',') if port]

        result = scan_ips(ip_range=ip_range, ports=ip_ports, exclude_ips=exclude_ips)
        ips = [item['ip'].strip() for item in result if item['open']]
        exists_ips = IPAddress.objects.filter(ip__in=ips).values_list('ip', flat=True)
        new_ips = []
        for item in ips:
            if not item in exists_ips:
                new_ips.append(IPAddress(ip=item))
        bulk_create(IPAddress, new_ips)
        cache_value = [item.ip for item in new_ips]
        cache.set(cache_key, cache_value)
        print('cache: ', cache.get(cache_key))




