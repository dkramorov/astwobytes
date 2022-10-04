#!/usr/env/env python3
import os
import json
import requests
import logging

from django.conf import settings
from envparse import env

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file

env.read_envfile(os.path.join(settings.BASE_DIR, 'conf', '.env'))

logger = logging.getLogger('simple')

class APIJDOCS():
    """Класс для работы с jdocs (получение лотов + автолотов)
    """
    login = env('API_JDOCS_USER')
    passwd = env('API_JDOCS_PASSWD')

    domain = 'https://users.jsmjapan.com/ru/site'
    lots_endpoint = '/get-user-records'
    autolots_endpoint = '/get-user-cars'

    default_params = {
        'key': passwd,
        'start_date': '2021-05-01',
        'end_date': '2021-05-20',
    }

    def __init__(self):
        pass

    def do_request(self, url: str, params: dict, out: str):
        """Запрос к апи
           :param url: ссылка
           :param params: параметры запроса
           :param out: имя выходного файла
        """
        r = requests.get(url, params=params, verify=False)
        result = {}
        try:
            result = r.json()
        except Exception as e:
            logger.info('[URL]: %s' % r.url)
            logger.info('[ERROR]: %s, %s' % (e, r.text))
        if result:
            with open_file(out, 'w+', encoding='utf-8') as f:
                f.write(json.dumps(result))
        return result

    def dates2params(self, start_date, end_date):
        """Даты в параметры для запроса
           :param start_date: Дата начала
           :param end_date: Дата окончания
        """
        params = self.default_params.copy()
        params['start_date'] = start_date
        params['end_date'] = end_date
        return params

    def get_autolots(self, start_date, end_date):
        """Получение автолотов
           :param start_date: Дата начала
           :param end_date: Дата окончания
        """
        urla = '%s%s' % (self.domain, self.autolots_endpoint)
        params = self.dates2params(start_date, end_date)
        result = self.do_request(url=urla, params=params, out='jdocs_get_autolots.json')
        return result

    def get_lots(self, start_date: str, end_date: str):
        """Получение лотов
           :param start_date: Дата начала
           :param end_date: Дата окончания
        """
        urla = '%s%s' % (self.domain, self.lots_endpoint)
        params = self.dates2params(start_date, end_date)
        result = self.do_request(url=urla, params=params, out='jdocs_get_lots.json')
        return result

    def load_exmple_from_old_format(self, lot_number: str):
        """Загрузить файл ylots.json (старый формат)
           и найти в нем лот - для сопоставления с новым форматом
           :param lot_number: номер лота
        """
        with open_file('ylots.json', 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
        for item in content:
            if not item['numar'] == lot_number:
                continue
            with open_file('%s_old.json' % lot_number, 'w+', encoding='utf-8') as f:
                f.write(json.dumps(item))
            date = item.get('data')
            new_lots = self.get_lots(start_date=date, end_date=date)
            for new_lot in new_lots:
                if not new_lot['yahoo_id'] == lot_number:
                    continue
                with open_file('%s_new.json' % lot_number, 'w+', encoding='utf-8') as f:
                    f.write(json.dumps(new_lot))

                catched = []
                # ---------------------------
                # Пробуем отобразить линковки
                # ---------------------------
                for k, v in new_lot.items():
                    print('--- %s=%s ---' % (k, v))
                    is_catched = False
                    for i, j in item.items():
                        if v == j:
                            catched.append(i)
                            print('    %s=%s' % (i, j))
                for i, j in item.items():
                    if not i in catched:
                        print('___   Not catched %s=%s' % (i, j))
                return new_lot

    def prepare_data(self, lots):
        """Подготавливаем лоты для вставки в таблицу
           :param lots: лоты, которые будем подготавливать
        """
        lots_old_format = []
        # Маппинг на старый формат
        mapping = {
            'Client': 'numeprenume', # Клиент
            'yahoo_id': 'numar', # Номер лота
            'purchase_date': 'data', # Дата покупки
            'payment_date': 'data_oplacino',
            'warehouse': 'data_primire',
            'arrived_date': 'data_primire_ru', # Дата прихода
            'qnt1': 'kolicistvo',
            'qnt2': 'kolicistvo_client',
            'product_name': 'description', # Название лота
            'client_price': 'price_pocup', # price?
            'client_bank_fee': 'price_bank_com',
            'client_delivery_fee': 'price_deliveri_client', # price_deliveri?
            'client_others': 'price_alte_client',
            'commission': 'price_com',
            'client_total': 'price_total', # Итого, клиент ¥
            'international_courier': 'transport',
            'yahoo_part_name': 'marka_part',
            'part_category_name': 'model_part',
            'tracking_no': 'nrotpravka',
            'export_date': 'data_livrare',
            'weight': 'ves',
            'order_number': 'order_number',
        }
        for lot in lots:
            lot_old_format = {}
            for new_key, old_key in mapping.items():
                lot_old_format[old_key] = lot[new_key]
            lot_old_format['images'] = [{
                'link': img['image_full_path'],
            } for img in lot.get('images', [])]
            lots_old_format.append(lot_old_format)

        with open_file('jdocs_prepared_data.json', 'w+', encoding='utf-8') as f:
            f.write(json.dumps(lots_old_format))
        return lots_old_format


    def prepare_autolots_data(self, lots):
        """Подготавливаем лоты для вставки в таблицу
           :param lots: лоты, которые будем подготавливать
        """
        lots_old_format = []
        # Маппинг на старый формат

        mapping = {
            'car_id': 'doko_id',
            'date': 'doko_created',
            'lot_no': 'number',
            'car_maker': 'mark',
            'yearMonth': 'year',
            'm3': 'volume',
            'price_c': 'price',
            'tax_c': 'tax',
            'auction_fee': 'auction_tax',
            'recycle_fee': 'recycle_tax',
            # 'shaken_c',
            'commission': 'deduction',
            'delivery_c': 'delivery',
            'dismantling': 'disassemble',
            'freight_c': 'freight',
            'agent_fee_k': 'exp_cert',
            'notes': 'notice',
            'car_options': 'options',
            'export_port': 'deliveryman',
            'shipping_line': 'provider',
            'type_of_export': 'export_method',
            'stock_yard': 'parking', # date
            # 'bl_date', # date
            'documents_sent': 'shipment', # date
            'ship_loading': 'ship_loading',
            'ETA': 'ho',
            'voyage_No': 'flight',
            'bl_number': 'bl',
            'discharge_port': 'from_port',
            # 'destination',
        }
        for lot in lots:
            lot_old_format = {}
            for new_key, old_key in mapping.items():
                lot_old_format[old_key] = lot[new_key]
            lots_old_format.append(lot_old_format)

        with open_file('jdocs_prepared_autolots_data.json', 'w+', encoding='utf-8') as f:
            f.write(json.dumps(lots_old_format))
        return lots_old_format

