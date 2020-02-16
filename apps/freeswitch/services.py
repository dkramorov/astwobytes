# -*- coding: utf-8 -*-
import os
import logging
import datetime

from django.conf import settings

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.date_time import str_to_date, date_plus_days
from apps.main_functions.files import (ListDir, isForD, open_file, drop_file)

from .backend import FreeswitchBackend
from .models import CdrCsv, PersonalUsers, PhonesWhiteList

logger = logging.getLogger('simple')
CDR_VARS = ('cid', 'cid_name', 'dest', 'context',
            'created', 'answered', 'ended',
            'duration', 'billing', 'state',
            'uuid', 'bleg_uuid', 'account',
            'read_codec', 'write_codec',
            'ip', 'user_agent', )

def parse_log_line(line: list):
    """Анализ линии из логов записей звонков
       :param line: линия для парсинга"""
    line_array = line.split('","')
    line_array_len = len(line_array)
    if not line_array_len in (15, 16, 17):
        logger.error('line length not in 15,16,17: %s' % (line, ))
        return
    cur_cdr = {}
    for i in range(line_array_len):
        line_array[i] = kill_quotes(line_array[i], 'quotes')
        line_array[i] = line_array[i].replace('\n', '').strip()

        key = CDR_VARS[i]
        value = line_array[i]

        if key in ('created', 'answered', 'ended'):
            value = str_to_date(value)
        if not value:
            value = None

        if key == 'user_agent':
            if value and '@' in value:
                value = value.split('@')[0]
                if value.isdigit():
                    puser = PersonalUsers.objects.filter(userid=value).first()
                    if puser:
                        cur_cdr['personal_user_id'] = puser.userid
                        cur_cdr['personal_user_name'] = puser.username
            else:
                value = None
        # ------------------
        # Убиваем нуль-байты
        # ------------------
        if isinstance(value, str):
            value = value.replace('\x00', '')
        cur_cdr[key] = value

    if not cur_cdr['uuid']:
        logger.error('uuid not in line %s' % (line, ))
        return

    if 'cid' in cur_cdr:
        if cur_cdr['cid']:
            cur_cdr['cid'] = cur_cdr['cid']
    # -----------------------------------
    # Пропускаем звонки, которые заходили
    # на оператора и не были приняты им
    # -----------------------------------
    if cur_cdr['state'] in ("ALLOTTED_TIMEOUT", ): # "ORIGINATOR_CANCEL" пока фиксируем
        return

    analogs = CdrCsv.objects.filter(uuid=cur_cdr['uuid'], created=cur_cdr['created'])
    if not analogs:
        new_cdr = CdrCsv()
    else:
        new_cdr = analogs[0]

    for key, value in cur_cdr.items():
        if key == 'dest':
            if '%' in value:
                value = value.split('%')[0]
            elif value:
                if value.isdigit():
                    if len(value) == 6:
                        value = '83952%s' % (value, )
                    elif len(value) == 10:
                        value = '8%s' % (value, )
                    #if len(value) == 11:
                        #value = '8%s' % (value[1:], )
                        # В случае с колцентром, первая семерка

        setattr(new_cdr, key, value)

    search_by_phone = PhonesWhiteList.objects.filter(tag__isnull=False, phone=new_cdr.dest).first()
    if search_by_phone:
        new_cdr.client_id = search_by_phone.tag
        new_cdr.client_name = search_by_phone.name
    new_cdr.save()

def analyze_logs():
    """Анализируем cdr_csv папку для записи звонков
       Конфиг
       autoload_configs/cdr_csv.conf.xml
       добавляем ..., "${remote_media_ip}"
       добавляем ..., "${network_addr}"
       Перезапуск модуля reload mod_cdr_csv
       Освободить файл логов cdr_csv rotate
    """
    FreeswitchBackend(settings.FREESWITCH_URI).cdr_csv_rotate() # перезагрузжаем логи
    path = 'cdr-csv' # На папку должна быть символическая ссылка в media
    content = ListDir(path)
    if not content:
        assert False
    now = datetime.datetime.today()
    old_date = date_plus_days(now, hours=-2)
    for item in content:
        # Мы уже rotate на лог сделали - основной не парсим
        if item == 'Master.csv' or not '.csv.' in item:
            logger.info('Passing %s' % (item, ))
            continue
        lines = []
        cur_path = os.path.join(path, item)
        if isForD(cur_path) == 'file':
            with open_file(cur_path) as f:
                lines = f.readlines()
        for line in lines:
            parse_log_line(line.decode('utf-8'))
        search_date = item.split('.')[-1]
        cur_item_date = '%s %s' % (search_date[:10], search_date[11:].replace('-', ':'))
        date = str_to_date(cur_item_date)
        if date < old_date:
            logger.info('Dropping %s' % (cur_path, ))
            drop_file(cur_path)
