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
    """Получение токена можно автоматизировать,
       но надо авторизовываться в Яндекс
    """
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
    headers = {
        'Authorization': 'OAuth %s' % token
    }
    try:
        r = requests.get('https://partner2.yandex.ru/api/statistics2/get.json',
                     params=params, proxies=proxies, headers=headers, timeout=5)
        resp = r.json()
        data = resp.get('data', {})
        values = data.get('totals', {})
        if not values:
            logger.info(resp)
            return {}
    except Exception as e:
        logger.error(e)
        values = {}

    #keys = list(values.keys())
    #if keys:
    #    balance_list = values[keys[0]]
    #    fbalance = list(filter(lambda x:x.get('partner_wo_nds', ''), balance_list))
    #    if fbalance:
    #        balance = fbalance[0]['partner_wo_nds']

    return values


if __name__ == '__main__':

   print(get_yandex_adv_clicks(proxies={
              'http'  : 'http://10.10.9.1:3128',
              'https' : 'http://10.10.9.1:3128',
            }))