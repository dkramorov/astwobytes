# -*- coding: utf-8 -*-
import os
import platform
import psutil

def search_binary(cmd):
    """Поиск исполняемого файла в системе"""
    search = '/usr/bin/which'
    search_cmd = '%s %s' % (search, cmd)
    f = os.popen(search_cmd)
    result = f.read()
    linux_prefix = '%s:' % cmd
    if linux_prefix in result:
        result = result.replace(linux_prefix, '')
    result = result.strip()
    if ' ' in result:
        result = result.split(' ')[0]
    return result.strip()

def get_psutil_attr_names():
    return list(psutil.Process().as_dict().keys())

def search_process(q: list):
    """Ищем процесс
       :param q: список строк для поиска
       Посмотреть всевозможные свойства можно get_psutil_attr_names()"""
    if not isinstance(q, list) and not isinstance(q, tuple):
        assert False
    mypid = os.getpid()
    for obj in psutil.process_iter():
        process = obj.as_dict(attrs=['pid', 'cmdline', 'create_time', ])
        if not process['cmdline']:
            continue
        if process['pid'] == mypid:
            continue
        match = True
        for item in q:
            if not item in process['cmdline']:
                match = False
                break
        if match:
            return process
    return None

