#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import asyncio
import time
import datetime
import websockets
import json
import math
import ssl
import requests
import redis

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from envparse import env
env.read_envfile()

TELEGRAM_PROXY = env('TELEGRAM_PROXY', default='http://10.10.9.1:3128')
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = env('TELEGRAM_CHAT_ID')

rediska = redis.StrictRedis()

def json_pretty_print(json_obj):
    """Вывести json в человеческом виде"""
    return json.dumps(json_obj, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)

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

class MathOperations:
    """Различные математические операции"""

    @staticmethod
    def martingail(digit: int, step: int, multiply: int = 2) -> float:
        """Стратегия Мартингейла
           У нас есть число digit,
           нам надо каждый шаг step удваивать это число
           :param digit: сумма ставки
           :param step: текущий шаг проигрышей подряд
           :param multiply: во сколько раз увеличиваем

           0.35 ставка, выплата 0.66
           35 = 66 (66-35=31 сколько это % от 35?)
           35   100%
           31   ?% 88% => 12% комиссия

           0.7 ставка, выплата 1.36
           70 = 136 (136-70=66 сколько это % от 70?)
           70   100%
           66   ?% 94% => 6% комиссия

           1.4 ставка, выплата 2.72
           140 = 272 (272-140=132 сколько это % от 140?)
           140 = 100%
           132 = ?% 94% => 6% комиссия

           2.8 ставка, выплата 5.44
           280 = 544 (544-280=264 сколько это % от 280?)
           280 = 100%
           264 = ?% 94% => 6% комиссия

           multiply => множитель, по умолчанию 2,
           с множителем в 1,5 можно 6 повторов сделать"""
        summa = 0
        percent = 6
        for i in range(step):
            if i == 0:
                summa += digit
            else:
                # От удваемого числа нужно плюсануть 6%
                # на первом шаге 12%, согласно расчетам
                if i == 1:
                    percent = 12
                six_percents = summa / 100 * percent
                summa = summa * multiply + six_percents
        return summa

class StateMachine:
    def __init__(self):
        self.authorized = False
        self.balance_subscribed = False

        self.account = {}
        self.balance = {}
        self.step = 1

        self.telegram = TelegramBot(token=TELEGRAM_TOKEN,
                                    proxies={'http': TELEGRAM_PROXY,
                                             'https': TELEGRAM_PROXY},
                                    chat_id=TELEGRAM_CHAT_ID)

        self.deals_data = []
        self.token = 'vwG5V6Vo66jUpqq'

    def auth(self):
        """Авторизация"""
        return json.dumps({
            'authorize': self.token,
        })

    def ping(self):
        """Пинг для поддержания соединения"""
        return json.dumps({
            'ping': 1
        })

    def subscribe_balance(self):
        """Подписаться на обновления баланса потоком"""
        return json.dumps({
            'balance': 1,
            'account': 'current',
            'subscribe': 1,
        })

    def calc_rates(self):
        digit = 0.35
        max_loose_count = 5
        multiply = 2
        # Если умудрились max раз подряд всрать пишем в статистику
        #if self.step > self.stats_data.max_loose_in_sequence:
        #    self.stats_data.max_loose_in_sequence = self.step
        while self.step > max_loose_count:
            self.step = self.step - max_loose_count;
        result = MathOperations.martingail(digit, self.step, multiply)
        return round(result, 2)

    def follow_deal(self, deal):
        """Следим за сделкой - правильно ее закрываем
           :param deal: новая информация о сделке"""
        for i in range(len(self.deals_data)):
            if self.deals_data[i]['contract_id'] == deal['contract_id']:
                self.deals_data[i] = deal
                transactions = deal.get('transaction_ids')
                if 'sell' in transactions:
                    self.in_deal = False
                    profit = deal['profit']
                    if profit < 0:
                        self.step += 1
                    else:
                        self.step = 1
                    msg = 'REAL DEAL %s, profit %s, balance %s' % (deal.get('status'), profit, self.balance.get('balance'))
                    logger.info(msg)
                    self.telegram.send_message(msg)

    def refresh(self):
        """Мягкий перезапуск"""
        self.authorized = False
        self.balance_subscribed = False
        self.account = {}
        logger.info('[REFRESH STATE MACHINE]')


def timestamp_to_date(stamp):
    """time.time() to datetime.datetime"""
    try:
        stamp = int(stamp)
    except ValueError:
        return None
    result = datetime.datetime.fromtimestamp(stamp)
    return result

async def consumer_handler(websocket, state_machine):
    """receiving messages and passing them to a consumer coroutine"""
    async for message in websocket:
        data = json.loads(message)
        if not type(data) == dict:
            return
        action = data['msg_type']
        if action == 'authorize':
            # Авторизация
            state_machine.account = data[action]
        elif action == 'buy':
            if action in data:
                state_machine.deals_data.append(data[action])
            else:
                logger.info(json_pretty_print(data))
        elif action == 'proposal_open_contract':
            state_machine.follow_deal(data[action])
        elif action == 'balance':
            if action in data:
                state_machine.balance = data[action]
            else:
                logger.info(json_pretty_print(data))
        else:
            logger.warning(data)

async def producer_handler(websocket, state_machine):
    """getting messages from a producer coroutine and sending them"""
    if not state_machine.authorized:
        # 1) Авторизация
        state_machine.authorized = True
        await websocket.send(state_machine.auth())
    elif not state_machine.balance_subscribed:
        # 4) Подписываемся на обновления баланса потоком
        state_machine.balance_subscribed = True
        await websocket.send(state_machine.subscribe_balance())
    #elif not state_machine.in_deal:
        # TEST
        #state_machine.in_deal = True
        #await websocket.send(state_machine.buy_from_playboy('CALL'))
    else:
        deal = rediska.get('binary_bot_deal')
        if deal:
            rediska.delete('binary_bot_deal')
            deal = json.loads(deal)
            price = state_machine.calc_rates()
            deal['price'] = price
            deal['parameters']['amount'] = price
            await websocket.send(json.dumps(deal))

async def check_events(websocket, state_machine):
    """Консьюмер и продюсер события"""
    time.sleep(0.1)

    # TEST break connection
    #await websocket.close()

    consumer_task = asyncio.ensure_future(consumer_handler(websocket, state_machine))
    producer_task = asyncio.ensure_future(producer_handler(websocket, state_machine))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

async def main_loop(state_machine):
    """Основной цикл бота"""
    uri = 'wss://ws.binaryws.com/websockets/v3?app_id=1089&l=RU'
    ssl_context = ssl.SSLContext()
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        while True:
            # Проверка, что вебсокет еще не закрыл соединение
            if hasattr(websocket, 'close_code'):
                logger.error('[ERROR]: websocket closed code %s, reason %s' % (websocket.close_code, websocket.close_reason))
                state_machine.refresh()
                time.sleep(5)
                break
            await check_events(websocket, state_machine)

async def handler():
    """Подключение к binary.com"""
    state_machine = StateMachine()
    while True:
        await main_loop(state_machine)


logger.info('[BOT STARTED]')
asyncio.get_event_loop().run_until_complete(handler())

