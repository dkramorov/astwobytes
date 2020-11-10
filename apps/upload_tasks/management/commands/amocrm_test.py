#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from django.core.management.base import BaseCommand

from apps.main_functions.files import open_file, check_path
from apps.main_functions.catcher import json_pretty_print
from apps.upload_tasks.amocrm import AmoCRM

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--start',
            action = 'store',
            dest = 'start',
            type = str,
            default = False,
            help = 'Set start date')
        parser.add_argument('--end',
            action = 'store',
            dest = 'end',
            type = str,
            default = False,
            help = 'Set end date')

    def handle(self, *args, **options):
        amocrm = AmoCRM()
        #amocrm.update_access_token()

        #amocrm.get_deals(**{
        #    'query': 9557071,
        #})
        #amocrm.get_deal(9557071)
        custom_fields_values = [{
            'field_id': 68675, # Страховой продукт
            'values': [{
                'value': 'КАСКО', # Можно и 142953 здесь (ид)
            }, ],
        }, {
            'field_id': 340829, # "Марка/модель"
            'values': [{
                'value': 'Тестовая марка/модель',
            }, ],
        }, {
            'field_id': 340831, # Год выпуска
            'values': [{
                'value': 2001,
            }, ],
        }, ]

        additional_data = [{
            'field_id': 624677, # Дата начала
            'values': [{
                'value': 1586476800, # timestamp
            }, ],
        }, {
            'field_id': 624679, # Дата окончания
            'values': [{
                'value': 1586476800 # timestamp
            }, ],
        }, ]

        deals = [{
            'name': 'Тестовая заявка 2',
            'status_id': 19480819,
            'pipeline_id': 1115932, # ид воронки ДВС
            'created_by': 0,
            'updated_by': 0,
            'custom_fields_values': custom_fields_values,
        }]
        #print(json_pretty_print(deals))
        #deal = amocrm.create_deals(deals)
        #print(json_pretty_print(deal))
        #print(json_pretty_print(amocrm.get_custom_fields('leads')['_embedded']['custom_fields']))

        custom_fields_values = [{
            'field_id': 45935, # Телефон (PHONE)
            'values': [{
                'value': '89148-123-321',
                'enum_code': 'MOB',
            }, ],
        }, {
            'field_id': 45937, # Email (EMAIL)
            'values': [{
                'value': 'test@test.ru',
                'enum_code': 'PRIV',
            }, ],
        }, {
            'field_id': 148765, # Дата рождения
            'values': [{
                'value': 1586476800 # timestamp,
            }, ],
        }, ]
        contacts = [{
            'name': 'Тестовый пользователь 2',
            'first_name': '',
            'last_name': '',
            'created_by': 0,
            'updated_by': 0,
            'custom_fields_values': custom_fields_values,
        }]
        #print(json_pretty_print(contacts))
        #contact = amocrm.create_contacts(contacts)
        #print(json_pretty_print(contact))
        #print(json_pretty_print(amocrm.get_custom_fields('contacts')['_embedded']['custom_fields']))

        test_deal_id = 27478111
        test_contact_id = 45990887
        #rel = amocrm.link_deal2contact(test_deal_id, test_contact_id)
        #print(json_pretty_print(rel))
