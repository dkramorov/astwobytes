# -*- coding:utf-8 -*-
import sys
import socket

from concurrent.futures import ThreadPoolExecutor

from apps.main_functions.simple_logger import logger
from apps.net_tools.models import make_list_from_range

"""
from django.core import management
management.call_command('scan_ips', ip_range=[127.0.0.1, ], ports=[4028, ])
"""

def scan_ip(task):
    """Сканирование ip адреса
       :param task: {'ip': '127.0.0.1', 'ports': [80, 4028]}
    """
    ip = task.get('ip')
    ports = task.get('ports')

    socket.setdefaulttimeout(1)
    if not ports:
        ports = [80, 4028] # 443 не открыт пока не зашли
    result = {
        'ip': ip,
        'open': [],
    }
    port = 0
    try:
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection = s.connect_ex((ip, port))
            if connection == 0:
                #logger.info('IP {}, Port {} is open'.format(ip, port))
                result['open'].append(port)
            #else:
            #    logger.info('IP {}, Port {} closed'.format(ip, port))
            s.close()
    except KeyboardInterrupt:
        logger.info('\nExiting Program')
    except socket.gaierror:
        logger.error('\n%s Hostname Could Not Be Resolved, last port %s' % (ip, port))
    except socket.error:
        logger.error('\n%s Host not responding, last port %s' % (ip, port))
    return result

def scan_ips(ip_range: list = None, ports: list = None, exclude_ips: list = None):
    """Сканирование айпи адресов по портам
       10.10.11.1-10.10.11.254
       10.10.10.1-10.10.10.254
       vpn connect then
       sudo route add 10.10.11.0/24 10.10.6.1
       sudo route add 10.10.10.0/24 10.10.6.1
    """
    if not ip_range:
        ip_range = ['10.10.11.%s' % i for i in range(1, 255)] + ['10.10.10.%s' % i for i in range(1, 255)]
    elif isinstance(ip_range, str):
        parsed_ip_range = make_list_from_range(ip_range)
        logger.info('received ip_range string: %s, parsed %s' % (ip_range, parsed_ip_range))
        ip_range = parsed_ip_range

    if ports:
        logger.info('received ports %s, ip_range: %s-%s' % (ports, ip_range[0], ip_range[-1]))

    if isinstance(exclude_ips, str):
        exclude_ips = make_list_from_range(ip_range)
    if exclude_ips:
        for ip in exclude_ips:
            if ip in ip_range:
                del ip_range[ip_range.index(ip)]
    ips = [{
        'ip': ip, 'ports': ports
    } for ip in ip_range]
    with ThreadPoolExecutor(len(ips)) as executor:
        results = executor.map(scan_ip, ips)
    return results

