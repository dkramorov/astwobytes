#-*- coding:utf-8 -*-
import os
import logging
import time
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count
from django.db import connections

from apps.main_functions.atomic_operations import bulk_create
from apps.main_functions.catcher import json_pretty_print
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

            ips = {item['ip'].strip(): item for item in result if item['open']}
            print('scanned', '(%s)' % row, len(result))
            print('\tlive ips', len(ips))

            new_ips = []
            for item in ips:
                mac = None
                for iface in ips[item].get('lan', []):
                    mac = iface.get('macaddr')
                addresses = IPAddress.objects.filter(ip=item)
                found = False
                for address in addresses:
                    if address.mac == mac:
                        found = True
                        break
                    if not address.mac:
                        found = True
                        IPAddress.objects.filter(pk=address.id).update(mac=mac)
                        break
                if not found:
                    new_ips.append(IPAddress(ip=item, mac=mac))

            print('\tnew_ips', len(new_ips))
            bulk_create(IPAddress, new_ips)
            # IPAddress созданы, но Comp просто так не создать, надо ip+mac связку, поэтому сканим api
            exists_ips = IPAddress.objects.filter(ip__in=ips.keys())
            for ip in exists_ips:
                api = WhatsMinerApi(ip=ip.ip, passwd='admin')
                summary = api.exec('summary')
                version = api.exec('get_version')
                psu = api.exec('get_psu')
                dev = api.exec('edevs')

                print('--summary--', ip, summary)
                print('--version--', ip, version)
                print('--psu--', ip, psu)
                print('--dev--', ip, dev)

                comp = Comp.objects.filter(ip=ip).first()
                if not comp:
                    comp = Comp.objects.create(ip=ip)

                auth_result = comp.check_authorization()
                print('--auth_result--', ip, auth_result)

                collection.insert_one({
                    'ip': ip.ip,
                    'ip_id': ip.id,
                    'action': 'rescan',
                    'summary': summary,
                    'version': version,
                    'psu': psu,
                    'dev': dev,
                    'auth': auth_result,
                    'date': datetime.datetime.utcnow(),
                })

def potestua():
    api = WhatsMinerApi(ip='10.10.5.195', passwd='admin',
                        token_data={'time': '2604', 'salt': 'BQ5hoXV8', 'newsalt': 'd9Su8izM'})
    # Если нет в монге данных по соляре
    auth = api.authorization()
    print(auth)
    print(api.set_zone())

    auth = api.authorization()
    print(auth)

    print(api.set_zone())
    #print(api.manage_led())
    return

class Command(BaseCommand):
    """
       vpn connect then
       sudo route add 10.10.11.0/24 10.10.6.1
       sudo route add 10.10.10.0/24 10.10.6.1
       sudo route add 10.10.5.0/24 10.10.6.1
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
        parser.add_argument('--restart',
            action = 'store',
            dest = 'restart',
            type = str,
            default = False,
            help = 'Restart over api by Comp pk')

    def handle(self, *args, **options):
        #potestua()
        #return
        if options.get('restart'):
            pk = options['restart']
            logger.info('RESTART comp with pk %s' % pk)
            comps = Comp.objects.select_related('ip').filter(pk=pk, ip__isnull=False)
            for comp in comps:
                ip = comp.ip.ip
                api = WhatsMinerApi(ip=ip, passwd='admin', token_data=comp.get_token_data())
                #api = WhatsMinerApi(ip=ip, passwd='admin')
                summary = api.exec('summary')
                version = api.exec('get_version')
                psu = api.exec('get_psu')
                dev = api.exec('devdetails')
                print('--summary--', ip, summary)
                print('--version--', ip, version)
                print('--psu--', ip, psu)
                print('--dev--', ip, dev)
                print('--auth--', ip, auth)
                auth = api.authorization()
                # TODO: RESTART
            return

        ip_ports = []
        if options.get('ip_ports'):
            ip_ports = [int(port) for port in options['ip_ports'].split(',') if port]
        else:
            ip_ports = [4028]
        for i in range(1):
            rescan(ip_ports)
            time.sleep(1)







