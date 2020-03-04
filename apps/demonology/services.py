# -*- coding: utf-8 -*-
import os
import logging

from django.conf import settings

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.files import (check_path, open_file, drop_file, make_folder)

logger = logging.getLogger('simple')

DAEMON_FOLDER = 'demonology'
# Системная папка, куда мы слинкуем наши скрипты
SYSTEM_FOLDER = '/etc/systemd/system/'

def drop_daemon(daemon_name):
    """Удаляем демона
       :param daemon_name: название демона"""
    daemon = '%s/%s' % (DAEMON_FOLDER, daemon_name)
    drop_file(daemon)

def create_daemon(daemon_name, exec_script, port, pyenv: str = None):
    """Создаем демона
       :param daemon_name: название демона, например daemon_1.service
       :param exec_script: исполняемый файл, например,
           /home/jocker/sites/astwobytes/apps/ws_a223/wss_server.py
       :param port: параметр для передачи в испольняемый файл, например
           порт на котором должен запускаться демон
           скрипт должен принимать этот параметр,
           демон к этому не имеет отношения, просто передает
       :param pyenv: питонячий путь для запуска через python, например,
           /home/jocker/sites/astwobytes/env/bin/python
       :return:
       --------
       В демоне не нужно активировать виртуальное окружение,
       можно просто запускать исполняемый файл вирт. окружения,
       там уже содержатся все нужные пути -
       Проверить это можно через
       # python -m site
       сравниваем с
       # /home/jocker/sites/astwobytes/env/bin/python -m site
       - покажет базу и пути
       """
    if check_path(DAEMON_FOLDER):
        make_folder(DAEMON_FOLDER)

    if not pyenv:
        pyenv = '%s/env/bin/python' % (settings.BASE_DIR.rstrip('/'), )

    #daemon_path = '%s/%s.service' % (SYSTEM_FOLDER, daemon_name)
    #if os.path.exists(daemon_path):
    #    logger.info('daemon already exists')
    #    return

    daemon_script = """[Unit]
Description=%s
After=multi-user.target
ConditionPathExists=%s

[Service]
ExecStart=%s %s %s
Restart=always
Type=idle

[Install]
WantedBy=multi-user.target
#Alias=%s # Алиас не должен быть таким же как имя сервсиа
""" % (daemon_name, exec_script, pyenv, exec_script, port, daemon_name)

    daemon = '%s/%s' % (DAEMON_FOLDER, daemon_name)
    with open_file(daemon, 'w+') as f:
        f.write(daemon_script)
