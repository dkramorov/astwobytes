#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import asyncio
import time
import datetime
import websockets
import json
import ssl
import requests
import redis
import random

from telegram import TelegramBot
from math_operations import MathOperations
from strategies import strategy_opposite_touches

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from envparse import env
env.read_envfile()

TELEGRAM_PROXY = env('TELEGRAM_PROXY', default='http://10.10.9.1:3128')
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = env('TELEGRAM_CHAT_ID')
WITH_REDIS = env('WITH_REDIS', default=False)

rediska = redis.StrictRedis()

def json_pretty_print(json_obj):
    """Вывести json в человеческом виде"""
    return json.dumps(json_obj, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)

class StateMachine:
    def __init__(self):
        self.authorized = False
        self.ticks_history_received = False
        self.ticks_subscribed = False
        self.balance_subscribed = False
        self.in_deal = False
        self.symbols_showed = False
        self.strategy = 'random'
        #self.strategy = 'bollinger'

        self.account = {}
        self.balance = {}
        self.step = 1
        self.loose_counter = 0
        self.last_update = time.time()

        self.telegram = TelegramBot(token=TELEGRAM_TOKEN,
                                    proxies={'http': TELEGRAM_PROXY,
                                             'https': TELEGRAM_PROXY},
                                    chat_id=TELEGRAM_CHAT_ID)

        self.max_loose = 5
        self.max_ticks = 100
        self.max_timeout = 300
        self.symbol = 'R_50' # При смене контракта все надо обнулить (методом)
        self.min_bet = 0.35

        #self.symbol = 'frxEURUSD'
        #self.min_bet = 0.50

        self.ticks_data = []
        self.deals_data = []
        self.bollinger_bands_steps = 20
        self.standard_deviations = 2
        self.token = 'S2CdZcfFPZ6Q0A2'

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

    def get_active_symbols(self):
        return json.dumps({
            'active_symbols': 'brief',
            'product_type': 'basic',
        })

    def get_ticks_history(self) -> str:
        """Получить историю по тикам"""
        return json.dumps({
           'ticks_history': self.symbol,
           'end': 'latest',
           'start': 1,
           'style': 'ticks',
           'adjust_start_time': 1,
           'count': self.max_ticks,
        })

    def subscribe_ticks(self):
        """Подписаться на обновления тиков потоком"""
        return json.dumps({
            'ticks': self.symbol,
            'subscribe': 1,
        })

    def subscribe_balance(self):
        """Подписаться на обновления баланса потоком"""
        return json.dumps({
            'balance': 1,
            'account': 'current',
            'subscribe': 1,
        })

    def save_new_ticks(self, symbol: str, history: list):
        """Записываем массив тиков"""
        if not symbol == self.symbol:
            logger.error('[ERROR]: symbol %s is incorrect, we wanna %s' % (symbol, self.symbol))
            return
        self.ticks_data = []
        self.deals_data = []
        if not history:
            return
        for i, item in enumerate(history['prices']):
            tick = {
                'symbol': symbol,
                'quote': item,
                'epoch': history['times'][i],
            }
            self.save_new_tick(tick, with_pop = False)

    def save_new_tick(self, tick: dict, with_pop: bool = True):
        """Сохранение в массив нового тика
           :param tick: тик
           :param with_pop: Удалить первый тик"""
        if not tick['symbol'] == self.symbol:
            logger.error('[ERROR]: symbol %s is incorrect, we wanna %s' % (tick['symbol'], self.symbol))
            return
        self.ticks_data.append([tick['epoch'], tick['quote']])
        if with_pop:
            self.ticks_data.pop(0)

        # Докидываем боллинджера в тик
        # третий элемент массива в
        # каждом тике со словарем
        prices = [item[1] for item in self.ticks_data]
        for i, cur_tick in enumerate(self.ticks_data):
            if len(cur_tick) < 3:
                # Линии болленджера
                # top, middle, bottom
                bb = MathOperations.bollinger_bands(prices, i,
                    self.bollinger_bands_steps,
                    self.standard_deviations)
                cur_tick.append(bb)

    def playboy(self, reverse: bool = False):
        """Играем по-черном
           Покупка =>
           Цена пересекает среднюю линию
           канала Боллинджера или касается ее
           После этого касается крайней
           линии канала Боллинджера
           + Покупка делается противоположно
           :param reverse: для реверсивной покупки"""
        # Ищем по контракту последнюю сделку,
        # от нее считать будем
        CALL = 'CALL'
        PUT = 'PUT'
        if reverse:
            CALL = 'PUT'
            PUT = 'CALL'

        # Случайная стратегия, просто для проверки
        if self.strategy == 'random':
            types = (CALL, PUT)
            return self.buy_from_playboy(types[random.randint(0, len(types)-1)])
        elif self.strategy == 'bollinger':
            result = strategy_opposite_touches(self.ticks_data)
            if result['action']:
                return self.buy_from_playboy(result['action'])

    def buy_from_playboy(self, direction):
        """Делаем ставку, что там по мартингейлу?"""
        self.in_deal = True
        self.last_update = time.time()
        amount = self.calc_rates()
        return json.dumps({
            'price': amount,
            'buy': 1,
            'subscribe': 1,
            'parameters': {
                'contract_type': direction,
                'symbol': self.symbol,
                'duration_unit': 't',
                'duration': 5,
                'basis': 'stake',
                'currency': 'USD',
                'amount': amount,
            }
        })

    def calc_rates(self):
        digit = self.min_bet #0.35
        multiply = 2
        # Если умудрились max раз подряд всрать пишем в статистику
        #if self.step > self.stats_data.max_loose_in_sequence:
        #    self.stats_data.max_loose_in_sequence = self.step
        while self.step > self.max_loose:
            self.step = self.step - self.max_loose
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
                        self.loose_counter += 1
                    else:
                        self.step = 1
                        self.loose_counter = 0
                    msg = 'DEAL %s, profit %s, balance %s' % (deal.get('status'), profit, self.balance.get('balance'))
                    logger.info(msg)
                    self.telegram.send_message(msg)

    def refresh(self):
        """Мягкий перезапуск"""
        self.authorized = False
        self.ticks_history_received = False
        self.ticks_subscribed = False
        self.balance_subscribed = False
        self.account = {}
        self.ticks_data = []
        # TODO: если мы были в сделке обыграть
        if self.in_deal and self.deals_data:
            logger.info('[IN DEAL]: %s' % (json_pretty_print(self.deals_data.pop())))
        self.in_deal = False
        logger.info('[REFRESH STATE MACHINE]')

    def check_pulse(self):
        """Проверить, что обновления идут"""
        if time.time() - self.last_update > self.max_timeout:
            return False
        return True

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
        elif action == 'history':
            # Сохраняем полученную историю тиков
            symbol = data['echo_req']['ticks_history']
            state_machine.save_new_ticks(symbol, data[action])
        elif action == 'tick':
            # Получаем тик по подписке
            symbol = data['echo_req']['ticks']
            state_machine.save_new_tick(data[action])
            if not state_machine.in_deal:
                deal = state_machine.playboy()
                if deal:
                    await websocket.send(deal)
                    if WITH_REDIS and state_machine.loose_counter >= state_machine.max_loose:
                        rediska.set('binary_bot_deal', deal)
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
        elif action == 'active_symbols':
            logger.info(json_pretty_print(data))
        else:
            logger.warning(data)

async def producer_handler(websocket, state_machine):
    """getting messages from a producer coroutine and sending them"""
    if not state_machine.symbols_showed:
        # Показываем контракты
        state_machine.symbols_showed = True
        await websocket.send(state_machine.get_active_symbols())
    if not state_machine.authorized:
        # 1) Авторизация
        state_machine.authorized = True
        await websocket.send(state_machine.auth())
    elif not state_machine.ticks_history_received:
        # 2) Получем историю
        state_machine.ticks_history_received = True
        await websocket.send(state_machine.get_ticks_history())
    elif not state_machine.ticks_subscribed:
        # 3) Подписываемся на обновления тиков потоком
        state_machine.ticks_subscribed = True
        await websocket.send(state_machine.subscribe_ticks())
    elif not state_machine.balance_subscribed:
        # 4) Подписываемся на обновления баланса потоком
        state_machine.balance_subscribed = True
        await websocket.send(state_machine.subscribe_balance())
    #elif not state_machine.in_deal:
        # TEST
        #state_machine.in_deal = True
        #await websocket.send(state_machine.buy_from_playboy('CALL'))
    else:
        # Если тики по подписке не приходят,
        # тогда надо к херам отсоединяться
        pulse = state_machine.check_pulse()
        if not pulse:
            await websocket.close()

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

