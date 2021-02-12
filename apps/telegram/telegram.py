# -*- coding: utf-8 -*-
import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)

# -------------------------------
# Телеграм-бот для информирования
# -------------------------------
class TelegramBot:
    # proxies = {'http': 'socks5://10.10.9.1:3333', 'https': 'socks5://10.10.9.1:3333'}
    # proxies = {'http': 'http://10.10.9.1:3128', 'https': 'https://10.10.9.1:3128'}
    def __init__(self, token=None, proxies=None, chat_id=None):
        token_from_settings = None
        if hasattr(settings, 'TELEGRAM_TOKEN'):
            token_from_settings = settings.TELEGRAM_TOKEN
        token = token or token_from_settings
        if not token:
            logger.error('TELEGRAM_TOKEN is undefined')
            assert False

        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
        if not proxies and settings.TELEGRAM_PROXY:
            proxies = {
                'http': settings.TELEGRAM_PROXY,
                'https': settings.TELEGRAM_PROXY,
            }
        self.proxies = proxies
        self.chat_id = chat_id or settings.TELEGRAM_CHAT_ID

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

    def do_request(self, method='getMe', kwargs=None):
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
        return self.do_request('getUpdates', {
            'timeout': timeout,
            'offset': offset
        })

    # --------------------------------
    # Отправка текстового сообщения,
    # можно воспользоваться parse_mode
    # parse_mode = 'HTML' (<b>123</b>)
    # parse_mode = 'Markdown'
    # --------------------------------
    def send_message(self, text: str,
                     chat_id: int = None,
                     parse_mode: str = None,
                     disable_web_page_preview: bool = False,
                     timeout: int = 20):
        if not settings.TELEGRAM_ENABLED:
            return {'error': 'Telegram is disabled in settings'}
        params = {
            'chat_id': chat_id or self.chat_id,
            'text': text,
            'disable_web_page_preview': disable_web_page_preview,
        }
        if parse_mode:
            params['parse_mode'] = parse_mode
        try:
            resp = requests.post(
                "{}{}".format(self.api_url, 'sendMessage'),
                params,
                proxies = self.proxies,
                timeout = timeout
            )
            if not resp.status_code == 200:
                logger.error('Telegram response: %s' % (resp.text, ))
                return {}
            return resp.json()
        except Exception as e:
            logger.error('Telegram и медный таз встретились на раз! %s' % str(e))
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
    def send_file(self, input_file,
                  caption='',
                  chat_id=None,
                  file_type: str = 'doc',
                  timeout: int = 20):
        """Отправка файла в телеграм чат
           :param input_file: открытый дескриптор файла
           :param caption: заголовок файла
           :param chat_id: идентификатор чата
           :param file_type: тип файла
        """
        if not settings.TELEGRAM_ENABLED:
            return {'error': 'Telegram is disabled in settings'}
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
                proxies=self.proxies,
                timeout = timeout
            )
            if not resp.status_code == 200:
                logger.error('Telegram response: %s' % (resp.text, ))
                return {}
            return resp.json()
        except Exception as e:
            logger.error('Telegram и медный таз встретились на раз! %s' % str(e))
        return {}
