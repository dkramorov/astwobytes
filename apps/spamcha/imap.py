#-*- coding:utf-8 -*-
import os
import datetime
import requests
import logging
import email
import imaplib

from apps.main_functions.string_parser import kill_html
from apps.main_functions.models import Config

logger = logging.getLogger('main')

class ImapProvider():
    """IMAP клиент для почты"""
    def __init__(self, user):
        """Подключение к серверу
           :param user: request.user или экземпляр модели User
        """
        self.conn = None
        self.authorized = False

        account = self.get_email_account(user)
        if not account:
            logger.info('[ERROR]: Email account not found')
            return
        self.login = account['login']
        self.passwd = account['passwd']
        self.imap_server = account['imap']
        self.conn = imaplib.IMAP4_SSL(account['imap'])
        if self.auth() == 'OK':
            logger.info('[IMAP]: authorized')
            self.authorized = True

    def get_email_account(self, user):
        """Получить email аккаунт пользователя
           :param user: пользователь
        """
        account = {}
        configs = Config.objects.filter(attr__startswith='spamcha', user=user)
        for config in configs:
            if config.attr == 'spamcha_login':
                account['login'] = config.value
            elif config.attr == 'spamcha_passwd':
                account['passwd'] = config.value
            elif config.attr == 'spamcha_imap':
                account['imap'] = config.value
        if 'login' in account and 'passwd' in account and 'imap' in account:
            return account

    def auth(self):
        """Авторизация"""
        result = self.conn.login(self.login, self.passwd)
        logger.info('[IMAP]: logged in %s' % result[0])
        return result[0]

    def get_folders(self):
        """Получение списка папок на сервере
        """
        result = []
        retcode, resp = self.conn.list()
        if retcode == 'OK':
            folders = [item.decode('utf-8') for item in resp]
            for folder in folders:
                folder = folder.split('"|"')[-1].strip()
                item = {'name': folder, 'count': 0}
                retcode, letters = self.select_folder(folder)
                if retcode == 'OK':
                     item['count'] = letters[0].decode('utf-8')

                ids_new_messages = self.search('(UNSEEN)')
                if ids_new_messages:
                    item['ids'] = ids_new_messages

                result.append(item)
        return result

    def select_folder(self, folder):
        """Выбирает папку на сервере
           :param folder: папка в зажопинском формате
        """
        logger.info('[IMAP]: select folder %s' % folder)
        result = self.conn.select(folder)
        return result

    def search(self, search_str: str = '(UNSEEN)'):
        """Получение списка ID писем через пробел
           :param search_str: поисковая строка 'ALL' / UNSEEN
        """
        retcode, result = self.conn.search(None, search_str)
        if retcode == 'OK':
            items = result[0].decode('utf-8').split(' ')
            return [int(item) for item in items if item]

    def get_headers(self, data):
        """Получем заголовки письма
           :param data: полученное письмо через fetch
        """
        result = {}
        for part in data:
            if not isinstance(part, tuple):
                continue
            msg = email.message_from_string(part[1].decode('utf-8'))
            s = email.header.make_header(email.header.decode_header(msg['Subject']))
            result['subject'] = str(s)
            t = email.header.make_header(email.header.decode_header(msg['To']))
            result['to'] = str(t)
            f = email.header.make_header(email.header.decode_header(msg['From']))
            result['from'] = str(f)

            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                result['date'] = local_date.strftime('%d-%m-%Y')
                result['time'] = local_date.strftime('%H:%M:%S')

            result['body'] = self.get_body(msg)

        return result

    def get_body(self, msg):
        """Получем текст письма
           :param msg: полученное письмо через fetch,
                       затем message_from_string(part[1].decode('utf-8'))
        """
        for part in msg.walk():
            #if not part.get_content_type() == 'text/plain':
            #    continue
            body = part.get_payload(decode=True)
            body = body.decode('utf-8')
            print(body)
            return kill_html(body)

    def all_letters(self, folder: str, page: int = 0, by: int = 3):
        """Выбор всех сообщений
           :param folder: папка с сообщениями
        """
        result = []
        self.select_folder(folder)
        letters = self.search('(ALL)')
        # Вытаскиваем письма
        letters = letters[::-1]
        start = page * by
        end = page * by + by
        for letter in letters[start:end]:
            retcode, data = self.conn.fetch(str(letter),'(RFC822)')
            if not retcode == 'OK':
                continue
            result.append({
                'id': letter,
                'email': self.get_headers(data),
            })
        return result


