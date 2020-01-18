# -*- coding: utf-8 -*-
import os
import platform

def get_platform():
    """Проверяем платформу"""
    result = {'isMac': False}
    p = platform.system()
    if 'Darwin' in p:
        result['isMac'] = True
    return result

def search_binary(cmd):
    """Поиск исполняемого файла в системе"""
    #search = "/usr/bin/whereis"
    #if get_platform()['isMac']:
        #search = "/usr/bin/which"
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

def ps_fax(process_name, search_process):
    """Ищем процесс по pid
       process_name = "imgahost"
       search_process = "bin/bis223 imgahost"
       Пример: freeswitch oper_calls
       project_name = settings.MEDIA_ROOT.split("/")[-2]
       is_running = ps_fax("oper_calls", "bin/%s oper_calls" % project_name)
       if is_running:
          print("Already running", is_running)
          exit()"""
    my_pid = os.getpid()
    isMac = get_platform()['isMac']

    ps = '/bin/ps -fax'
    cmd = '%s|grep %s' % (ps, process_name)
    f = os.popen(cmd)
    process_info = f.readlines()
    f.close()

    parent = None
    for item in process_info:
        if search_process in item:
            # Проверяем, не наш ли это процесс
            # На линухе процесс - первая запись
            # На маке - пятая запись
            item = item.replace('\t', ' ')
            item_array = item.strip().split(' ')
            if isMac:
                found = False
                for i, item in enumerate(item_array):
                    try:
                        process_id = int(item_array[i + 1])
                    except ValueError:
                        process_id = None
                    if i > 4:
                        break
                    if process_id == my_pid:
                        found = True
                        break
                if found:
                    continue
            else:
              # parent (из крона стартует)
              if '/bin/sh -c' in item:
                  continue
              if int(item_array[0]) == my_pid:
                  continue
            return item
    return 0

