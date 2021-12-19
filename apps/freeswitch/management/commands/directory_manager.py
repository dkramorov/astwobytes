# -*- coding: utf-8 -*-
import os
import logging
import time
import json
import xml.sax
import requests
import shutil

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import open_file, check_path, full_path
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.fortasks import search_process
from apps.freeswitch.backend import FreeswitchBackend

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--get_jabber_users',
            action = 'store_true',
            dest = 'get_jabber_users',
            default = False,
            help = 'Get all jabber users')
        parser.add_argument('--passwd',
            action = 'store',
            type = str,
            dest = 'passwd',
            default = False,
            help = 'Account passwd')
        parser.add_argument('--login',
            action = 'store',
            type = str,
            dest = 'login',
            default = False,
            help = 'Account login')
        parser.add_argument('--context',
            action = 'store',
            type = str,
            dest = 'context',
            default = False,
            help = 'Account context')
        parser.add_argument('--caller_id',
            action = 'store',
            type = str,
            dest = 'caller_id',
            default = False,
            help = 'Account caller_id')
        parser.add_argument('--caller_name',
            action = 'store',
            type = str,
            dest = 'caller_name',
            default = False,
            help = 'Account caller_name')
        parser.add_argument('--group',
            action = 'store',
            type = str,
            dest = 'group',
            default = False,
            help = 'Account group')
    def handle(self, *args, **options):
        """Работа с directory freeswitch по пользователям"""
        is_running = search_process(q = ('directory_manager', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        if options.get('get_jabber_users'):
            get_jabber_users()
            return

        print('[EXAMPLE]: python manage.py directory_manager --passwd=123 --login=89148959224 --context=public_context --caller_id=89148959224 --caller_name=Den --group=app')
        passwd = options.get('passwd')
        login = options.get('login')
        context = options.get('context')
        caller_id = options.get('caller_id')
        caller_name = options.get('caller_name')
        group = options.get('group')
        if not passwd or not login or not context or not caller_id or not caller_name or not group:
            print('[ERROR]: not enough params')
            return

        xml = 'app_users.xml'
        users = read_source(source_xml=xml)

        # Ищем аналог и обновляем, если есть
        user_exists = False
        for user in users:
            if user['login'] == login:
                user['passwd'] = passwd
                user['context'] = context
                user['caller_id'] = caller_id
                user['caller_name'] = caller_name
                user['group'] = group
                user_exists = True
                break
        if not user_exists:
            users.append({
                'passwd': passwd,
                'login': login,
                'context': context,
                'caller_id': caller_id,
                'caller_name': caller_name,
                'group': group,
            })
        write_dest(dest_xml=xml, users=users)

        print(json_pretty_print(users))

def check_fs_users_db_version():
    """Проверяем какую версию имеет джаббер по пользователям свича
       смотрим на файл fs_users_db_version.json,
       если у нас он другой, тогда надо обновляться
    """
    jaba_domain = 'https://%s' % settings.JABBER_DOMAIN.rstrip('/')
    fs_users_db_version = 'fs_users_db_version.json'
    if check_path(fs_users_db_version):
        version = 0
    else:
        with open_file(fs_users_db_version, 'r', encoding='utf-8') as f:
            version = int(json.loads(f.read())['version'])
    r = requests.get('%s/media/%s' % (jaba_domain, fs_users_db_version))
    print(r.text)
    new_version = int(r.json()['version'])
    if new_version == version:
        print('versions equal')
        return False
    with open_file(fs_users_db_version, 'w+', encoding='utf-8') as f:
        f.write(json.dumps({'version': new_version}))
    return True

def get_jabber_users():
    """Получение всех пользователей джаббера
       и создание их в фрисвич директории,
       обновление происходит если версия дб отличается,
       смотрим на файл fs_users_db_version.json,
       если у нас он другой, тогда обновляемся
    """
    if not check_fs_users_db_version():
        return
    jaba_domain = 'https://%s' % settings.JABBER_DOMAIN.rstrip('/')
    endpoint = '/jabber/get_jabber_users'
    token = settings.FS_TOKEN
    url = '%s%s' % (jaba_domain, endpoint)
    headers = {
        'token': settings.FS_TOKEN,
    }
    r = requests.get(url, headers=headers)
    if not r.status_code == 200:
        print('[ERROR]: response %s, status_code %s' % (r.text, r.status_code))
        return
    users = []
    response = r.json()
    for item in response:
        users.append({
            'passwd': item['passwd'],
            'login': item['phone'],
            'context': 'public_context',
            'caller_id': item['phone'],
            'caller_name': item['phone'],
            'group': 'app',
        })
    xml = 'app_users.xml'
    write_dest(dest_xml=xml, users=users)
    fs_public_directory = '/usr/local/freeswitch/conf/directory/public'
    if os.path.exists(fs_public_directory):
        dest = os.path.join(fs_public_directory, xml)
        shutil.move(full_path(xml), dest)
    else:
        print('[ERROR]: fs dir not found %s, stopping...' % fs_public_directory)
        return
    # локальный монитор
    # autoload_configs/xml_rpc.conf.xml
    fs = FreeswitchBackend(settings.FREESWITCH_URI)
    result = fs.restart_profile('public')
    print(result)

def read_source(source_xml: str):
    """Считать имеющиеся данные по пользователям
       :param source_xml: путь к файлу, откуда читаем пользователей
    """
    if check_path(source_xml):
        return []
    with open_file(source_xml, 'r+', encoding='utf-8') as f:
        content = f.read()

    result = []
    handler = UserDirectoryParser(result)
    xml.sax.parseString(content, handler)
    return handler.result

def write_dest(dest_xml: str, users: list):
    """Записать результаты по пользователям в файл
       :param dest_xml: путь к файлу, куда пишем пользователей
       :param users: пользователи, которых пишем в файл
    """
    user_directory_template = """
  <user id="{login}">
    <params>
      <param name="password" value="{passwd}"/>
    </params>
    <variables>
      <variable name="toll_allow" value="domestic,international,local"/>
      <variable name="accountcode" value="{login}"/>
      <variable name="user_context" value="{context}"/>
      <variable name="effective_caller_id_name" value="{caller_id}"/>
      <variable name="effective_caller_id_number" value="{caller_name}"/>
      <variable name="outbound_caller_id_name" value="{caller_id}"/>
      <variable name="outbound_caller_id_number" value="{caller_name}"/>
      <variable name="callgroup" value="{group}"/>
    </variables>
  </user>
"""
    with open_file(dest_xml, 'w+', encoding='utf-8') as f:
        f.write('<include>\n')
        for user in users:
            cur_user = user_directory_template.format(
                passwd = user['passwd'],
                login = user['login'],
                context = user['context'],
                caller_id = user['caller_id'],
                caller_name = user['caller_name'],
                group = user['group'],
            )
            f.write(cur_user)
        f.write('</include>')


class UserDirectoryParser(xml.sax.ContentHandler):
    """Парсер профилей пользователей
<include>
  <user id="{login}">
    <params>
      <param name="password" value="{passwd}"/>
    </params>
    <variables>
      <variable name="toll_allow" value="domestic,international,local"/>
      <variable name="accountcode" value="{login}"/>
      <variable name="user_context" value="{context}"/>
      <variable name="effective_caller_id_name" value="{caller_id}"/>
      <variable name="effective_caller_id_number" value="{caller_name}"/>
      <variable name="outbound_caller_id_name" value="{caller_id}"/>
      <variable name="outbound_caller_id_number" value="{caller_name}"/>
      <variable name="callgroup" value="{group}"/>
    </variables>
  </user>
</include>
    """
    def __init__(self, result):
        """Передаем result для аккумуляции результата
           :param result: аккумуляция результата
        """
        self.result = result
        self.cur_user = {}

        self.include_name = 'include'
        self.in_include_name = False # <include>

        self.user_name = 'user'
        self.in_user_name = False # <user>

        self.params_name = 'params'
        self.in_params_name = False # <params>

        self.param_name = 'param'
        self.in_param_name = False

        self.variables_name = 'variables'
        self.in_variables_name = False

        self.variable_name = 'variable'
        self.in_variable_name = False

    def startElement(self, name, attributes):
        if not self.in_include_name and name == self.include_name:
            self.in_include_name = True

        if not self.in_user_name and name == self.user_name:
            self.in_user_name = True
            self.cur_user['login'] = attributes.get('id')

        if not self.in_params_name and name == self.params_name:
            self.in_params_name = True

        if not self.in_param_name and name == self.param_name:
            self.in_param_name = True
            if attributes.get('name') == 'password':
                self.cur_user['passwd'] = attributes.get('value')

        if not self.in_variables_name and name == self.variables_name:
            self.in_variables_name = True

        if not self.in_variable_name and name == self.variable_name:
            self.in_variable_name = True
            name = attributes.get('name')
            value = attributes.get('value')
            if name == 'accountcode':
                self.cur_user['login'] = value
            elif name == 'user_context':
                self.cur_user['context'] = value
            elif name == 'effective_caller_id_name':
                self.cur_user['caller_id'] = value
            elif name == 'effective_caller_id_number':
                self.cur_user['caller_name'] = value
            elif name == 'callgroup':
                self.cur_user['group'] = value

    def characters(self, content):
        pass

    def endElement(self, name):
        if self.in_include_name and name == self.include_name:
            self.in_include_name = False

        if self.in_user_name and name == self.user_name:
            self.result.append(self.cur_user)
            self.cur_user = {}
            self.in_user_name = False

        if self.in_params_name and name == self.params_name:
            self.in_params_name = False

        if self.in_param_name and name == self.param_name:
            self.in_param_name = False

        if self.in_variables_name and name == self.variables_name:
            self.in_variables_name = False

        if self.in_variable_name and name == self.variable_name:
            self.in_variable_name = False



