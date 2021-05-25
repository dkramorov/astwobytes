#!/usr/env/env python3
import os
import json
import requests

from django.conf import settings
from envparse import env

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file

env.read_envfile(os.path.join(settings.BASE_DIR, 'conf', '.env'))

class APIJDOCS():
    """Класс для работы с jdocs (получение лотов)
    """
    login = env('API_JDOCS_USER')
    passwd = env('API_JDOCS_PASSWD')
    domain = 'https://users.jsmjapan.com'
    lots_endpoint = '/ru/site/get-user-records'
    default_params = {
        'key': passwd,
        'start_date': '2021-05-01',
        'end_date': '2021-05-20',
    }

    def __init__(self):
        pass

    def get_lots(self, start_date: str, end_date: str):
        """Получение лотов
           :param start_date: Дата начала
           :param end_date: Дата окончания
        """
        urla = '%s%s' % (self.domain, self.lots_endpoint)
        params = self.default_params.copy()
        params['start_date'] = start_date
        params['end_date'] = end_date
        r = requests.get(urla, params=params)
        result = {}
        try:
            result = r.json()
        except Exception as e:
            logger.info('[ERROR]: %s, %s' % (e, r.text))
        if result:
            with open_file('jdocs_get_lots.json', 'w+', encoding='utf-8') as f:
                f.write(json.dumps(result))
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
        # Маппинг на старый формат
        mapping = {
            'yahoo_id': 'numar', # Номер лота
            'purchase_date': 'data', # Дата покупки
            'payment_date': 'data_oplacino',
            'warehouse': 'data_primire',
            'arrived_date': 'data_primire_ru', # Дата прихода
            'qnt1': 'kolicistvo',
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
        }
        for lot in lots:
            new_lot = {}
            for new_key, old_key in mapping.items():
                new_lot[old_key] = lot[new_key]
            new_lot['images'] = [img['image_full_path'] for img in lot.get('images', [])]
        print(json_pretty_print(new_lot))
        return new_lot


