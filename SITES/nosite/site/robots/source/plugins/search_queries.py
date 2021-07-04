import os
import json
import logging
import requests

from envparse import env
env.read_envfile()
API_SERVER = env('API_SERVER')
API_TOKEN = env('API_TOKEN')
PLUGINS_FOLDER = os.path.split(os.path.abspath(__file__))[0]
ROOT_FOLDER = os.path.split(PLUGINS_FOLDER)[0]

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def api_request(endpoint, params):
    """Запрос к апи
       :param endpoint: адрес api
       :param params: параметры запроса
    """
    result = []
    params.update({
        'page': 1,
        'by': 1,
    })
    endpoint = '%s%s' % (API_SERVER.rstrip('/'), endpoint)
    err_template = '[ERROR]: Api request error %s {}' % endpoint
    try:
        resp = requests.get(endpoint, params=params, timeout=5).json()
    except Exception:
        logger.exception(err_template.format(params))
        return result
    by = 500
    total_records = resp.get('total_records', 0)
    total_pages = total_records / by + 1
    for i in range(int(total_pages)):
        params['by'] = by
        params['page'] = i + 1
        try:
            resp = requests.get(endpoint, params=params, timeout=5).json()
            result += resp.get('data', [])
        except Exception:
            logger.exception(err_template.format(params))
    return result

def get_sites():
    """Получение сайтов"""
    endpoint = '/robots/sites/api/'
    params = {
        'only_fields': 'id,url',
    }
    result = api_request(endpoint, params)
    sites = {str(item['id']): item['url'] for item in result}
    dest = os.path.join(ROOT_FOLDER, 'sites.json')
    with open(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(sites))
    return sites

def load_sites():
    """Получения сайтов из файла"""
    sites_file = os.path.join(ROOT_FOLDER, 'sites.json')
    if not os.path.exists(sites_file):
        return get_sites()
    with open(sites_file, 'r', encoding='utf-8') as f:
        sites = json.loads(f.read())
    return sites

def search_site(site_id: int = None,
                site_url: str = None):
    """Вспомогательная функция
       для поиска сайта по ид/адресу
       :param site_id: ид сайта
       :param site_url: адрес сайта
    """
    site = {}
    sites = load_sites()
    if site_id:
        site_id = str(site_id)
        if site_id in sites:
            site = {
                'id': site_id,
                'domain': sites[site_id],
            }
    elif site_url:
        scheme, domain = site_url.split('//')
        domain = domain.split('/')[0]
        site_url = '%s//%s' % (scheme, domain)
        for k, v in sites.items():
            if v == site_url:
                site = {'id': k, 'domain': v}
    return site

def get_site_queries(site_id: int = None,
                     site_url: str = None):
    """Получение запросов по сайту
       :param site_id: ид сайта
       :param site_url: адрес сайта
    """
    site = search_site(site_id=site_id, site_url=site_url)

    endpoint = '/robots/search_queries/api/'
    params = {
        'only_fields': 'name',
        'filter__site__id': site['id'],
    }
    result = api_request(endpoint, params)
    search_queries = [item['name'] for item in result if item['name']]
    dest = os.path.join(ROOT_FOLDER, 'search_queries_%s.json' % site['id'])
    with open(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(search_queries))
    return search_queries

def load_site_queries(site_id: int):
    """Получения поисковых запросов из файла по сайту
       :param site_id: ид сайта
    """
    site_queries_file = os.path.join(ROOT_FOLDER, 'search_queries_%s.json' % site_id)
    if not os.path.exists(site_queries_file):
        return get_site_queries(site_id=site_id)
    with open(site_queries_file, 'r', encoding='utf-8') as f:
        site_queries = json.loads(f.read())
    return site_queries

def get_search_queries(site_url: str = 'https://223-223.ru'):
    """Получение списка поисковых запросов
       :param site_url: адрес сайта
    """
    site = search_site(site_url=site_url)
    search_queries = load_site_queries(site['id'])
    q_arr = [item.replace('"', '').replace('\'', '').replace(',', ' ').replace('(', '').replace(')', '').replace('.', ' ').replace('  ', ' ').replace('\t', '').strip()
             for item in search_queries if item]
    q_arr = list(set(q_arr))
    return q_arr


if __name__ == '__main__':
    #q_arr = get_search_queries()
    #print(json.dumps(q_arr, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False))

    ##JSON_QUERIES_PATH = '/home/jocker/selenium/json_queries.json'
    ##queries = update_search_queries(host='http://spam.223-223.ru')
    ##with open(JSON_QUERIES_PATH, 'w+', encoding='utf-8') as f:
    ##    f.write(json.dumps(queries, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False))

    #print(len(queries))
    #get_search_queries(with_update = True)

    # Проверка на получение сайтов и запросов для сайта
    #print(get_sites())
    #get_site_queries(site_id=2)
    #get_site_queries(site_url='https://8800из-за-бугра.рф')
    #assert get_site_queries(site_id=2) == get_site_queries(site_url='https://8800из-за-бугра.рф')


    print(get_search_queries())