# -*- coding: utf-8 -*-
import os
import logging
import datetime

from django.conf import settings

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.date_time import str_to_date, date_plus_days
from apps.main_functions.files import (ListDir, isForD, open_file, drop_file)

from .backend import FreeswitchBackend
from .models import CdrCsv, PersonalUsers, PhonesWhiteList, Redirects

logger = logging.getLogger('simple')
CDR_VARS = ('cid', 'cid_name', 'dest', 'context',
            'created', 'answered', 'ended',
            'duration', 'billing', 'state',
            'uuid', 'bleg_uuid', 'account',
            'read_codec', 'write_codec',
            'ip', 'user_agent', )

def parse_log_line(line: list, redirects: list):
    """Анализ линии из логов записей звонков
       :param line: линия для парсинга
       :param redirects: переадресации 10 знаков (без 7/8)
    """
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
                if value.isdigit(): # Depricated
                    puser = PersonalUsers.objects.filter(userid=value).first()
                    if puser:
                        cur_cdr['personal_user_id'] = puser.userid
                        cur_cdr['personal_user_name'] = puser.username
                else:
                    puser = PersonalUsers.objects.filter(userkey=value).first()
                    if puser:
                        cur_cdr['personal_user_id'] = puser.userkey
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
                    # переадресации начинаются с 7
                    if len(value) == 11 and value[1:] in redirects:
                        value = '7%s' % value[1:]
        setattr(new_cdr, key, value)

    # Передаресация к нам придет с 7,
    # в PhonesWhiteList у нас все телефоны на 8
    # телефонов колцентра не должно быть в переадресациях
    dest_arr = ('8%s' % (new_cdr.dest[1:], ), '7%s' % (new_cdr.dest[1:], ))
    search_by_phone = PhonesWhiteList.objects.filter(tag__isnull=False, phone__in=dest_arr).first()
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
    redirects = Redirects.objects.all().values_list('phone', flat=True)
    redirects = [kill_quotes(redirect, 'int') for redirect in redirects]
    redirects = [redirect[1:] for redirect in redirects if len(redirect) == 11]
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
            parse_log_line(line.decode('utf-8'), redirects)
        search_date = item.split('.')[-1]
        cur_item_date = '%s %s' % (search_date[:10], search_date[11:].replace('-', ':'))
        date = str_to_date(cur_item_date)
        if date < old_date:
            logger.info('Dropping %s' % (cur_path, ))
            drop_file(cur_path)

def voice_code(dest: str,
               digit: str,
               script: str = 'hello.say_digit',
               allowed_phones: list = None,
               additional_params: dict = None):
    """Апи-метод, чтобы позвонить на телефон и продиктовать код
       :param dest: номер назначение
       :param digit: число, которое сообщаем в назначение
       Вызывается скрипт hello/say_digit.py
    """
    full_settings = settings.FULL_SETTINGS_SET
    if not 'FREESWITCH_SERVICES_URI' in full_settings:
        uri = settings.FREESWITCH_URI
    else:
        uri = full_settings['FREESWITCH_SERVICES_URI']

    if not script in ['hello.say_digit', 'reg_call.lua']:
        return 'error: script not supported'
    if not dest or not digit:
        return 'error: phone or digit is absent'
    if len(dest) != 11:
        if dest in allowed_phones:
            pass # allowed_phones can call
        else:
            return 'error: phone is not 11 digits'
    fs = FreeswitchBackend(uri)
    args = [dest, digit]
    if additional_params:
        for key, value in additional_params.items():
            if value:
                args.append(value)
    return fs.call_script(script, args)

