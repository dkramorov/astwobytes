#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TelegramBot:
    def __init__(self, token=None, proxies=None, chat_id=None):
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.proxies = proxies
        self.chat_id = chat_id

    def get_emoji(self, code=None):
        emoji = {'thunderstorm': '\U0001F4A8',    # Code: 200's, 900, 901, 902, 905
                 'drizzle': '\U0001F4A7',         # Code: 300's
                 'rain': '\U00002614',            # Code: 500's
                 'snowflake': '\U00002744',       # Code: 600's snowflake
                 'snowman': '\U000026C4',         # Code: 600's snowman, 903, 906
                 'atmosphere': '\U0001F301',      # Code: 700's foogy
                 'clearSky': '\U00002600',        # Code: 800 clear sky
                 'fewClouds': '\U000026C5',       # Code: 801 sun behind clouds
                 'clouds': '\U00002601',          # Code: 802-803-804 clouds general
                 'hot': '\U0001F525',             # Code: 904
                 'defaultEmoji': '\U0001F300',    # default emojis
                }
        return emoji.get(code, emoji['defaultEmoji'])

    def do_request(self, method="getMe", kwargs=None):
        if not kwargs:
            kwargs = {}
        urla = "{}{}".format(self.api_url, method)
        resp = requests.get(urla, kwargs, proxies=self.proxies)
        return resp.json()

    # -------------------------------------------
    # Чтобы получить идентификатор чата,
    # сначала отправляем сообщение в чат с ботом,
    # затем снимаем данные этим методом
    # -------------------------------------------
    def get_updates(self, offset=None, timeout=30):
        return self.do_request("getUpdates", {"timeout":timeout, "offset":offset})

    # --------------------------------
    # Отправка текстового сообщения,
    # можно воспользоваться parse_mode
    # parse_mode = "HTML" (<b>123</b>)
    # parse_mode = "Markdown"
    # --------------------------------
    def send_message(self, text, chat_id=None, parse_mode=None):
        params = {"chat_id":chat_id or self.chat_id, "text":text}
        if parse_mode:
            params['parse_mode'] = parse_mode
        try:
            resp = requests.post(
                "{}{}".format(self.api_url, "sendMessage"),
                params,
                proxies = self.proxies
            )
            if not resp.status_code == 200:
                logger.error("Telegram response: %s" % (resp.text, ))
                return {}
            return resp.json()
        except Exception as e:
            logger.error("Telegram и медный таз встретились на раз! %s" % str(e))
        return {}

    def send_document(self, input_file, caption='', chat_id=None):
        """Отправка файла в телеграм чат"""
        self.send_file(input_file, caption=caption, chat_id=chat_id, file_type='doc')

    def send_photo(self, input_file, caption='', chat_id=None):
        """Отправка файла в телеграм чат"""
        self.send_file(input_file, caption=caption, chat_id=chat_id, file_type='img')

    # ---------------------------------
    # USAGE:
    # передаем в f открытый дескриптор
    # fname = '/home/.../1.xlsx'
    # with open(fname, "rb") as f:
    #   TelegramBot().send_document(f))
    # ---------------------------------
    def send_file(self, input_file, caption='', chat_id=None, file_type: str = 'doc'):
        """Отправка файла в телеграм чат
           :param input_file: открытый дескриптор файла
           :param caption: заголовок файла
           :param chat_id: идентификатор чата
           :param file_type: тип файла
        """
        params = {'caption': caption, 'chat_id': chat_id or self.chat_id}
        method = 'sendDocument'
        files = {'document': input_file}
        if file_type == 'img':
            method = 'sendPhoto'
            files = {'photo': input_file}
        try:
            resp = requests.post(
                "{}{}".format(self.api_url, method),
                files=files,
                data=params,
                proxies=self.proxies
            )
            if not resp.status_code == 200:
                logger.error('Telegram response: %s' % (resp.text, ))
                return {}
            return resp.json()
        except Exception as e:
            logger.error('Telegram и медный таз встретились на раз! %s' % str(e))
        return {}
