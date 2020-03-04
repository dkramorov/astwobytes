# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import open_file, check_path, make_folder

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        """Создаем uwsgi файл, который нужно будет разместить в
           /etc/uwsgi/apps-available/, например,
           /etc/uwsgi/apps-available/astwobytes.ini"""

        logger.info("""please, do following:
---------------------------------
--- INSTALL uwsgi for python3 ---
---------------------------------
# apt-get install uwsgi-plugin-python3
# apt install uwsgi-plugin-python
look at /usr/lib/uwsgi/plugins, check python3_plugin.so python_plugin.so
if it does not exists
if we have python LOWER 3.6, let is build
-------------------------------
--- BUILD uwsgi for python3 ---
-------------------------------
# sudo apt install python3.6 python3.6-dev uwsgi uwsgi-src uuid-dev libcap-dev libpcre3-dev libssl-dev
$ cd ~
$ export PYTHON=python3.6
$ uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python36"
$ sudo mv python36_plugin.so /usr/lib/uwsgi/plugins/python36_plugin.so
$ sudo chmod 644 /usr/lib/uwsgi/plugins/python36_plugin.so
$ uwsgi --plugin python36 -s :0
""")

        folder = 'demonize'
        if check_path(folder):
            make_folder(folder)
        uwsgi_path = '%s/astwobytes.ini' % (folder, )
        with open_file(uwsgi_path, 'w+') as f:
            f.write("""[uwsgi]
  processes = 1
  master = true
  plugins = python36
  chdir = /home/jocker/sites/astwobytes
  harakiri = 40
  wsgi-file = /home/jocker/sites/astwobytes/conf/wsgi.py
  pythonpath = /home/jocker/sites/astwobytes/env/lib/python3.6/site-packages
  buffer-size = 8192
""")
        logger.info('created %s' % (uwsgi_path, ))
