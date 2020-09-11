#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import datetime
import logging
import pathlib
import ssl
import asyncio
import websockets
import json
import requests
import random
import MySQLdb

#https://github.com/varvet/mobile-websocket-example/blob/master/android/WebsocketExampleClientProject/WebsocketExampleClient/src/main/java/se/elabs/websocketexampleclient/MainActivity.java

"""СМС-HUB принимает и раздает смски для отправки,
   все через веб-сокет, нахуй все эти базы данных и кэши
"""

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from envparse import env
env.read_envfile()

TELEGRAM_PROXY = env('TELEGRAM_PROXY', default='')
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = env('TELEGRAM_CHAT_ID')
WITH_REDIS = env('WITH_REDIS', default=False)
if WITH_REDIS:
    import redis
    rediska = redis.StrictRedis()

TOKEN = env('TOKEN', default='')
API_URL = env('API_URL', default='')
PORT = env('PORT', default='', cast=int)
HOST = env('HOST', default='')
CERT_PATH = env('CERT_PATH', default='')

DB_HOST = env('DB_HOST', default='')
DB_USER = env('DB_USER', default='')
DB_PASSWD = env('DB_PASSWD', default='')
DB_NAME = env('DB_NAME', default='')

logger.info('Arguments: %s: %s', len(sys.argv), sys.argv)
if len(sys.argv) > 1:
    TOKEN = sys.argv[1]
if len(sys.argv) > 2:
    API_URL = sys.argv[2]

class DB:
    """Класс для запросов к базе данных"""
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = MySQLdb.connect(host=DB_HOST,
                                    user=DB_USER,
                                    passwd=DB_PASSWD,
                                    db=DB_NAME, )
        self.conn.autocommit(True)

    def query(self, sql: str, params: list):
        """Запрос в базу данных,
           например,
           sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
           params = ("John", "Highway 21")
        """
        try:
            if self.cursor:
                self.cursor.close()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, params)
        except Exception as e:
            logger.error('[ERROR]: %s' % e)
            self.connect()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, params)
        return self.cursor

db = DB()
PHONES = set()

def json_pretty_print(json_obj):
    """Вывести json в человеческом виде"""
    return json.dumps(json_obj, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)

async def consumer_handler(websocket, path):
    async for message in websocket:
        print('received', message)
        try:
            json_obj = json.loads(message)
        except Exception as e:
            logger.error(e)
            return
        if not isinstance(json_obj, dict):
            return
        # token обязателен для json
        if not 'token' in json_obj or not json_obj['token'] == TOKEN:
            logger.error('TOKEN incorrent')
            return
        # регистрация телефона
        if 'register' in json_obj:
            table_name = 'spamcha_smsphone'
            reg_obj = json_obj['register']
            for key, data in reg_obj.items():
                icc_id = data.get('icc_id')
                number = data.get('number')
                display_name = data.get('display_name')
                query = 'select id from {} where code=%s'.format(table_name)
                params = (icc_id, )
                cursor = db.query(query, params)
                rows = cursor.fetchall()
                if rows:
                    continue
                created = datetime.datetime.today()
                query = """insert into {}(name, phone, code, created, updated, is_active) values(%s, %s, %s, %s, %s, 1)""".format(table_name)
                params = (display_name, number, icc_id, created, created)
                cursor = db.query(query, params)
                logger.info('new phone %s' % icc_id)
            websocket.icc_id = icc_id
            await websocket.send(json.dumps({'register': 'success'}))
        # получение списка телефонов
        elif 'get_phones' in json_obj:
            phones = {'get_phones': [ws.icc_id for ws in PHONES if hasattr(ws, 'icc_id')]}
            await websocket.send(json.dumps(phones))
        # найти телефон
        elif 'find_phone' in json_obj:
            find_phones = [ws for ws in PHONES if hasattr(ws, 'icc_id') and ws.icc_id == json_obj['find_phone']]
            for ws in find_phones:
                await ws.send(json.dumps({'find_phone': ws.icc_id}))

async def producer_handler(websocket, path):
    rand = random.random()
    if rand > 0.9:
        now = '%s' % time.time()
        print('send', now)
        await websocket.send(now)

async def main_loop(websocket, path):
    """Основной цикл websocket соединений
       Консьюмер и продюсер событий
    """
    time.sleep(0.1)
    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

async def handler(websocket, path):
    """Основной обработчик websocket соединений"""
    PHONES.add(websocket)
    while True:
        try:
            if websocket.closed:
                logger.error('closed websocket')
                PHONES.remove(websocket)
                break
            await main_loop(websocket, path)
        except Exception as e:
            logger.error(e)
        time.sleep(0.1)

# ---
# WSS
# ---
ssl_context = None
if CERT_PATH:
    logger.info('CERT_PATH %s' % (CERT_PATH, ))
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #localhost_pem = pathlib.Path(__file__).with_name('%sfullchain.pem' % (CERT_PATH, ))
    #ca_cert = pathlib.Path(__file__).with_name('%sprivkey.pem' % (CERT_PATH, ))
    localhost_pem = pathlib.Path(CERT_PATH).with_name('fullchain.pem')
    logger.info('fullchain=> %s' % (localhost_pem, ))
    ca_cert = pathlib.Path(CERT_PATH).with_name('privkey.pem')
    logger.info('privkey=>%s' % (ca_cert, ))
    ssl_context.load_cert_chain(localhost_pem, keyfile=ca_cert)

start_server = websockets.server.serve(handler, HOST, PORT, ssl=ssl_context)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
