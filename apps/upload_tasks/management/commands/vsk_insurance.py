#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print

from zeep import Client
from zeep.plugins import HistoryPlugin
from zeep import transports
from lxml import etree

logger = logging.getLogger(__name__)

def get_history(history):
    """Получить историю запросов"""
    try:
        for hist in [history.last_sent, history.last_received]:
            print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))
    except (IndexError, TypeError):
        # catch cases where it fails before being put on the wire
        pass

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
        """ВСК Стархование"""

        ENDPOINT = 'http://autoservice.vsk.ru/companies/vsk/services/eltpoiskintegration.asmx?wsdl'

        def get_methods(api):
            """Получить методы сервиса"""
            service = list(dict(api.wsdl.services).values())[0]
            port = list(dict(service.ports).values())[0]
            return port.binding._operations.items()

        def get_elements(method_name: str = 'CALC_DATAv2'):
            """Получить элементы метода"""
            for method in get_methods(client):
                if method[0] == method_name:
                    operation = method[1]
                    return operation.input.body.type.elements

        def parse_elements(elements):
            """Обход всех элементов метода"""
            all_elements = {}
            for name, element in elements:
                all_elements[name] = {}
                all_elements[name]['optional'] = element.is_optional
                if hasattr(element.type, 'elements'):
                    all_elements[name]['type'] = parse_elements(element.type.elements)
                else:
                    all_elements[name]['type'] = str(element.type)
            return all_elements

        def demo_explain():
            """Пример, как вывести параметры для
               тела документа,
               которые передаем в метод"""
            elements = get_elements()
            print(json_pretty_print(parse_elements(elements)))


        history = HistoryPlugin()
        client = Client(ENDPOINT, plugins=[history])

        #client.transport.session.proxies = {
        #    'http': 'http://10.10.9.1:3128',
        #    'https': 'http://10.10.9.1:3128'
        #}
        demo_explain()

        login = "int_ts_msik_20170713"
        passwd = "148362ab"
        context = {
            'CalcFinal': False,
            'DateCalc': datetime.datetime.today(),
            'DurationMonth': 12,
            'InsuredJuridical': False,
            'LduType': 0,
            'UserLogin': login,
            'UserPass': passwd,
        }

        try:
            resp = client.service.CALC_DATAv2(**context)
        except Exception as e:
            resp = None
            print(e)
        get_history(history)

        if resp:
            print(resp)