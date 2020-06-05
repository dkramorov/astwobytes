# -*- coding:utf-8 -*-
import time
import urllib
import logging
import requests
import datetime

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# TODO: передвать через настройки
# client_id/token
# ids счетчиков для яндекс.метрики

class YandexMetrika:
    def __init__(self):
        # Чтобы получить токен, надо пройти по ссылке
        self.oauth_url = 'https://oauth.yandex.ru/authorize'
        self.oauth_params = {
            'response_type': 'token',
            'client_id': '7806598477db40c09ffad90b86ebba0f',
        }
        self.oauth_link = '%s?%s' % (self.oauth_url, '&'.join(self.oauth_params))

    def get_yandex_adv_clicks(self,
                              proxies: dict = None,
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

    def request(self, ids: list = [17621686], limit: int = 10, **kwargs):
        """Запрос в ЯндексМетрику
           https://yandex.ru/dev/metrika/doc/api2/api_v1/examples-docpage/
           :param ids: список номеров счетчиков
           :param limit: запрашиваемое кол-во
           :param kwargs: параметры запроса
           :return: словарь агрегация по метрике

           фильтр по операторам надо проводить в апострофах, например,
           params['filters'] = '(ym:s:bounceRate==100) AND (EXISTS(ym:s:paramsLevel1==\'ip\' AND ym:s:paramsLevel2==\'%s\'))' % ip
        """
        urla = 'https://api-metrika.yandex.net/stat/v1/data'
        params = {
            'ids': ids,
            'limit': limit,
            'pretty': True,
            'lang': 'ru',
        }
        params.update({k: v for k, v in kwargs.items()})
        r = requests.get(urla, params=params)
        print(urllib.parse.unquote(r.request.url))
        return r.json()

    def get_bad_users(self, **kwargs):
        """Получение тварей (отказы)"""
        params = {
            'metrics': 'ym:s:visits',
            'dimensions': 'ym:s:paramsLevel2',
            'date1': 'yesterday',
            'date2': 'today',
            'filters': '(ym:s:bounceRate==100)',
            'sort': '-ym:s:visits',
            'limit': 5,
            'lang': 'ru',
            'group': 'year',
        }
        params.update(kwargs)
        if kwargs.get('filters') and kwargs['filters']:
            params['filters'] += ' AND (ym:s:bounceRate==100)'
        return self.request(**params)

    def get_weak_users(self, **kwargs):
        """Получение тварей (отказы)"""
        params = {
            'metrics': 'ym:s:visits',
            'dimensions': 'ym:s:paramsLevel2',
            'date1': 'yesterday',
            'date2': 'today',
            'filters': '(ym:s:visitDuration<15)',
            'limit': 5,
            'lang': 'ru',
            'group': 'year',
        }
        params.update(kwargs)
        if kwargs.get('filters') and kwargs['filters']:
            params['filters'] += ' AND (ym:s:visitDuration<15)'
        return self.request(**params)

    def get_robots(self, **kwargs):
        """Получение предположительных роботов"""
        params = {
            'metrics': 'ym:s:visits',
            'dimensions': 'ym:s:paramsLevel2',
            'date1': 'yesterday',
            'date2': 'today',
            'filters': '(ym:s:isRobot==\'Yes\')',
            'sort': '-ym:s:visits',
            'limit': 5,
            'lang': 'ru',
            'group': 'year',
        }
        params.update(kwargs)
        if kwargs.get('filters') and kwargs['filters']:
            params['filters'] += ' AND (ym:s:isRobot==\'Yes\')'
        return self.request(**params)

if __name__ == '__main__':
    proxies = {
        'http'  : 'http://10.10.9.1:3128',
        'https' : 'http://10.10.9.1:3128',
    }
    now = datetime.date.today()
    long_ago = now - datetime.timedelta(days=90)

    ym = YandexMetrika()
    #print(get_yandex_adv_clicks(proxies=proxies))
    #print(get_bad_users(proxies=proxies))
    resp = ym.request(**{
        'metrics': 'ym:s:bounceRate,ym:s:visits',
        'dimensions': 'ym:s:paramsLevel2',
        #'date1': 'yesterday',
        #'date2': 'today',
        'date1': long_ago.strftime('%Y-%m-%d'),
        'date2': 'today',
        'filters': 'ym:s:bounceRate==100',
        'sort': '-ym:s:visits',
        #'filters': 'ym:s:paramsLevel2==\'188.225.74.89\'',
        'limit': 5,
    })
    print(resp)
    for item in resp.get('data'):
        print(item)