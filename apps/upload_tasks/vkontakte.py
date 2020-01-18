#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import check_path, open_file

from envparse import env
env.read_envfile()

logger = logging.getLogger(__name__)

#LOGIN = env('LOGIN')
#PASSWD = env('PASSWD')

#APP_ID = env('APP_ID')
#SECURE_KEY = env('SECURE_KEY')
#SERVICE_KEY = env('SERVICE_KEY')

TOKEN = env('TOKEN')

class VK:
    def __init__(self, token=None, group_id=None):
        """Инициализация
           :param token: access_token
           :param group_id: идентификатор сообщества
           Документация по товарам https://vk.com/dev/goods_docs

           1) Получаем доступ приложением
              https://oauth.vk.com/authorize?client_id=7271884&display=page&redirect_uri=http://vallom.ru&scope=groups,market,photos,offline&response_type=code&v=5.103
           2) Получаем токен для запросов
              https://oauth.vk.com/access_token?client_id=7271884&client_secret={SECURE_KEY}&redirect_uri=http://vallom.ru&code=db32ef65088c1ef20c
        """
        self.API_URL = 'https://api.vk.com/method/'
        self.s = requests.Session()
        self.TOKEN = token or TOKEN
        self.group_id = group_id

    def required_params(self, params):
        """Добавляем обязательные параметры для всех запросов"""
        params['access_token'] = self.TOKEN
        params['v'] = '5.103'

    def get_categories(self):
        """Получаем список категорий для товаров"""
        fname = 'vkontakte_getCategories.txt'
        if not check_path(fname):
            with open_file(fname, 'r') as f:
                content = json.loads(f.read())
            return content

        method = 'market.getCategories'
        params = {
            'count': 100,
            'offset': 0,
        }
        self.required_params(params)
        categories = []
        while True:
            r = self.s.get('%s%s' % (self.API_URL, method), params=params)
            content = r.json()
            items = content['response']['items']
            if not items:
                break
            categories += items
            params['offset'] += content['response']['count']
        with open_file(fname, 'wb+') as f:
            f.write(json.dumps(categories).encode('utf-8'))
        return categories

    def get_upload_img_url(self, is_main: bool = True):
        """Получение ссылки для загрузки фотографии
           :param is_main: обложка или дополнительная фотка если False"""
        method = 'photos.getMarketUploadServer'
        params = {
            'group_id': self.group_id,
            'main_photo': 1 if is_main else 0,
        }
        self.required_params(params)
        r = self.s.get('%s%s' % (self.API_URL, method), params=params)
        return r.json()['response']['upload_url']

    def upload_img(self, is_main, path):
        """Загрузка изображения на сервер"""
        upload_img_url = self.get_upload_img_url(is_main)
        files = {
            'file': open_file(path, 'rb')
        }
        r = self.s.post(upload_img_url, files=files)
        imga = r.json()
        if 'error' in imga:
            logger.error(imga)
            return None

        method = 'photos.saveMarketPhoto'
        params = {
            'group_id': self.group_id,
            'photo': imga['photo'],
            'server': imga['server'],
            'hash': imga['hash'],
            'crop_data': imga.get('crop_data', ''),
            'crop_hash': imga.get('crop_hash', ''),
         }
        self.required_params(params)
        r = self.s.get('%s%s' % (self.API_URL, method), params=params)
        return r.json()['response'] # Массив

    def drop_product(self, item_id: int):
        """Удаление товара
           :param item_id: Идентификатор товара
           :param owner_id: Идентификатор владельца товара"""
        method = 'market.delete'
        params = {
            'item_id': item_id,
            'owner_id': -self.group_id,
        }
        self.required_params(params)
        r = self.s.get('%s%s' % (self.API_URL, method), params=params)
        return r.json()['response']

    def get_products(self, count: int = 100, offset: int = 0):
        """Возвращает список товаров в сообществе
           :param count: кол-во возвращаемых товаров
           :param offset: смещение - с какой позиции запрашиваем"""
        method = 'market.get'
        params = {
            'owner_id': -self.group_id,
            'count': count,
            'offset': offset,
        }
        self.required_params(params)
        r = self.s.get('%s%s' % (self.API_URL, method), params=params)
        return r.json()['response']['items']

    def upload_extra_images(self, images: list = None):
        """Загрузка дополнительных фотографий для товара
           :param images: Список путей до картинок"""
        extra_images = []
        if images:
            for image in images:
                extra_imga = self.upload_img(False, image)
                if extra_imga:
                    extra_images.append(extra_imga[0]['id'])
        return extra_images


    def new_product(self, img: str, images: list = None,
                    category_id: int = 404, price: float = 0.1, old_price: float = 0.2,
                    product_name: str = '', product_description: str = '',
                    is_deleted: bool = False, url: str = ''):
        """Добавление нового товара
           :param path: путь для основного изображения товара
           :param images: список путей для дополнительных фоток товара
           :param category_id: категория для товара (get_categories метод)
           :param price: цена товара
           :param old_price: старая цена товара
           :param product_name: название товара
           :param product_description: описание товара
           :param is_deleted: флаг, что товар удален
           :param url: ссылка на сайт"""
        method = 'market.add'
        imga = self.upload_img(True, img)
        extra_images = self.upload_extra_images(images)

        params = {
            'owner_id': -self.group_id,
            'name': product_name,
            'description': product_description,
            'category_id': category_id,
            'price': price,
            'old_price': old_price,
            'deleted': 1 if is_deleted else 0,
            'main_photo_id': imga[0]['id'],
            'photo_ids': ','.join(['%s' % (im, ) for im in extra_images]),
            'url': url,
        }
        self.required_params(params)
        r = self.s.get('%s%s' % (self.API_URL, method), params=params)
        return r.json()['response']['market_item_id']

    def edit_product(self, item_id: int, img: str, images: list = None,
                    category_id: int = 404, price: float = 0.1, old_price: float = 0.2,
                    product_name: str = '', product_description: str = '',
                    is_deleted: bool = False, url: str = ''):
        """Редактирование товара
           :param item_id: идентификатор товара
           :param path: путь для основного изображения товара
           :param images: список путей для дополнительных фоток товара
           :param category_id: категория для товара (get_categories метод)
           :param price: цена товара
           :param old_price: старая цена товара
           :param product_name: название товара
           :param product_description: описание товара
           :param is_deleted: флаг, что товар удален
           :param url: ссылка на сайт"""
        method = 'market.edit'
        imga = self.upload_img(True, img)
        extra_images = self.upload_extra_images(images)

        params = {
            'item_id': item_id,
            'owner_id': -self.group_id,
            'name': product_name,
            'description': product_description,
            'category_id': category_id,
            'price': price,
            'old_price': old_price,
            'deleted': 1 if is_deleted else 0,
            'main_photo_id': imga[0]['id'],
            'photo_ids': ','.join(['%s' % (im, ) for im in extra_images]),
            'url': url,
        }
        self.required_params(params)
        r = self.s.get('%s%s' % (self.API_URL, method), params=params)
        return r.json()['response']
