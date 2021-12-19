#-*- coding:utf-8 -*-
import re
import os
import time
import json
import logging
import datetime
import requests
import curlify
import xml.sax
import xlsxwriter
import sys
import traceback

import threading
import queue

from lxml import html as lxml_html

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.telegram.telegram import TelegramBot

from apps.main_functions.fortasks import search_process
from apps.main_functions.string_parser import kill_html, kill_quotes
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import (
    ListDir,
    check_path,
    open_file,
    make_folder,
    full_path,
)

logger = logging.getLogger(__name__)

all_settings = settings.FULL_SETTINGS_SET

TG_TOKEN = all_settings['RUPOOL_TG_TOKEN']
TG_CHAT = all_settings['RUPOOL_TG_CHAT']
telega = TelegramBot(token=TG_TOKEN, chat_id=TG_CHAT)

DOMAIN = all_settings['RUPOOL_DOMAIN']

DIR = 'rupool'
if check_path(DIR):
    make_folder(DIR)

default_headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Referer': DOMAIN,
    'TE': 'trailers',
    'Accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en,ru-RU;q=0.8,ru;q=0.5,en-US;q=0.3',
    'Cache-Control': 'no-cache',
    'Host': 'www.rupool.ru',
    'Origin': 'https://www.rupool.ru',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
}

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--get_cats',
            action = 'store_true',
            dest = 'get_cats',
            default = False,
            help = 'Get categories')
        parser.add_argument('--get_products',
            action = 'store_true',
            dest = 'get_products',
            default = False,
            help = 'Get products')
        parser.add_argument('--get_stocks',
            action = 'store_true',
            dest = 'get_stocks',
            default = False,
            help = 'Get stocks')
        parser.add_argument('--report',
            action = 'store_true',
            dest = 'report',
            default = False,
            help = 'Generate excel report')
        parser.add_argument('--images',
            action = 'store_true',
            dest = 'images',
            default = False,
            help = 'Receive product images')
        parser.add_argument('--full',
            action = 'store_true',
            dest = 'full',
            default = False,
            help = 'All operations')

    def handle(self, *args, **options):
        is_running = search_process(q = ('rupool_report', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            #exit()

        telega.send_message('hi')

        if options.get('get_products') or options.get('full'):
            get_products_operation(True)

        if options.get('get_cats') or options.get('full'):
            get_cats_operation()

        if options.get('get_stocks') or options.get('full'):
            get_stocks_operation()

        if options.get('report') or options.get('full'):
            make_report()

        if options.get('images'):
            folder = os.path.join(DIR, 'images')
            if check_path(folder):
                make_folder(folder)
            for i in range(1, 10):
                subfolder = os.path.join(folder, str(i))
                if check_path(subfolder):
                    make_folder(subfolder)
            get_images_operation(folder)

def get_images_operation(folder: str):
    """Обертка для получения изображений на товары
       :param folder: папка для картинок
    """
    sitemap = get_sitemap()
    #print(json_pretty_print(sitemap))
    s = auth()
    for item in sitemap:
        if not 'sitemap_goods' in item:
            continue
        urlset = get_urlset(item)
        #print(json_pretty_print(urlset))
        print(item)
        get_images(urlset, folder, session=s)

def get_images(links: list, folder: str, session: requests.Session):
    """Получаем все изображения товаров по ссылкам из карты сайта
       :param links: ссылки из карты сайта на товары
       :param folder: папка для картинок
       :param session: авторизация
    """
    pr = ParallelRequestsForImages(
        session = session,
        folder = folder,
    )
    pr.tasker(links)

class ParallelRequestsForImages:
    def __init__(self,
                 session: requests.Session,
                 folder: str):
        """Инициализация
           :param session: сессия requests.Session для авторизованных запросов
           :param folder: папка для изображений
        """
        # https://hg.python.org/cpython/file/3.5/Lib/queue.py
        self.q = queue.Queue(maxsize = 40)
        # Функция подготовки ссылок
        self.session = session
        self.folder = folder
        self.finished = False

    def get_image(self, product_id: int):
        """Получить изображения для товара
           Только для авторизованных
           Картинка без вотермарки:
           Скачать оригинал
               view-source:https://www.rupool.ru/good/374383?dowmloadnum=1
               downloadnum=2 - номер картинки
           <a href="/good/374383?dowmloadnum=1" class="download_origin">скачать оригинал</a>
           :param product_id: ид товара
        """
        subfolder = os.path.join(self.folder, str(product_id)[0])
        for i in range(10):
            params = {
                'dowmloadnum': i + 1,
            }
            r = self.session.get('%s/good/%s' % (DOMAIN, product_id), params=params)

            content_type = r.headers['content-type']
            if r.status_code != 200:
                print('[ERROR]: %s status_code %s' % product_id, r.status_code)
                continue
            if 'html' in content_type:
                break

            if r.status_code == 200 and 'image/' in content_type:
                d = r.headers['content-disposition']
                fname = re.findall('filename=(.+)', d)[0]
                dest = os.path.join(subfolder, fname)
                with open_file(dest, 'wb+') as f:
                    f.write(r.content)

    def do_work(self):
        while True:
            try:
                url = self.q.get()
                r = self.get_url(url)
                self.q.task_done()
            except Exception as e:
                print(e)
                traceback.print_exc(file=sys.stdout)
                return

            if self.finished:
                return
            if self.q.unfinished_tasks == 0:
                self.finished = True
                return

    def get_url(self, url):
        """Запрос
           :param url: ссылка
        """
        print(self.links.index(url), '/', len(self.links))

        product_id = int(url.split('/good/')[-1])
        self.get_image(product_id)

    def tasker(self, links):
        """Постановка задач в очередь
           :param links: ссылки для запросов
        """
        for i in range(self.q.maxsize):
            t = threading.Thread(target=self.do_work)
            t.daemon = True
            t.start()

        print('--- threading count %s ---' % threading.active_count())
        self.links = links

        for url in self.links:
            self.q.put(url)
        self.q.join()
        self.finished = True
        print('all done')


def make_report():
    """Сформировать отчет и заслать в телегу"""
    dirs = ListDir(DIR)
    pages = []
    for item in dirs:
        if item.startswith('products') and item.endswith('.json'):
            key = item.split('products')[-1].split('.')[0]
            src = os.path.join(DIR, 'cats.json')
            with open_file(src, 'r', encoding='utf-8') as f:
                cats = json.loads(f.read())
            src = os.path.join(DIR, 'stocks%s.json' % key)
            with open_file(src, 'r', encoding='utf-8') as f:
                stocks = json.loads(f.read())
            src = os.path.join(DIR, item)
            with open_file(src, 'r', encoding='utf-8') as f:
                products = json.loads(f.read())
            pages.append({
                'products': products,
                'stocks': {
                    int(item['id']): item['stock'] for item in stocks
                },
                'cats': {
                    item['id']: item['name'] for item in cats
                },
            })
    create_xlsx(pages)

def get_products_operation(with_auth: bool = False):
    """Обертка для получения категорий"""
    sitemap = get_sitemap()
    #print(json_pretty_print(sitemap))
    for item in sitemap:
        if not 'sitemap_goods' in item:
            continue
        urlset = get_urlset(item)
        #print(json_pretty_print(urlset))
        print(item)
        s = None
        prefix = ''
        if with_auth:
            s = auth()
        if 'sitemap_goods1' in item:
            prefix += '1'
        elif 'sitemap_goods2' in item:
            prefix += '2'
        get_products(urlset, prefix, session=s)

def get_cats_operation():
    """Обертка для получения категорий"""
    sitemap = get_sitemap()
    for item in sitemap:
        if not item.endswith('sitemap_cats.xml'):
            continue
        urlset = get_urlset(item)
        get_rubrics(urlset)

def get_stocks_operation():
    """Обертка для получения остатков"""
    prefix = ''
    sitemap = get_sitemap()
    for item in sitemap:
        if not 'sitemap_goods' in item:
            continue
        urlset = get_urlset(item)
        if 'sitemap_goods1' in item:
            prefix = '1'
        elif 'sitemap_goods2' in item:
            prefix = '2'
        get_stocks(urlset, prefix)

def create_xlsx(pages):
    titles = (
        ('Код товара', 'product_code'),
        ('Наименование', 'product_name'),
        ('Наличие', 'stocks'),
        ('Цена розница', 'price'),
        ('Цена закупочная', 'opt_price'),
        ('% скидки', 'discount'),
        ('Раздел', 'cat'),
    )
    dest = os.path.join(DIR, 'report.xlsx')
    book = xlsxwriter.Workbook(full_path(dest))

    total_products = 0
    for i, page in enumerate(pages):
        sheet = book.add_worksheet('Лист %s' % (i + 1))
        row_number = 0

        for i, title in enumerate(titles):
            sheet.write(row_number, i, title[0])
            sheet.write(row_number + 1, i, title[1])
        row_number += 1

        stocks = page['stocks']
        cats = page['cats']

        total_products += len(page['products'])
        for product in page['products']:
            sheet.write(row_number, 0, product['id'])
            sheet.write(row_number, 1, product['name'])

            product_price = product.get('price')
            discount = product.get('discount')

            sheet.write(row_number, 2, stocks.get(product['id']))
            sheet.write(row_number, 3, product_price)

            if product_price and discount:
                product_price = int(kill_quotes(product_price, 'int'))
                discount = int(kill_quotes(discount, 'int'))
                opt_price = product_price - (product_price / 100 * discount)
                sheet.write(row_number, 4, opt_price)
            sheet.write(row_number, 5, discount)
            sheet.write(row_number, 6, cats.get(product.get('cat')))
            row_number += 1
    book.close()

    now = datetime.datetime.today()

    with open_file(dest, 'rb') as f:
        caption = 'rupool.ru %s. Товаров: %s' % (now.strftime('%Y-%m-%d'), total_products)
        telega.send_document(f, caption=caption)

def safe_request(method, url, params = None, data = None, json_obj = None, headers=None, cookies=None):
    """Запрос с повторениями на случай ошибки сети
       :param method: requests.get / requests.post
       :param url: ссылка
       :param params: параметры в query
       :param data: параметры в форме
       :param json_obj: json в теле
    """
    if not headers:
        headers = default_headers
    for i in range(10):
        try:
            r = method(url=url, params=params, data=data, json=json_obj, headers=headers, cookies=cookies)
            if r.status_code == 200:
                return r
        except Exception as err:
            print('error, try', i, ':', err)

def to_string(el):
    """Получение элемента текстом
       :param el: элемент
    """
    return lxml_html.tostring(el)

def auth():
    """Авторизация на https://www.rupool.ru/enter/
       6493289 / XL440G
       :param s: сессия
    """
    s = requests.Session()
    s.headers.update(default_headers)
    r = s.get('%s/enter/' % DOMAIN)
    cookies = {
        'ab': 'main',
        'cookie[jcid]': '0',
        #'cookie[city]': '29',
    }
    tree = lxml_html.fromstring(r.text)
    auth_form = tree.xpath('//form[@id="frm_login"]')[0]
    login_input = auth_form.xpath('.//input[@name="login"]')[0]
    passwd_input = auth_form.xpath('.//input[@name="passw"]')[0]
    submit_button = auth_form.xpath('.//input[@name="submit"]')[0]
    action = auth_form.get('action')
    s.headers.update({
        'Referer': '%s/enter/' % DOMAIN,
    })
    r = s.post('%s%s' % (DOMAIN, action), data={
        'item': '',
        'login': all_settings['RUPOOL_LOGIN'],
        'passw': all_settings['RUPOLL_PASSWD'],
        'submit': submit_button.attrib.get('value'),
    }, cookies=cookies)
    #print(r.text)
    #print(curlify.to_curl(r.request))
    return s

def get_sitemap():
    """Получить карту сайта"""
    dest = os.path.join(DIR, 'sitemap.json')
    if not check_path(dest):
        with open_file(dest, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    r = requests.get('https://www.rupool.ru/sitemap.xml')
    result = []
    handler = SiteMapParser(result)
    xml.sax.parseString(r.text, handler)
    if not handler.result:
        print('[ERROR]: sitemap empty')
        return
    with open_file(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(handler.result))
    return handler.result

def get_urlset(sitemap_url: str):
    """Получить карту сайта, ссылки"""
    sitemap_name = os.path.split(sitemap_url)[-1].replace('.xml', '.json')
    dest = os.path.join(DIR, sitemap_name)
    if not check_path(dest):
        with open_file(dest, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    r = requests.get(sitemap_url)
    result = []
    handler = SiteMapParser(result)
    xml.sax.parseString(r.text, handler)
    if not handler.result:
        print('[ERROR]: %s empty' % sitemap_name)
        return

    with open_file(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(handler.result))
    return handler.result

def get_breadcrumbs(page_in_bottom, is_ppage: bool = False):
    """Найти хлебные крошки
       :param page_in_bottom: элемент с хлебными крошками
       :param is_ppage: страничка товара
    """
    parents = []
    lis = page_in_bottom.xpath('.//ol[@class="breadcrumb"]/li')
    if is_ppage:
        lis = page_in_bottom.xpath('.//ol/li')
    if not lis: # корень
        return parents
    for li in lis:
        alinks = li.xpath('.//a')
        for alink in alinks:
            parent_id = int(alink.attrib.get('href').split('/')[-1])
            if is_ppage:
                parents.append(parent_id)
            else:
                parent_name = alink.xpath('.//span')[0].text.strip()
                parents.append({
                    'id': parent_id,
                    'name': parent_name,
                })
    return parents

def get_rubrics(links):
    """Получаем все рубрики по ссылкам из карты сайта
       :param links: ссылки из карты сайта на категории
    """
    dest = os.path.join(DIR, 'cats.json')

    if not check_path(dest):
        with open_file(dest, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
            pass

    def prepare_cat_links(links: list):
        """Функция для подготовки ссылок на рубрики
           :param links: ссылки
        """
        new_links = []
        for i, link in enumerate(links):
           if '/catalog/' in link:
                new_links.append(link)
        return new_links

    def analyze_cat(r):
        """Анализ ответа по страничке категории
           :param r: requests.get / requests.post
        """
        cat_id = int(r.request.url.split('/')[-1])
        cat = {
            'id': cat_id,
            'parents': [],
        }
        tree = lxml_html.fromstring(r.text)
        page_in_bottom = tree.xpath('.//div[@id="page_in_bottom"]')[0]

        h1 = page_in_bottom.xpath('.//h1')
        if not h1:
            print('[ERROR]: h1 not found for %s' % cat_id)
            return

        h1 = h1[0]
        cat_name = h1.text.strip()
        cat['name'] = cat_name

        cat['parents'] = get_breadcrumbs(page_in_bottom)

        return cat

    pr = ParallelRequests(
        prepare_function = prepare_cat_links,
        accum_function = analyze_cat,
    )
    pr.tasker(links)
    cats = pr.accum_result
    print(json_pretty_print(cats))

    with open_file(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(cats))
    return cats

def prepare_product_links(links: list):
    """Функция для подготовки ссылок на товары
       :param links: ссылки
    """
    new_links = []
    links_len = len(links)
    for i, link in enumerate(links):
        if '/good/' in link:
            new_links.append(link)
    return new_links

def get_stocks(links, prefix=''):
    """Получаем все остатки по ссылкам на товары, взятых из карты сайта
       STOCK - POST
       https://www.rupool.ru/lib/JsHttpRequest/this.php?action=after_cache&item=store_info
           goods[]=si434067
           goods[]=si286120
           item=store_info
           func_before=StoreInfoAfter
           by_ps_alt=1
       :param links: ссылки из карты сайта на товары
       :param prefix: номер файла из карты сайта
    """
    dest = os.path.join(DIR, 'stocks%s.json' % prefix)

    """Однопоточный метод"""
    if not check_path(dest):
        with open_file(dest, 'r', encoding='utf-8') as f:
            #return json.loads(f.read())
            pass

    endpoint = '/lib/JsHttpRequest/this.php'
    params = {
        'action': 'after_cache',
        'item': 'store_info',
    }
    stocks = []
    products = []
    links_len = len(links)
    for i, link in enumerate(links):

        if '/good/' in link:
            product_id = int(link.split('/')[-1])
            products.append(product_id)

    containers = []
    goods = []
    by = 500
    for i, product in enumerate(products):
        if i % by == 0 and i > 0:
            containers.append(goods)
            goods = []
        goods.append(product)
    containers.append(goods)

    for i, container in enumerate(containers):
        print('stocks', i, '/', len(containers))
        url = '%s%s' % (DOMAIN, endpoint)
        data = {
           'item': 'store_info',
           'func_before': 'StoreInfoAfter',
           'by_ps_alt': 1,
        }
        data['goods[]'] = ['si%s' % good for good in container]
        r = safe_request(requests.post, url=url, params=params, data=data)
        result = r.json()
        for key, value in result['arr'].items():
            stocks.append({
                'id': key.replace('si', '').strip(),
                'stock': kill_html(value),
            })
    print('[STOCKS]: products %s / stocks %s' % (len(products), len(stocks)))
    with open_file(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(stocks))
    return stocks


def get_products(links, prefix='', session = None):
    """Получаем все товары по ссылкам из карты сайта
       :param links: ссылки из карты сайта на товары
       :param prefix: номер файла из карты сайта
    """
    dest = os.path.join(DIR, 'products%s.json' % prefix)
    def analyze_product(r):
        """Анализ ответа по страничке товара
           :param r: requests.get / requests.post
        """
        product_id = int(r.request.url.split('/')[-1])
        product = {
            'id': product_id,
        }
        tree = lxml_html.fromstring(r.text)
        page_in_bottom = tree.xpath('.//div[@id="page_in_bottom"]')[0]

        h1 = page_in_bottom.xpath('.//h1')[0]
        product_name = h1.text.strip()
        product['name'] = product_name
        breadcrumbs = get_breadcrumbs(page_in_bottom, is_ppage=True)
        if breadcrumbs:
            product['cat'] = breadcrumbs[-1]

        price_block = page_in_bottom.xpath('.//span[@id="pricech%s"]' % product_id)
        if price_block:
            price = price_block[0].xpath('.//span[@class="price_view"]')
            if price and price[0].text:
                product['price'] = price[0].text.replace('руб.', '').strip()
        #print(product)

        # Ищем скидку
        goods = page_in_bottom.xpath('.//div[@class="good"]')
        for good in goods:
            if good.attrib.get('itemtype') == 'http://schema.org/Product':
                for div in good:
                    discount_str = 'Код %s - ' % product_id
                    if div.text and discount_str in div.text:
                        discount = div.text.split(discount_str)[-1]
                        product['discount'] = discount
        return product


    products = []

    pr = ParallelRequests(
        prepare_function = prepare_product_links,
        accum_function = analyze_product,
        session = session,
    )
    pr.tasker(links)
    products = pr.accum_result
    with open_file(dest, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(products))
    return products

class ParallelRequests:
    def __init__(self,
                 accum_function = None,
                 prepare_function = None,
                 partial_save = None,
                 session = None):
        """Инициализация
           :param accum_function: функция для обработки результата
           :param prepare_function: функция подготовки ссылок до постановки в очередь
                                    должна возвращать новые ссылки
           :param partial_save: функция частичного сохранения результатов
           :param session: сессия requests.Session для авторизованных запросов
        """
        # https://hg.python.org/cpython/file/3.5/Lib/queue.py
        self.q = queue.Queue(maxsize = 40)
        self.accum_result = [] # Куда ложим результаты
        # Функция обработки результата (в accum_result)
        self.accum_function = accum_function
        # Функция подготовки ссылок
        self.prepare_function = prepare_function
        self.links = []
        self.headers = default_headers
        self.partial_save = partial_save
        self.session = session
        self.finished = False

    def do_work(self):
        while True:
            try:
                url = self.q.get()
                r = self.get_url(url)
                result = self.analyze_result(r)
                self.q.task_done()
            except Exception as e:
                print(e)
                traceback.print_exc(file=sys.stdout)
                return

            if self.finished:
                return
            if self.q.unfinished_tasks == 0:
                self.finished = True
                return

    def get_url(self, url):
        """Запрос
           :param url: ссылка
        """
        if self.session:
            for i in range(5):
                try:
                    r = self.session.get(url=url)
                    if r.status_code == 200:
                        return r
                except Exception as err:
                    print('error, try', i, ':', err)
            return

        r = safe_request(requests.get, url, headers=self.headers)
        return r

    def analyze_result(self, r):
        """Обработка результатов запроса
           :param r: результат запроса requests.get / requests.post
        """
        print(r.request.url, '=>',
              r.status_code,
              '(', self.links.index(r.request.url), '/', len(self.links), ')'
        )
        if self.accum_function:
            row = self.accum_function(r)
            if row:
                self.accum_result.append(row)
            if self.partial_save:
                self.partial_save(self.accum_result)
            return row

    def tasker(self, links):
        """Постановка задач в очередь
           :param links: ссылки для запросов
        """
        for i in range(self.q.maxsize):
            t = threading.Thread(target=self.do_work)
            t.daemon = True
            t.start()

        print('--- threading count %s ---' % threading.active_count())
        if self.prepare_function:
            links = self.prepare_function(links)
        self.links = links

        for url in self.links:
            self.q.put(url)
        self.q.join()
        self.finished = True
        print('all done')

class SiteMapParser(xml.sax.ContentHandler):
    """Парсер карты сайта
       sitemap_firms.xml
       sitemap_cats.xml
       sitemap_goods.xml
       sitemap_artiles.xml
       sitemap_goods1.xml
    """
    def __init__(self, result):
        """Передаем result для аккумуляции результата
           :param result: аккумуляция результата
        """
        self.result = result
        self.cur_loc = {}

        self.loc_name = 'loc'
        self.in_loc_name = False # <loc>
        self.loc_value = ''

    def startElement(self, name, attributes):
        if not self.in_loc_name and name == self.loc_name:
            self.in_loc_name = True

    def characters(self, content):
        if self.in_loc_name:
            self.loc_value += content

    def endElement(self, name):
        if self.in_loc_name and name == self.loc_name:
            self.in_loc_name = False
            self.result.append(self.loc_value)
            self.loc_value = ''

