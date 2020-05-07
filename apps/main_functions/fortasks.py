# -*- coding: utf-8 -*-
import os
import platform
import psutil
import socket

def get_locale():
    """Возвращает локаль,
       функция здесь для информации:
       иногда через LaunchAgents запускается локаль US-ASCII (None, None)
       вместо utf-8 и проблема с записью и чтением файла начинается"""
    import locale
    return (locale.getpreferredencoding(False), locale.getlocale())

def get_hostname():
    """Возвращаем имя хоста"""
    return socket.gethostname()

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
       Посмотреть все свойства можно get_psutil_attr_names()
    """
    if not isinstance(q, list) and not isinstance(q, tuple):
        assert False
    mypid = os.getpid()
    myppid = os.getppid()
    for obj in psutil.process_iter():
        process = obj.as_dict(attrs=['pid', 'cmdline', 'create_time', ])
        if not process['cmdline']:
            continue
        if process['pid'] == mypid or process['pid'] == myppid:
            continue
        match = True
        for item in q:
            in_cmd = list(filter(lambda x: item in x, process['cmdline']))
            #print(in_cmd)
            if not in_cmd:
                match = False
                break
        if match:
            return process
    return None
