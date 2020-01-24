# -*- coding: utf-8 -*-
import os
import logging

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.date_time import str_to_date
from apps.main_functions.files import (ListDir, isForD,
    full_path, check_path,
    make_folder, open_file, drop_file)
from apps.main_functions.models import Standard

from .backend import FreeswitchBackend, RemoteDB

logger = logging.getLogger('simple')
CDR_VARS = ('cid', 'cid_name', 'dest', 'context',
            'created', 'answered', 'ended',
            'duration', 'billing', 'state',
            'uuid', 'bleg_uuid', 'account',
            'read_codec', 'write_codec',
            'ip', 'user_agent', )

class FSUser(Standard):
    """Пользователи FreeSwitch"""
    FOLDER = 'fs_users'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passwd = models.CharField(max_length=255, blank=True, null=True)
    context = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    cid = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    callgroup = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    def drop_extension(self):
        """Удаление файла в случае удаления записи или отключения"""
        fname = '%s/fs_user_%s.xml' % (self.FOLDER, self.id)
        if not check_path(fname):
            drop_file(fname)
        #FreeswitchBackend(settings.FREESWITCH_URI).reloadxml()

    def delete(self, *args, **kwargs):
        self.drop_extension()
        super(FSUser, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(FSUser, self).save(*args, **kwargs)
        if not self.is_active:
            self.drop_extension()
        extension = """
<include>
  <user id="{}">
    <params>
      <param name="password" value="{}"/>
    </params>
    <variables>
      <variable name="toll_allow" value="domestic,international,local"/>
      <variable name="accountcode" value="{}"/>
      <variable name="user_context" value="{}"/>
      <variable name="effective_caller_id_name" value="{}"/>
      <variable name="effective_caller_id_number" value="{}"/>
      <variable name="outbound_caller_id_name" value="{}"/>
      <variable name="outbound_caller_id_number" value="{}"/>
      <variable name="callgroup" value="{}"/>
    </variables>
  </user>
</include>""".format(self.user.username,
                     self.passwd,
                     self.user.username,
                     self.context,
                     self.user.username,
                     self.user.username,
                     self.cid,
                     self.cid,
                     self.callgroup)
        fname = full_path('%s/fs_user_%s.xml' % (self.FOLDER, self.id))
        if check_path(fname):
            make_folder(self.FOLDER)
        with open(fname, 'w+') as f:
            f.write(extension)
        #FreeswitchBackend(settings.FREESWITCH_URI).reloadxml()

class Redirects(Standard):
    """Переадресации - у нас есть номера, мы можем
       переадресовать с этого номера на другой
       context redirects"""
    FOLDER = 'redirects'
    phone = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Наш телефон')
    dest = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Куда переадресовываем (номер телефона)')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='Краткое описание')
    gw = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Шлюз, через который переадресовываем')
    price = models.IntegerField(blank=True, null=True, db_index=True, verbose_name='Цена для тарификации')
    price_unit = models.IntegerField(blank=True, null=True, db_index=True, verbose_name='Количество секунд для цены тарификации')

    class Meta:
        verbose_name = 'Freeswitch - Переадресация'
        verbose_name_plural = 'Freeswtich - Переадресации'

    def drop_extension(self):
        """Удаление файла в случае удаления записи или отключения"""
        fname = '%s/redirect_%s.xml' % (self.FOLDER, self.id)
        if not check_path(fname):
            drop_file(fname)
        FreeswitchBackend(settings.FREESWITCH_URI).reloadxml()

    def delete(self, *args, **kwargs):
        self.drop_extension()
        super(Redirects, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Redirects, self).save(*args, **kwargs)
        if not self.is_active:
            self.drop_extension()
            return
        extension = """
<extension name="redirect_{}">
  <condition field="destination_number" expression="^([78]{})$">
    <action application="set" data="effective_caller_id_number={}"/>
    <action application="set" data="effective_caller_id_name={}"/>
    <action application="set" data="ringback={}"/>
    <action application="export" data="hold_music={}"/>
    <action application="set" data="ignore_early_media=true" />
    <action application="set" data="record_file_name={}"/>
    <action application="set" data="media_bug_answer_req=true"/>
    <action application="export" data="execute_on_answer=record_session {}"/>
    <action application="set" data="sip_h_Diversion=&quot;{}&quot; <sip: {}@{}>;reason=unconditional;"/>
    <action application="bridge" data="sofia/gateway/{}/{}"/>
  </condition>
</extension>""".format(self.phone,
                       kill_quotes(self.phone[1:], 'int'),
                       '${caller_id_number}',
                       '${caller_id_number}',
                       '${us-ring}',
                       '$${hold_music}',
                       '$${base_dir}/${context}/${strftime(%Y-%m-%d)}/${destination_number}_${uuid}.wav',
                       '${record_file_name}',
                       '${diversion_phone}',
                       '${diversion_phone}',
                       '${diversion_domain}',
                       self.gw,
                       kill_quotes(self.dest, 'int'))
        fname = full_path('%s/redirect_%s.xml' % (self.FOLDER, self.id))
        if check_path(fname):
            make_folder(self.FOLDER)
        with open(fname, 'w+') as f:
            f.write(extension)
        FreeswitchBackend(settings.FREESWITCH_URI).reloadxml()

class CdrCsv(models.Model):
    """Логи звонков"""
    cid = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${caller_id_name}", "jocker"')
    cid_name = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${caller_id_number}", "jocker"')
    dest = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${destination_number}", "021067405"')
    context = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${context}", "rtmp_context"')
    created = models.DateTimeField(blank=True, null=True, db_index=True,
        verbose_name='"${start_stamp}", "2015-08-07 22:36:38"')
    answered = models.DateTimeField(blank=True, null=True, db_index=True,
        verbose_name='"${answer_stamp}", "2015-08-07 22:36:40"')
    ended = models.DateTimeField(blank=True, null=True, db_index=True,
        verbose_name='"${end_stamp}", "2015-08-07 22:36:44"')
    duration = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='"${duration}", "6"')
    billing = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='"${billsec}", "4"')
    state = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${hangup_cause}", "NORMAL_CLEARING"')
    uuid = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${uuid}", "b01e66de-8997-4e33-9907-4a237b22e049"')
    bleg_uuid = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${bleg_uuid}", "cb2c6082-2519-472d-8748-6d310b01d992"')
    account = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${accountcode}", "jocker"')
    read_codec = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${read_codec}", "GSM"')
    write_codec = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='"${write_codec}", "GSM"')
    ip = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='Айпи адрес')
    user_agent = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='С какого приложения звонок')
    client_id = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Ид компании, телефон которой в dest')
    client_name = models.CharField(max_length=255, blank=True, null=True,
        verbose_name='Название компании, телефон которой в dest')
    personal_user_id = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Ид пользователя на сайте')
    personal_user_name = models.CharField(max_length=255, blank=True, null=True,
        verbose_name='Имя пользователя на сайте')

    class Meta:
        verbose_name = 'Freeswitch - Звонок'
        verbose_name_plural = 'Freeswtich - Звонки'

def parse_log_line(db, line: list):
    """Анализ линии из логов записей звонков
       :param db: класс для работы с удаленной базой
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

        if key == 'personal_user_id':
            if value and '@' in value:
                value = value.split('@')[0]
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
        setattr(new_cdr, key, value)

    if not new_cdr.client_id:
        # ----------------------------
        # Определяем нахер че за фирма
        # ----------------------------
        company = db.get_company_by_phone(new_cdr.dest)
        if company:
            new_cdr.client_id = company['id']
            new_cdr.client_name = company['name']
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
    db = RemoteDB()
    FreeswitchBackend(settings.FREESWITCH_URI).cdr_csv_rotate() # перезагрузжаем логи
    path = 'cdr-csv' # На папку должна быть символическая ссылка в media
    content = ListDir(path)
    if not content:
        assert False
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
            parse_log_line(db, line.decode('utf-8'))
        logger.info('Dropping %s' % (cur_path, ))
        drop_file(cur_path)
