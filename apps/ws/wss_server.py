#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import asyncio
import time
import datetime
import random
import websockets
import json
import pathlib
import ssl
import requests

import jwt
#>>> encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
#'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
#>>> jwt.decode(encoded, 'secret', algorithms=['HS256'])
#{'some': 'payload'}

#import redis
#r = redis.StrictRedis(host='localhost', port=6379, db=0)
#r.set('foo', 'bar')
#r.get('foo')
#>>>'bar'
#r.delete('foo')

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from envparse import env
env.read_envfile()

API_URL = env('API_URL', default='http://localhost:8000') # Для сохранения в БД
#import MySQLdb
#DB = MySQLdb.connect(db=env('DB', default='astwobytes'),
#                     user=env('DB_USER', default='root'),
#                     passwd=env('DB_PASSWD', default=''), )

SECRET = env('SECRET', default='se')
HOST = env('HOST', default='127.0.0.1')
PORT = env('PORT', cast=int, default=8888)
CERT_PATH = env('CERT_PATH', default='')
USERS = set()

async def consumer_handler(websocket, path):
    """receiving messages and passing them to a consumer coroutine"""
    async for message in websocket:
        msg = json.loads(message)
        if not type(msg) == dict:
            return
        if not await consumer(websocket, msg):
            return

async def consumer(websocket, msg):
    """Обработка сообщения от клиента"""
    logger.info('[RECEIVED]: %s', msg)
    if not hasattr(websocket, 'user'):
        websocket.user = await auth_user(msg)
        await register_user(websocket)
        await websocket.send(json.dumps({'action': 'auth'}))
        # Всем разослать, что новый пользователь подрубился
        await send_list_users()
    if not websocket.user:
        return False
    # нет действия - ну и пнх
    if not msg.get('action'):
        return False
    await ws_actions(websocket, msg)
    return True

async def producer_handler(websocket, path):
    """getting messages from a producer coroutine and sending them"""
    while True:
        msg = await producer()
        if msg:
            await websocket.send(msg)
        await asyncio.sleep(0.1)

async def producer():
    """Подготовка сообщения для клиента"""
    #random_msg = random.randint(0, 100)
    #if random_msg > 90:
        #return 'random_msg'
    pass

async def register_user(websocket):
    """Регистрация нового пользователя"""
    USERS.add(websocket)
    #print(dir(websocket))
    #print(websocket.remote_address)
    #print(websocket.request_headers)

async def auth_user(msg):
    """Авторизация пользователя
    Пользователь должен быть уже авторизован на клиенте,
    в противном случае - не надо совсем создавать соединение,
    клиент отправляет jwt токен нам, который выдан при авторизации,
    мы его расшифровываем и должно получиться имя пользователя,
    - секретный ключ для расшифровки на сервере авторизации и здесь
    """
    user = msg.get('user')
    token = msg.get('token')
    if not token or not user:
        return None
    auth = jwt.decode(token, SECRET)
    if auth['token'] == user:
        return user
    return None

async def unregister_user(websocket):
    """Закрытие соединения с пользователем"""
    USERS.remove(websocket)
    await send_list_users()

async def send_list_users():
    """Отправляем всем список подключенных пользователей"""
    users = set([ws.user for ws in USERS])
    [await ws.send(json.dumps({
        'action': 'users_list',
        'users_list': list(users)
    })) for ws in USERS]

async def save_user_msg(msg):
    """Отправка по апи сообщения пользователя в БД"""
    endpoint = '/ws/messages/api/'
    params = {'msg': msg, 'token': SECRET}
    resp = requests.post('%s%s' % (API_URL, endpoint), json=params)
    if resp.status_code != 200:
        logger.error(resp.text)

async def ws_actions(websocket, msg):
    """Действия вебсокета"""
    if not hasattr(websocket, 'user') or not websocket.user == msg.get('user'):
        return
    updated = time.time()
    now = datetime.datetime.today()
    now_date = now.strftime('%d-%m-%Y')
    now_time = now.strftime('%H:%M')
    action = msg.get('action')
    if action == 'bcast_msg':
        bcast_msg = msg.get(action, '').strip()
        if bcast_msg:
            obj = {
                'from': websocket.user,
                'action': action,
                action: bcast_msg,
                'date': now_date,
                'time': now_time,
                'updated': updated,
            }
            [await ws.send(json.dumps(obj)) for ws in USERS]
            await save_user_msg(obj)
    elif action in ('to_user', 'to_group'):
        user_msg = msg.get('msg', '').strip()
        to_user = msg.get(action, '')
        if isinstance(to_user, str):
            to_user = to_user.strip()
        if to_user and user_msg:
            obj = {
                'group_id': msg.get('group_id'),
                'from': websocket.user,
                'action': action,
                'to': to_user,
                'msg': user_msg,
                'date': now_date,
                'time': now_time,
                'updated': updated,
            }
            if action == 'to_group':
                users = []
                for ws in USERS:
                    if ws.user in to_user:
                        users.append(ws)
                [await ws.send(json.dumps(obj)) for ws in users]
            else:
                users = filter(lambda x: x.user == to_user, USERS)
                [await ws.send(json.dumps(obj)) for ws in users]
            await save_user_msg(obj)
    elif action == 'users_list':
        await send_list_users()

async def handler(websocket, path):
    """consumer and producer same time"""
    #await register_user(websocket) # пока еще нет авторизации websocket.user
    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()
    await unregister_user(websocket)

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

start_server = websockets.serve(handler, HOST, PORT, ssl=ssl_context)
logger.info('[SERVER STARTED]: HOST %s, PORT %s' % (HOST, PORT))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


