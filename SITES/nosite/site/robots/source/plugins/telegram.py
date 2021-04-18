# -*- coding: utf-8 -*-
import logging
import requests
import socket

logger = logging.getLogger(__name__)

class TelegramBot:
    """Телеграм-бот для информирования
       proxies = {'http': 'socks5://10.10.9.1:3333', 'https': 'socks5://10.10.9.1:3333'}
       proxies = {'http': 'http://10.10.9.1:3128', 'https': 'https://10.10.9.1:3128'}
       USAGE:
        kwargs = {
            'headless': True,
            'plugins': {
                'skype': {},
                'telegram': {
                    'proxies': {
                        'http': 'http://10.10.9.1:3128',
                        'https': 'http://10.10.9.1:3128',
                    },
                    'token': '1006956431:AAErJ0b8X28rBVVpPsEt8QuDFrciHSeNLhk',
                    'chat_id': '-344346652',
                }
            },
        }
        ...
        driver.telegram.send_message('test')
    """

    def __init__(self, token=None, proxies=None, chat_id=None):
        if not token:
            logger.error('TELEGRAM_TOKEN is undefined')
            assert False
        self.timeout = 5
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
        resp = requests.get(urla, kwargs, proxies=self.proxies, timeout=self.timeout)
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
    def send_message(self, text: str, chat_id: int = None, parse_mode: str = None,
                     disable_web_page_preview: bool = False):
        params = {
            'chat_id': chat_id or self.chat_id,
            'text': '%s \n...%s' % (text, socket.gethostname()),
            'disable_web_page_preview': disable_web_page_preview,
        }
        if parse_mode:
            params['parse_mode'] = parse_mode
        try:
            resp = requests.post(
                "{}{}".format(self.api_url, 'sendMessage'),
                params,
                proxies = self.proxies,
                timeout = self.timeout
            )
            if not resp.status_code == 200:
                logger.error('Telegram response: %s' % (resp.text, ))
                return {}
            return resp.json()
        except Exception as e:
            logger.error('Telegram и медный таз встретились на раз! %s' % str(e))
        return {}

    # ---------------------------------
    # USAGE:
    # передаем в f открытый дескриптор
    # fname = "/home/.../1.xlsx"
    # with open(fname, 'rb') as f:
    #   TelegramBot().send_document(f))
    # ---------------------------------
    def send_document(self, input_file, caption="", chat_id=None):
        params = {'caption': caption, 'chat_id': chat_id or self.chat_id}
        files = {'document': input_file}
        try:
            resp = requests.post(
                '{}{}'.format(self.api_url, 'sendDocument'),
                files = files,
                data = params,
                proxies = self.proxies,
                timeout = self.timeout
            )
            if not resp.status_code == 200:
                logger.error('Telegram response: %s' % (resp.text, ))
                return {}
            return resp.json()
        except Exception as e:
            logger.error('Telegram и медный таз встретились на раз! %s' % str(e))
        return {}
