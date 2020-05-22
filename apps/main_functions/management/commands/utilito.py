#-*- coding:utf-8 -*-
import os
import traceback
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_binary
from apps.main_functions.files import file_size, ListDir, isForD
from apps.main_functions.string_parser import (
    domain2punycode,
    generate_base_auth,
    ip2long,
    load_iptables,
    check_ip,
)

logger = logging.getLogger('main')

def clear_nginx_logs():
    """Чистка логов нгинкса"""
    messages = []
    nginx_log_path = '/var/log/nginx'
    items = ListDir(nginx_log_path, ignore_default_folder=True)
    for item in items:
        cur_path = os.path.join(nginx_log_path, item)
        item_type = isForD(cur_path)
        if item_type == 'file':
            if item.startswith('error.log.') or item.startswith('access.log.'):
                fsize = file_size(cur_path) / 1024
                try:
                    os.unlink(cur_path)
                    messages.append('[UNLINK]: %s - %sKb' % (cur_path, fsize))
                except:
                    messages.append('[ERROR]: drop %s failed' % cur_path)
    if messages:
        logger.info('\n' + '\n'.join(messages))

def iptables_action(action: str, ip: str, iptables_file: str = '/home/jocker/iptables'):
    """Блокирование или разблокирование айпи
       :param action: действие (блокировка/разблокировка)
       :param ip: айпи адрес
       :param iptables_file: путь до файла с таблицей фаервола
    """
    ip = check_ip(ip)
    if not ip:
        logger.info('bad ip=>%s' % ip)
        return
    fips = load_iptables()
    iptables = search_binary('iptables')
    if not iptables:
        logger.info('iptables not found')
        return
    iptables_save = search_binary('iptables-save')
    if not iptables_save:
        logger.info('iptables-save not found')
        return
    if action == 'block_ip':
        if ip in fips:
            logger.info('%s already in iptables' % ip)
            return
        rule = '%s -A INPUT -s %s -j DROP' % (iptables, ip)
        os.system(rule)
        os.system('%s>%s' % (iptables_save, iptables_file))
    elif action == 'unblock_ip':
        if not ip in fips:
            logger.info('%s not in iptables' % ip)
            return
        rule = '%s -D INPUT -s %s -j DROP' % (iptables, ip)
        os.system(rule)
        os.system('%s>%s' % (iptables_save, iptables_file))

class Command(BaseCommand):
    """Разные утилиты для операций"""
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--clear_nginx_logs',
            action = 'store_true',
            dest = 'clear_nginx_logs',
            default = False,
            help = 'Clear nginx logs')
        parser.add_argument('--iptables',
            action = 'store_true',
            dest = 'iptables',
            default = False,
            help = 'Show iptables')
        parser.add_argument('--idna',
            action = 'store',
            dest = 'idna',
            type = str,
            default = False,
            help = 'Translate cyrillic domain to punycode')
        parser.add_argument('--htpasswd',
            action = 'store',
            dest = 'htpasswd',
            type = str,
            default = False,
            help = 'Generate crypto passwd for base auth')
        parser.add_argument('--salt',
            action = 'store',
            dest = 'salt',
            type = str,
            default = False,
            help = 'Set salt for htpasswd command')
        parser.add_argument('--ip2long',
            action = 'store',
            dest = 'ip2long',
            type = str,
            default = False,
            help = 'Ip address to digit')
        parser.add_argument('--block_ip',
            action = 'store',
            dest = 'block_ip',
            type = str,
            default = False,
            help = 'Block ip address')
        parser.add_argument('--unblock_ip',
            action = 'store',
            dest = 'unblock_ip',
            type = str,
            default = False,
            help = 'Unblock ip address')

    def handle(self, *args, **options):
        # domain => punycode
        if options.get('idna'):
            logger.info('idna=> %s' % domain2punycode(options['idna']))

        # passwd for base auth
        if options.get('htpasswd'):
            passwd = options['htpasswd']
            salt = '86'
            if options.get('salt'):
                salt = options['salt']
            passwd_with_salt = generate_base_auth(passwd, salt)
            logger.info('passwd=>%s, salt=>%s, result=>%s' % (passwd, salt, passwd_with_salt))

        # ip2long
        if options.get('ip2long'):
            ip = options['ip2long']
            logger.info('ip2long=>%s' % ip2long(ip))

        # Чистим логи nginx
        if options.get('clear_nginx_logs'):
            clear_nginx_logs()

        # Показываем таблицу фаервола
        if options.get('iptables'):
            logger.info('\n' + '\n'.join(load_iptables()))

        # Блокирование/разблокирование айпи
        if options.get('block_ip') or options.get('unblock_ip'):
            search_ip = options.get('block_ip') or options.get('unblock_ip')
            action = 'block_ip' if options.get('block_ip') else 'unblock_ip'
            iptables_action(action, search_ip)
