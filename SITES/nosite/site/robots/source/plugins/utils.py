# -*- coding:utf-8 -*-
import os
import psutil
import shutil
import json
import requests
import socket
import random
import logging

from envparse import env
env.read_envfile()
API_SERVER = env('API_SERVER')
API_TOKEN = env('API_TOKEN')

logger = logging.getLogger(__file__)

def ListDir(path):
    """Список папок и файлов
       :param path: путь
    """
    dirs = []
    try:
        dirs = os.listdir(path)
    except OSError:
        pass
    return dirs

def isForD(path):
    """Проверка пути - файл это или папка
       :param path: путь
    """
    if os.path.isdir(path):
        return 'dir'
    if os.path.isfile(path):
        return 'file'
    return None

def get_hd_space(dev: str = '/'):
    """Получить информацию по месту на диске в МБ
       :param dev: точка монтирования
    """
    space = psutil.disk_usage('/')
    return {
        'free': space.free / 1024 / 1024,
        'used': space.used / 1024 / 1024,
        'total': space.total / 1024 / 1024,
        'percent': space.percent,
    }

def hd_clear_space():
    """Подчистить место в случае необходимости"""
    space = get_hd_space()
    if space['used'] <= 90:
        return
    folders = (
        '/var/cache',
        '/var/log/journal',
        '/root/*',

    )
    for folder in folders:
        if folder.endswith('*'):
            main_folder = folder[:-1]
            for item in ListDir(main_folder):
                if main_folder == '/root/' and item.startswith('.'):
                    continue
                path = os.path.join(main_folder, item)
                if isForD(path) == 'file':
                    os.unlink(path)
        else:
            if os.path.exists(folder):
                shutil.rmtree(folder)

    tmp_folder = '/tmp'
    for item in ListDir(tmp_folder):
        bad_path = os.path.join(tmp_folder, item)
        if item.endswith('.dmp') and isForD(bad_path) == 'file':
            try:
                os.unlink(bad_path)
            except Exception as e:
                logger.error('[ERROR]: tmp file drop failed %s' % item)

        elif item.startswith('.com.google.Chrome.'):
            try:
                shutil.rmtree(bad_path)
            except Exception as e:
                logger.error('[ERROR]: tmp dir drop failed %s' % item)

def search_process(q: list):
    """Ищем процесс
       :param q: список строк для поиска
    """
    if not isinstance(q, list) and not isinstance(q, tuple):
        assert False
    mypid = os.getpid()
    myppid = os.getppid()
    for obj in psutil.process_iter():
        process = obj.as_dict(attrs=['pid', 'cmdline', 'create_time', ])
        if not process['cmdline']:
            continue
        if process['pid'] == mypid or process['pid'] == myppid:
            continue
        match = True
        for item in q:
            in_cmd = list(filter(lambda x: item in x, process['cmdline']))
            #print(in_cmd)
            if not in_cmd:
                match = False
                break
        if match:
            return process
    return None

def punto(text: str, direction: str = 'eng2rus'):
    """Перевод английской раскладки в русские буквы,
       например, для ввода паролей по логину
       :param text: текст для изменения
       :param direction: тип для изменения
    """
    if not text:
        return text
    text = '%s' % text
    eng = ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',
           'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '\\',
           'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/')
    rus = ('й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ',
           'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'ё',
           'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '/')
    def get_letter(letter: str):
        """Возвращаем букву после преобразований
           :param letter: буква до преобразований
        """
        if direction == 'eng2rus':
            source = eng
            dest = rus
        elif direction == 'rus2eng':
            source = rus
            dest = eng
        ind = None
        if letter in source:
            ind = source.index(letter)
            return dest[ind]
        return letter

    result = ''
    for letter in text:
        result += get_letter(letter)
    return result

def driver_versions(driver):
    """Версии браузера и драйвера
       если они отличаются, значит, надо обновляться
       :param driver: экземпляр selenium.webdriver
    """
    result = {}
    if 'browserVersion' in driver.capabilities:
        result['selenium'] = driver.capabilities['browserVersion']
    if 'chrome' in driver.capabilities and 'chromedriverVersion' in driver.capabilities['chrome']:
        result['chrome'] = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    return result

def inform_server(browser):
    """Информируем сервер о роботе
       :param browser: экземпляр browser
    """
    if not API_SERVER or not API_TOKEN:
        logger.info('API_SERVER / API_TOKEN not set')
        return
    driver = browser.driver
    headers = {'token': API_TOKEN}
    params = {
        'versions': driver_versions(driver),
        'hostname': socket.gethostname(),
        'free_space': get_hd_space(),
    }
    endpoint = '%s/robots/inform_server/' % API_SERVER.rstrip('/')

    yandex_login, yandex_passwd = browser.yandex.load_credentials()
    profile_params = {
        'name': browser.profile_name,
        'user_agent': browser.user_agent,
        'resolution': browser.screen,
        'yandex_login': yandex_login,
        'yandex_passwd': yandex_passwd,
    }
    params['profile'] = profile_params
    try:
        r = requests.get(endpoint, json=params, headers=headers)
        print('[INFORM_SERVER]: %s => %s' % (r.status_code, r.text))
        if not r.status_code == 200:
            print(r.text)
    except Exception as e:
        logger.info('[ERROR]: %s' % e)


def fill_starts_counter(cur_dir: str):
    """Инкрементальный номер запуска,
       получаем из файла и инкрементируем
       :param cur_dir: корневая директория
    """
    total_starts_counter = 0
    counter_file = os.path.join(cur_dir, 'starts_counter.txt')
    if os.path.exists(counter_file):
        with open(counter_file, 'r', encoding='utf-8') as f:
            start_counter = json.loads(f.read())
            total_starts_counter = start_counter['starts_counter']
    with open(counter_file, 'w+', encoding='utf-8') as f:
        f.write(json.dumps({
            'starts_counter': total_starts_counter + 1,
        }))
    return total_starts_counter


def simpler(digit, total):
    """Упрощаем число, получаем неделимое на total
       Например, хотим запускать последовательно профили,
       тогда нужно ввести счетчик, который будет инкрементироваться
       берем его и количество профилей и выясняем какой на очереди
       :param digit число - номер запуска
       :param total число - всего профилей
    """
    if total <= 0:
        return digit
    while digit >= total:
        digit -= total
    return digit


def check_connection_over_proxy(proxy: str,
                                probability: int = 50,
                                test_url: str = 'https://223-223.ru'):
    """Проверка соединения через проксик
       если проверка проходит, то с вероятностью probability
       используем проксик
       :param proxy: проксик, например,
                     http://10.10.9.1:3128
       :param probability: монетка для рандома
       :param test_url: адрес сайта,
                        соединение к которому проверяем
                        через проксик
    """
    proxies = {
        'http'  : proxy,
        'https' : proxy,
    }
    try:
        r = requests.get(test_url, proxies=proxies, timeout=5)
        if r.status_code == 200:
            chance = random.randint(0, 100)
            if chance <= probability:
                return True
    except Exception as e:
        logger.info('[proxy]: proxies not available %s' % (e, ))
    return False


def get_ip():
    """Получить ip адрес"""
    api_url = '%s/my_ip/' % API_SERVER.rstrip('/')
    ip = '0.0.0.0'
    try:
        r = requests.get(api_url, timeout=5)
        ip = r.json().get('ip')
    except Exception as e:
        logger.info(e)
    return ip

def get_hostname():
    """Получить имя хоста"""
    return socket.gethostname()

if __name__ == '__main__':
    logger.info('hd_clear_space')
    hd_clear_space()
