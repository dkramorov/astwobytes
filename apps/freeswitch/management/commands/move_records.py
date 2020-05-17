# -*- coding: utf-8 -*-
import logging
import os
import shutil
import time

from django.core.management.base import BaseCommand

from apps.main_functions.fortasks import search_process

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--calc',
            action = 'store_true',
            dest = 'calc',
            default = False,
            help = 'Calculate commands for directory')
        parser.add_argument('--source',
            action = 'store',
            dest = 'source',
            type = str,
            default = False,
            help = 'Set source folder for move in another place and replace to symlink')
        parser.add_argument('--dest',
            action = 'store',
            dest = 'dest',
            type = str,
            default = False,
            help = 'Set dest folder')
    def handle(self, *args, **options):
        """Перемещение записей source => dest
           source - откуда перемещаем (создаем симв. ссыль на dest)
           dest - куда перемещаем
           предполагается, что dest - это nfs папка

           СЕРВЕР
           apt-get install nfs-kernel-server
           mcedit /etc/exports
           /home/jocker/sites 192.168.1.0/255.255.255.0(rw,insecure,nohide,all_squash,anonuid=1000,anongid=1000,no_subtree_check)
           /etc/init.d/nfs-kernel-server restart
           # exportfs -rav
           exporting 192.168.1.0/255.255.255.0:/home/jocker/sites

           КЛИЕНТ
           apt-get install nfs-common
           mount -t nfs 192.168.1.100:/home/jocker/sites /home/jocker/tmp

           DEMO USAGE:
           # python manage.py move_records --source=2020-01-27 --dest=2020-01-27 --calc
        """
        is_running = search_process(q = ('move_records', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        source = dest = None
        source_folder = '/usr/local/freeswitch/default_context'
        if options.get('source'):
            source = options['source']
            if not source.startswith('/'):
                source = os.path.join(source_folder, source)
        dest_folder = '/home/jocker/tmp/freeswitch/default_context'
        if options.get('dest'):
            dest = options['dest']
            if not dest.startswith('/'):
                dest = os.path.join(dest_folder, dest)

        if options.get('calc'):
            """Корявенько пока - не учитываются переопределенные пути"""
            logger.info('calculating commands...')
            source_folder = os.path.split(source)[0]
            logger.info('source folder %s' % source_folder)
            folders = os.listdir(source_folder)
            for folder in folders:
                fname = os.path.join(source_folder, folder)
                if not os.path.islink(fname):
                    print('python manage.py move_records --source=%s --dest=%s' % (folder, folder))
            exit()

        if not source or not dest:
            logger.info('you have to set source and dest both')
            exit()
        if os.path.islink(source):
            logger.info('%s already is symlink' % source)
            exit()
        if source == dest or dest in source or source in dest:
            logger.info('you doing something wrong')
            exit()
        if os.path.exists(dest):
            logger.info('you can not move to existing folder')
            exit()
        if not os.path.exists(source) and os.path.exists(dest):
            logger.info('source have to be exists and dest have to be absent')
            exit()

        path = ''
        # Первую не берем /
        # Последнюю не создаем
        for item in dest.split('/')[1:-1]:
            path += '/%s' % item
            if not os.path.exists(path):
                logging.info('creating %s' % path)
                os.mkdir(path)
                os.system('/bin/chmod -R 755 %s' % path)
        logger.info('source %s, dest %s' % (source, dest))
        shutil.copytree(source, dest)
        shutil.rmtree(source)
        os.symlink(dest, source)
        os.system('/bin/chmod -R 755 %s' % dest)
