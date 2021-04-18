# -*- coding:utf-8 -*-
import time
import logging
import requests

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ---------------------------
# Получение информации по РСЯ
# ---------------------------
def get_yandex_oauth_token(driver):
    """Получение токена можно автоматизировать, но надо авторизовываться в Яндекс"""
    urla = 'https://oauth.yandex.ru/authorize'
    urla += '?response_type=token'
    urla += '&client_id=7806598477db40c09ffad90b86ebba0f'
    driver.goto(urla)

def get_yandex_adv_clicks(proxies: dict = None,
                          period: str = 'today',
                          token: str = 'AgAAAAAE9l-KAALM0NdBwLmQN0X-uZOvTsc766I'):
    """Получаем кол-во кликов по Яндекс.Директ"""
    params = {
        'oauth_token': token,
        'lang': 'ru',
        'pretty': 1,
        'period': period,
        'level': 'advnet_context_on_site',
        'field': 'direct_context_clicks',
        'field': 'rtb_block_all_hits',
        'field': 'partner_wo_nds',
    }
    if not proxies:
        proxies = {}
    try:
        r = requests.get('https://partner2.yandex.ru/api/statistics/get.json',
                     params=params, proxies=proxies, timeout=5)
        resp = r.json()
        data = resp.get('data', [])
        values = data.get('data', [])
        if not values:
            return {}
    except Exception as e:
        logger.error(e)
        values = {}
    return values


if __name__ == '__main__':

   print(get_yandex_adv_clicks(proxies={
              'http'  : 'http://10.10.9.1:3128',
              'https' : 'http://10.10.9.1:3128',
            }))