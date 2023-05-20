# -*- coding:utf-8 -*-
import json
import time
import socket
import hashlib
import binascii
import datetime
import base64
import traceback
import requests

from apps.main_functions.simple_logger import logger
from passlib.hash import md5_crypt
from Crypto.Cipher import AES

class WhatsMinerApi:
    token_data = {}
    def __init__(self, ip: str, port: int = 4028, passwd: str = 'admin', token_data: dict = None):
        self.ip = ip
        self.port = port
        self.passwd = passwd
        self.last_login = datetime.datetime.now() - datetime.timedelta(days=1)
        # cgiminer => {"command":"CMD","parameter":"PARAM"}
        self.version = None
        if token_data:
            self.token_data = token_data
        self.luci_session = None

    def add_to_16(self, src):
        """Дописать нульбайт, TODO: rfill"""
        while len(src) % 16 != 0:
            src += '\0'
        return str.encode(src)

    def socket_request(self, cmd: dict):
        """Запрос на сокет"""
        socket.setdefaulttimeout(10)
        if 'cmd' in cmd:
            # Дублируем в command (cgiminer => {"command":"CMD","parameter":"PARAM"})
            #cmd['command'] = cmd['cmd']
            if 'param' in cmd:
                cmd['parameter'] = cmd['param']
        data = json.dumps(cmd)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection = s.connect((self.ip, self.port))
        s.sendall(data.encode('utf-8'))
        resp = self.recv(s, 4000)
        s.close()
        #print(resp)
        resp = resp.decode('utf-8').replace('\n', '').replace('\x00', '').replace(',}', '}')
        try:
            return json.loads(resp.replace(':inf,', ':"",').replace(':nan,', ':"",'))
        except Exception:
            traceback.print_exc()
            print('[ERROR]: req %s, ip %s, port %s, resp not json %s' % (cmd, self.ip, self.port, resp))

    def exec(self, cmd: str = None, param: str = None):
        """Выполнение команды cmd
           :param cmd: команда для выполнения
           :param param: параметр
        """
        cmd_commands = {
            'get_token': {}, # Получение токена
            'summary': {}, # Получение сводной информации
            'get_version': {}, # Получение версии
            #'get_miner_info': {'info': 'ip,proto,netmask,gateway,dns,hostname,mac,ledstat,gateway'},
            #'status': {},
            'get_psu': {},
            'devdetails': {},
            'edevs': {},
            'devs': {},
            'pools': {},
        }
        if not cmd in cmd_commands:
            logger.error('%s not in cmd_commands' % cmd)
            return
        data = {
            'cmd': cmd,
        }
        if param:
            data['param'] = param
        if cmd_commands[cmd]:
            for k, v in cmd_commands[cmd].items():
                data[k] = v
        return self.socket_request(cmd=data)

    def recv(self, sock, n):
        """Получение байтов из соединения с сокетом"""
        sock.setblocking(True)
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                if data:
                    return data
                return None
            data.extend(packet)
        return data

    def decode_cipher(self, json_response: dict):
        """Декодирование сообщения, которое пришло от сервера"""
        try:
            if 'STATUS' in json_response and json_response['STATUS'] == 'E':
                msg = json_response['Msg']
                logger.error('[ERROR]: %s' % msg)
                self.token_data = None
                return

            resp_ciphertext = base64.b64decode(json_response['enc'])
            resp_plaintext = self.cipher.decrypt(resp_ciphertext).decode().split('\x00')[0]
            resp = json.loads(resp_plaintext)
        except Exception as e:
            logger.exception('Error decoding encrypted response')
            self.token_data = None
            return
        return resp

    def gen_credentials(self, time: str, salt: str, new_salt: str):
        """Получение ключа
           pip install passlib
           pip install pycryptodome

           {"STATUS":"S","When":1678185039,"Code":134,"Msg":{"time":"5039","salt":"BQ5hoXV9","newsalt":"P5NTAcEp"},"Description":"whatsminer v1.3"}

           openssl passwd -1 -salt BQ5hoXV9 admin
               $1$BQ5hoXV9$RxmaDUO33TS7O26yeMHZ81

           md5_crypt.hash('admin', salt='BQ5hoXV9')
               $1$BQ5hoXV9$RxmaDUO33TS7O26yeMHZ81

           key  = openssl passwd -1 -salt $salt    "${admin_password}"|cut -f 4 -d '$'
           sign = openssl passwd -1 -salt $newsalt "${key}${time:0-4}"|cut -f 4 -d '$'

           key  = openssl passwd -1 -salt BQ5hoXV9 admin|cut -f 4 -d '$'
               $1$BQ5hoXV9$RxmaDUO33TS7O26yeMHZ81 => RxmaDUO33TS7O26yeMHZ81 (отрезаем по $)
           sign = openssl passwd -1 -salt P5NTAcEp RxmaDUO33TS7O26yeMHZ815039|cut -f 4 -d '$'
               W7vZynrBZBwIIjR5dvDJb0

           sign passed as token
        """
        key = md5_crypt.hash(self.passwd, salt=salt).split('$')[-1]
        aes_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
        aes_key = binascii.unhexlify(aes_key.encode('utf-8'))
        self.cipher = AES.new(aes_key, AES.MODE_ECB)

        phrase = '%s%s' % (key, time)
        self.token = md5_crypt.hash(phrase, salt=new_salt).split('$')[-1]
        self.last_login = datetime.datetime.now()
        return {
            'token': self.token,
            'last_login': self.last_login,
        }

    def authorization(self):
        if self.token_data:
            self.gen_credentials(
                time=self.token_data['time'],
                salt=self.token_data['salt'],
                new_salt=self.token_data['newsalt'],
            )
            return self.token_data
        data = self.exec(cmd='get_token')
        if data.get('STATUS') and isinstance(data['STATUS'], (list, tuple)) and data['STATUS'][0]['STATUS'] == 'E':
            # {'STATUS': 'E', 'When': 1682414431, 'Code': 136, 'Msg': 'over max connect'}
            return data
        logger.info('get_token response: %s, type=%s' % (data, type(data)))
        if not isinstance(data, dict):
            return {'error': 'Пустой ответ на запрос токена'}
        msg = data['Msg']
        self.token_data = msg
        self.gen_credentials(
            time=msg['time'],
            salt=msg['salt'],
            new_salt=msg['newsalt'],
        )
        return msg

    def write_operation(self, cmd):
        """Операции с API для записи"""
        cmd['token'] = self.token
        api_cmd = json.dumps(cmd)
        # Encrypt it and assemble the transport json
        enc_str = str(
            base64.encodebytes(
                self.cipher.encrypt(self.add_to_16(api_cmd))),
                encoding='utf8'
            ).replace('\n', '')
        data_enc = {'enc': 1} # transmit w/ "enc" to signal that it's encrypted
        data_enc['data'] = enc_str
        json_response = self.socket_request(cmd=data_enc)
        logger.info('___json_response: "%s"' % json_response)
        if not json_response:
            logger.error('[ERROR]: json_response is empty')
            return {}
        resp = self.decode_cipher(json_response)
        return resp

    def download_logs(self):
        """Скачать логи"""
        cmd_download_logs = {
            'cmd': 'download_logs',
        }
        return self.write_operation(cmd=cmd_download_logs)

    def manage_led(self):
        """Управление свето-диодом"""
        cmd_manage_led = {
            'cmd': 'set_led',
            'param': 'auto',
        }
        return self.write_operation(cmd=cmd_manage_led)

    def reboot(self):
        """Перезагрузка системы"""
        cmd_reboot = {
            'cmd': 'reboot',
        }
        return self.write_operation(cmd=cmd_reboot)

    def change_passwd(self):
        """Изменение пароля от аккаунта admin"""
        cmd_modify_passwd = {
            'cmd': 'update_pwd',
            'old': 'admin',
            'new': 'admin1',
        }
        return self.write_operation(cmd=cmd_modify_passwd)

    def set_zone(self, timezone: str = 'CST-8', zonename = 'Asia/Shanghai'):
        """Задаем часовой пояс, по совместительству проверяем, что токен в поряде"""
        cmd_set_zone = {
            'cmd': 'set_zone',
            'timezone': timezone,
            'zonename': zonename,
        }
        return self.write_operation(cmd=cmd_set_zone)

    def auth_luci(self):
        self.luci_session = requests.Session()
        auth = {'luci_username': 'admin', 'luci_password': 'admin'}
        self.luci_session.post('https://%s/cgi-bin/luci/' % self.ip, data=auth, verify=False)

    def get_luci_lan(self):
        try:
            r = self.luci_session.get('https://%s/cgi-bin/luci/admin/network/iface_status/lan?_=%s' % (self.ip, time.time()), verify=False)
            return r.json()
        except Exception:
            traceback.print_exc()

