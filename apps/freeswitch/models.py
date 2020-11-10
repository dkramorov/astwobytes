# -*- coding: utf-8 -*-
import os
import logging
import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.date_time import str_to_date, date_plus_days
from apps.main_functions.files import (ListDir, isForD,
    full_path, check_path,
    make_folder, open_file, drop_file)
from apps.main_functions.models import Standard

from .backend import FreeswitchBackend

class PersonalUsers(Standard):
    """Зарегистрированные пользователи на сайте
       используем для привязки к звонкам,
       Такого пользователя можно привязать к FSUser,
       тогда можно будет разрешить ему звонить на любые номера,
       посредством динамического диалплана, который проверяется
       через /freeswitch/is_user_in_white_list/?user_id=134@223-223.ru
       Загружается через CRM_HOST в настройках - не редактируется
    """
    username = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    userid = models.IntegerField(blank=True, null=True, db_index=True)
    phone_confirmed = models.IntegerField(blank=True, null=True, db_index=True, verbose_name='Телефон подтвержден')
    phone = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Freeswitch - Пользователи сайта'
        verbose_name_plural = 'Freeswtich - Пользователи сайта'

    def save(self, *args, **kwargs):
        if self.phone:
            phone = kill_quotes(self.phone, 'int')
            if phone.startswith('7'):
                phone = '8%s' % (phone[1:], )
            self.phone = phone
        super(PersonalUsers, self).save(*args, **kwargs)

class PhonesWhiteList(Standard):
    """Белый список телефонов для АТС,
       на которые пропускаем звонки
       посредством динамического диалплана, который проверяется
       через /freeswitch/is_user_in_white_list/?phone=89148959223
       Загружается через CRM_HOST в настройках - не редактируется
    """
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    phone = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Важный идентификатор, например, id компании')

    def save(self, *args, **kwargs):
        if self.phone:
            phone = kill_quotes(self.phone, 'int')
            if phone.startswith('7'):
                phone = '8%s' % (phone[1:], )
            self.phone = phone
        super(PhonesWhiteList, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Freeswitch - Телефоны CRM'
        verbose_name_plural = 'Freeswtich - Телефоны CRM'

class FSUser(Standard):
    """Пользователи FreeSwitch"""
    FOLDER = 'fs_users'
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_fs_user')
    passwd = models.CharField(max_length=255, blank=True, null=True)
    context = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    cid = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    callgroup = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # Привязка пользователя с сайта
    personal_user = models.OneToOneField(PersonalUsers, blank=True, null=True, on_delete=models.SET_NULL, related_name='personal_fs_user')

    class Meta:
        verbose_name = 'Freeswitch - Пользователь'
        verbose_name_plural = 'Freeswtich - Польозватели'

    def drop_extension(self):
        """Удаление файла в случае удаления записи или отключения"""
        fname = '%s/fs_user_%s.xml' % (self.FOLDER, self.id)
        if not check_path(fname):
            drop_file(fname)
        FreeswitchBackend(settings.FREESWITCH_URI).reloadxml()

    def delete(self, *args, **kwargs):
        self.drop_extension()
        super(FSUser, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        cid = kill_quotes(self.cid, 'int')
        if cid.startswith('7'):
            cid = '8%s' % (cid[1:], )
        self.cid = cid
        super(FSUser, self).save(*args, **kwargs)
        if not self.is_active or not self.user or not self.passwd or not self.context or not self.cid:
            self.drop_extension()
            return
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
        FreeswitchBackend(settings.FREESWITCH_URI).reloadxml()

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

    def get_record_path(self):
        """Получить путь до записи"""
        record = '/media/%s/%s/%s_%s.wav' % (
            self.context,
            self.created.strftime('%Y-%m-%d'),
            self.dest,
            self.uuid,
        )
        return record

    class Meta:
        verbose_name = 'Freeswitch - Звонок'
        verbose_name_plural = 'Freeswtich - Звонки'
