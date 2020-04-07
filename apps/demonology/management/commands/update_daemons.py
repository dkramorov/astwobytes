#-*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand

from apps.main_functions.files import full_path, ListDir, isForD

logger = logging.getLogger('simple')

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--logs',
            action = 'store',
            dest = 'logs',
            type = str,
            default = False,
            help = 'Show logs for daemon')
        parser.add_argument('--watch',
            action = 'store',
            dest = 'watch',
            type = str,
            default = False,
            help = 'Watch logs for daemon')
        parser.add_argument('--restart',
            action = 'store',
            dest = 'restart',
            type = str,
            default = False,
            help = 'Restart daemon')
        parser.add_argument('--stop',
            action = 'store',
            dest = 'stop',
            type = str,
            default = False,
            help = 'Stop daemon')
        parser.add_argument('--status',
            action = 'store',
            dest = 'status',
            type = str,
            default = False,
            help = 'Show daemon status')

    def handle(self, *args, **options):
        """Работа с демонами"""
        if options.get('logs'):
            cmd = '/bin/journalctl -u %s -b --no-pager' % (options['logs'], )
            logger.info(cmd)
            os.system(cmd)
            return
        if options.get('watch'):
            cmd = '/bin/journalctl -u %s -f' % (options['watch'], )
            logger.info(cmd)
            os.system(cmd)
            return
        if options.get('restart'):
            cmd = '/bin/systemctl restart %s' % (options['restart'], )
            logger.info(cmd)
            os.system(cmd)
            return
        if options.get('stop'):
            cmd = '/bin/systemctl stop %s' % (options['stop'], )
            logger.info(cmd)
            os.system(cmd)
            return
        if options.get('status'):
            cmd = '/bin/systemctl status %s' % (options['status'], )
            logger.info(cmd)
            os.system(cmd)
            return

        daemons_folder = '/etc/systemd/system/'
        folder = 'demonology'
        folder_items = ListDir(folder)
        logger.info(folder_items)
        for item in folder_items:
            script = os.path.join(folder, item)
            if isForD(script) == 'file' and item.endswith('.service'):
                fname = os.path.join(daemons_folder, item)
                if os.path.exists(fname):
                    logger.info('%s exists, dropping' % (item, ))
                    os.unlink(fname)

                cmd = '/bin/cp %s %s' % (full_path(script), daemons_folder)
                logger.info(cmd)
                os.system(cmd)

                cmd = '/bin/systemctl daemon-reload'
                logger.info(cmd)
                os.system(cmd)

                cmd = '/bin/systemctl enable %s' % (item, )
                logger.info(cmd)
                os.system(cmd)

                cmd = '/bin/systemctl restart %s' % (item, )
                logger.info(cmd)
                os.system(cmd)



