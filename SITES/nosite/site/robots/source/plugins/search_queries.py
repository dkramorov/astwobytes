import os
import json
import logging
import requests

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def update_search_queries(host: str = 'http://spam.223-223.ru'):
    """Обновление поисковых запросов по апи
       :param host: адрес откуда собираем запросы
    """
    result = []
    endpoint = '%s/promotion/vocabulary/api/' % host
    params = {
        'by': 1,
        'page': 1,
        'only_fields': 'name',
    }
    try:
        resp = requests.get(endpoint, params=params, timeout=5).json()
    except Exception:
        logger.exception('Не удалось получить запросы с %s' % endpoint)
        return result
    by = 500
    total_records = resp.get('total_records', 0)
    total_pages = total_records / by + 1
    for i in range(int(total_pages)):
        params['by'] = by
        params['page'] = i + 1
        try:
            resp = requests.get(endpoint, params=params, timeout=5).json()
            result += [item['name'] for item in resp.get('data', []) if 'name' in item]
        except Exception:
            logger.exception('Не удалось получить запросы с %s, %s' % (endpoint, params))
    return result

def get_search_queries(root_dir: str = '/home/jocker/selenium',
                       profile_dir: str = '',
                       with_update: bool = False):
    """Получение списка поисковых запросов из файла json_queries
       или аналогичного файла в профиле
       :param root_dir: директория с ботом
       :param profile_dir: директория с профилем
       :param with_update: обновление запросов новыми
    """
    q_arr = []

    # --------------------------
    # Запросы считываем из файла
    # --------------------------
    json_queries_file = os.path.join(root_dir, 'json_queries.json')
    # --------------------------
    # Если у профиля свой список
    # запросов - используем его
    # --------------------------
    json_queries_file_profile = os.path.join(profile_dir, 'json_queries.json')
    if os.path.exists(json_queries_file_profile):
        json_queries_file = json_queries_file_profile

    with open(json_queries_file, 'r', encoding='utf-8') as f:
        queries = json.loads(f.read())
        if with_update and not profile_dir: # в профиле не обновляемся
            queries += update_search_queries()
        q_arr = [item.replace('"', '').replace('\'', '').replace(',', ' ').replace('(', '').replace(')', '').replace('.', ' ').replace('  ', ' ').replace('\t', '').strip()
                 for item in queries if item]
        q_arr = list(set(q_arr))

    with open(json_queries_file, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(q_arr, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False))
    return q_arr


if __name__ == '__main__':
    JSON_QUERIES_PATH = '/home/jocker/selenium/json_queries.json'
    #q_arr = get_search_queries()
    #print(json.dumps(q_arr, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False))
    queries = update_search_queries(host='http://spam.223-223.ru')
    with open(JSON_QUERIES_PATH, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(queries, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False))
    #print(len(queries))
    #get_search_queries(with_update = True)
