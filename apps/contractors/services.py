#-*- coding:utf-8 -*-
import os
import requests
import logging

logger = logging.getLogger('simple')

def get_info_by_inn(inn: str):
    """Получение данные по ИНН
       :param inn: ИНН
    """
    result = {}
    if not inn:
        return result
    url = 'https://egrul.nalog.ru/'
    s = requests.Session()
    params = {
        'vyp3CaptchaToken': '',
        'page': '',
        'query': inn,
        'region': '',
        'PreventChromeAutocomplete': '',
    }
    r = s.post(url, data=params)
    resp = r.json()
    r = s.get('%ssearch-result/%s' % (url, resp['t']))
    resp = r.json()
    rows = resp.get('rows', [])
    if rows:
        row = rows[0]
        result = {
            'address': row.get('a', ''),
            'name': row.get('c', ''),
            'director': row.get('g', ''),
            'inn': row.get('i', ''),
            'type': row.get('k', ''),
            'full_name': row.get('n', ''),
            'ogrn': row.get('o', ''),
            'kpp': row.get('p', ''),
            'reg': row.get('r', ''),
        }
    return result
