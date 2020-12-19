#-*- coding:utf-8 -*-
import time
import json
import logging
import datetime
import requests

from django.conf import settings
from django.db.models import Count

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import check_path, open_file
from apps.flatcontent.models import Containers, Blocks
from apps.products.models import (
    Products,
    ProductsPhotos,
    ProductsCats,
    Property,
    PropertiesValues,
    ProductsProperties,
)

from envparse import env
env.read_envfile()

logger = logging.getLogger(__name__)

LOGIN = env('SIMALAND_LOGIN')
PASSWD = env('SIMALAND_PASSWD')
PHONE = env('SIMALAND_PHONE')

class SimaLand:
    """https://www.sima-land.ru/info/shop/"""
    def __init__(self, login: str = None,
                 passwd: str = None,
                 phone: str = None, ):
        """Инициализация
           :param login: логин
           :param passwd: пароль
           :param phone: телефон
           Документация https://www.sima-land.ru/api/v5/help/ (нов)
                        https://www.sima-land.ru/api/v3/help/ (корзинка)
           После заливки овердохуя пустых рубрик, а также надо
           фиксануть ссылки и привязку к контейнеру командами:
           python manage.py search_empty_cats --drop_empty
           python manage.py update_catalogue_links
        """
        self.api_url = 'https://www.sima-land.ru/api/v5'
        self.api_url_v3 = 'https://www.sima-land.ru/api/v3'
        self.jwt_v3 = None
        self.s = requests.Session()
        self.login = login or LOGIN
        self.passwd = passwd or PASSWD
        self.phone = phone or PHONE
        self.units = {} # ед. измерения товаров

    def get_jwt(self):
        """Получение JWT токена"""
        params = {
            'email': self.login,
            'password': self.passwd,
            'phone': self.phone,
            'regulation': True,
        }
        r = self.s.post('%s/signin' % self.api_url, json=params)
        if r.status_code == 204:
            self.s.headers.update(r.headers)

    # api v3
    def get_jwt_v3(self):
        """Авторизация через версию апи 3"""
        if self.jwt_v3:
            return
        auth = requests.auth.HTTPBasicAuth(self.login, self.passwd)
        r = self.s.post('%s/auth' % self.api_url_v3, auth=auth)
        resp = r.json()
        self.s.headers.update({
            'Authorization': 'Bearer %s' % resp['jwt'],
        })
        self.jwt_v3 = resp['jwt']

    def get_categories(self):
        """Получить все категории
           В ответе есть level, по нему собираем уровень
           В ответе есть path, состоит из id
           для первого уровня он равен id, разделитель точка
        """
        all_cats = []
        params = {'p': 1}
        resp_count = 1
        while(resp_count > 0):
            r = self.s.get('%s/category' % self.api_url, params=params)
            if not r.status_code == 200:
                break
            resp = r.json()
            resp_count = len(resp)
            params['p'] += 1
            all_cats += resp
        # Создаем каталог
        container = Containers.objects.filter(state=7, tag='simaland').first()
        if not container:
            container = Containers.objects.create(
                state=7,
                tag='simaland',
                name='Каталог sima-land.ru'
            )
        level = 0
        parents = None
        logger.info('start filling catalogue simaland, total rubrics in simaland %s' % len(all_cats))
        while True:
            level += 1
            cats = [cat for cat in all_cats if cat['level'] == level]
            if not cats:
                break
            logger.info('gather %s level with %s rubrics' % (level, len(cats)))
            for cat in cats:
                if level > 1:
                    # path[-2] = parent, path[-1] - текущий ид
                    path = cat['path'].split('.')
                    parent = Blocks.objects.filter(
                        tag='simaland_%s' % path[-2],
                        container=container,
                    ).first()
                    if not parent:
                        logger.info('cat %s without parents' % cat)
                        continue
                    parents = parent.parents if parent.parents else ''
                    parents += '_%s' % parent.id
                analog = Blocks.objects.filter(
                    tag='simaland_%s' % cat['id'],
                    container=container,
                ).first()
                if not analog:
                    with_icon = '.' in cat['icon'][-5:]
                    analog = Blocks.objects.create(
                        state=4,
                        tag='simaland_%s' % cat['id'],
                        container=container,
                        img=cat['icon'] if with_icon else None,
                        name=cat['name'],
                        parents=parents,
                    )

    def get_unit(self, unit_id):
        """Получить единицу измерения
           :param unit_id: ид единицы измерения
        """
        r = self.s.get('%s/unit/%s' % (self.api_url, unit_id))
        if not r.status_code == 200:
            return
        resp = r.json()
        self.units[resp['id']] = resp['name']

    def get_units(self):
        """Получить все единицы измерения"""
        params = {'p': 1}
        resp_count = 1
        while(resp_count > 0):
            r = self.s.get('%s/unit' % self.api_url, params=params)
            if not r.status_code == 200:
                break
            resp = r.json()
            resp_count = len(resp)
            params['p'] += 1
            # Обрабытываем каждую пачку ед. измерения
            for unit in resp:
                self.units[unit['id']] = unit['name']

    def save_product(self, product):
        """Сохранение товара
           :param product: словарь с данными
        """
        # Без остатка (баланса) нам товары не нужны
        # Без категории нам товары не нужны
        # Без фоток нам товары не нужны
        photos = product.get('agg_photos')
        if product['balance'] == '0' or not product['category_id'] or not photos:
            return None
        analog = Products.objects.filter(code='simaland_%s' % product['id']).first()
        if not analog:
            analog = Products(code='simaland_%s' % product['id'])
        analog.info = product['description']
        analog.name = product['name']
        analog.price = product['price']
        analog.min_count = product['minimum_order_quantity']
        analog.multiplicity = product['qty_multiplier']
        if not product['unit_id'] in self.units:
            self.get_unit(product['unit_id'])
        analog.measure = self.units[product['unit_id']]
        analog.altname = product['sid']
        analog.img = '%s%s/700.jpg' % (product['base_photo_url'], photos[0])
        analog.save()
        # Фотки
        photos_analogs = analog.productsphotos_set.all().aggregate(Count('id'))['id__count']
        if not photos_analogs and len(photos) > 1:
            for i in photos[1:]:
                ProductsPhotos.objects.create(
                    product=analog,
                    img = '%s%s/700.jpg' % (product['base_photo_url'], i),
                )
        # Категория
        category_analog = analog.productscats_set.all().first()
        if not category_analog:
            cat_id = product['category_id']
            cat = Blocks.objects.filter(tag='simaland_%s' % cat_id, container__tag='simaland').only('id').first()
            if cat:
                ProductsCats.objects.create(
                    product=analog,
                    cat=cat,
                )
        return analog

    def get_product(self, product_id: int):
        """Получить товар по ид
        """
        r = self.s.get('%s/item/%s' % (self.api_url, product_id))
        self.get_units()
        resp = r.json()
        self.save_product(resp)
        return resp

    def get_products(self):
        """Получить все товары
           ссылка на товар по артикулу (sid)
        """
        self.get_units()
        params = {'p': 1}
        resp_count = 1
        while(resp_count > 0):
            r = self.s.get('%s/item' % self.api_url, params=params)
            if not r.status_code == 200:
                logger.info('status_code %s, response %s' % (r.status_code, r.text))
                # Не всегда надо заваливать процесс,
                # надо здесь учесть 500 ошибки
                break
            resp = r.json()
            resp_count = len(resp)
            params['p'] += 1
            # Обрабытываем каждую пачку товаров
            for product in resp:
                self.save_product(product)

    def get_props(self):
        """Получить свойства товаров"""
        params = {'p': 1}
        resp_count = 1
        while(resp_count > 0):
            r = self.s.get('%s/attribute' % self.api_url, params=params)
            if not r.status_code == 200:
                break
            resp = r.json()
            resp_count = len(resp)
            params['p'] += 1
            # Обрабытываем каждую пачку свойств
            for prop in resp:
                analog = Property.objects.filter(code='simaland_%s' % prop['id']).only('id').first()
                if not analog:
                    analog = Property.objects.create(
                        code='simaland_%s' % prop['id'],
                        name=prop['name'],
                    )

    def get_attrs(self):
        """Получить связи свойств с товарами"""
        pvalues = {}
        fname = 'simaland_pvalues.json'
        if not check_path(fname):
            f = open_file(fname)
            content = json.loads(f.read())
            pvalues = {int(k): v for k, v in content.items()}
            f.close()
        if not pvalues:
            logging.info('receiving values')
            params = {'p': 1}
            resp_count = 1
            while(resp_count > 0):
                r = self.s.get('%s/option' % self.api_url, params=params)
                if not r.status_code == 200:
                    break
                resp = r.json()
                resp_count = len(resp)
                params['p'] += 1
                for item in resp:
                    pvalues[item['id']] = item['name']
            f = open_file(fname, 'w+')
            f.write(json.dumps(pvalues))
            f.close()

        pvalues[0] = 'Да'
        lazy_props = {}

        logging.info('%s values received, receiving attrs' % len(pvalues))
        params = {'p': 1}
        resp_count = 1
        while(resp_count > 0):
            r = self.s.get('%s/item-attribute' % self.api_url, params=params)
            if not r.status_code == 200:
                break
            resp = r.json()
            resp_count = len(resp)
            params['p'] += 1
            # Обрабытываем каждую пачку свойств
            for item in resp:
                product_id = item['item_id']
                prop_id = item['attribute_id']
                option_value = item['option_value']
                if not option_value in pvalues:
                    #logging.info('%s not in pvalues' % item)
                    continue
                product = Products.objects.filter(code='simaland_%s' % product_id).only('id').first()
                if not product:
                    continue
                if prop_id in lazy_props:
                    prop = lazy_props[prop_id]
                else:
                    prop = Property.objects.filter(code='simaland_%s' % prop_id).only('id').first()
                    lazy_props[prop_id] = prop
                if not prop:
                    logger.info('prop not found %s' % item)
                    continue

                analog = PropertiesValues.objects.filter(
                    prop=prop,
                    str_value=pvalues[option_value],
                ).only('id').first()
                if not analog:
                    analog = PropertiesValues.objects.create(
                        prop=prop,
                        str_value=pvalues[option_value],
                    )
                pvalue = ProductsProperties.objects.filter(
                    product=product,
                    prop=analog,
                ).only('id').first()
                if not pvalue:
                    pvalue = ProductsProperties.objects.create(
                        product=product,
                        prop=analog,
                    )

    # api v3
    def get_cart(self):
        """Получение корзинки"""
        self.get_jwt_v3()
        endpoint = '/cart-item/'
        r = self.s.get('%s%s' % (self.api_url_v3, endpoint))
        return r.json()

    # api v3
    def clear_cart(self, product_id: int):
        """Очистка корзинки по одному товару
           :param product_id: id товара
        """
        self.get_jwt_v3()
        endpoint = '/cart-item/%s/' % product_id
        r = self.s.delete('%s%s' % (self.api_url_v3, endpoint))
        if r.status_code == 204:
            return True
        return False

    # api v3
    def add2cart(self, cart_id: int, items: list):
        """Добавление товаров в корзинку
           :param cart_id: id корзинки
           :param items: список товаров [{'item_id': 1, 'qty': 1}, ]
        """
        self.get_jwt_v3()
        endpoint = '/cart/%s/' % cart_id
        params = {
            'items': items,
        }
        r = self.s.put('%s%s' % (self.api_url_v3, endpoint), json=params)
        return r.json()

    # DEPRICATED
    def raw_auth(self):
        """Авторизация запросами - НЕ ИСПОЛЬЗУЕТСЯ"""
        s = requests.Session()
        auth_url = 'https://www.sima-land.ru/auth/'
        r = s.get(auth_url)
        content = html.fromstring(r.text)

        login_form = content.xpath('//form[@id="login-form"]')
        if not login_form:
            assert False
        login_form = login_form[0]

        csrf = login_form.xpath('.//input[@name="_csrf"]')
        if not csrf:
            assert False
        csrf = csrf[0].attrib.get('value')

        auth_url = 'https://www.sima-land.ru/api/v3/login-form/'
        headers = {'X-CSRF-Token': csrf}
        auth = {
            'entity': self.login,
            'password': self.passwd,
            'type': 'email',
        }
        r = s.post(auth_url, json=auth, headers=headers)
        print(r.text)


        signup_url = 'https://www.sima-land.ru/signup/?sort=rating'
        auth = {
            '_csrf': [
                csrf, csrf,
            ],
            'LoginForm[entity]': self.login,
            'LoginForm[password]': self.passwd,
        }
        r = s.post(signup_url, data=auth)
        print(r.text)

