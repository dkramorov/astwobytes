#-*- coding:utf-8 -*-
import traceback
import datetime
import xml.sax
import json
import requests

from django.conf import settings
from django.core.cache import cache

from apps.main_functions.date_time import str_to_date
from apps.main_functions.files import open_file, check_path

class CBRCurrencyParser(xml.sax.ContentHandler):
    """Парсер валют
       https://www.cbr.ru/scripts/XML_daily.asp
       <ValCurs Date="02.03.2002" name="Foreign Currency Market">
         <Valute ID="R01010">
         <NumCode>036</NumCode>
         <CharCode>AUD</CharCode>
         <Nominal>1</Nominal>
         <Name>Австралийский доллар</Name>
         <Value>16,0102</Value>
       </Valute> ...
    """
    def __init__(self, voca=None):
        self.result = []
        self.currency = {}
        self.ValCursName = "ValCurs"
        self.isValCurs = 0 # <ValCurs>
        self.ValuteName = "Valute"
        self.isValute = 0 # <Valute>
        self.NumCodeName = "NumCode"
        self.isNumCode = 0 # <NumCode>
        self.NumCodeValue = ""
        self.CharCodeName = "CharCode"
        self.isCharCode = 0 # <CharCode>
        self.CharCodeValue = ""
        self.NominalName = "Nominal"
        self.isNominal = 0 # <Nominal>
        self.NominalValue = ""
        self.NameName = "Name"
        self.isName = 0 # <Name>
        self.NameValue = ""
        self.ValueName = "Value"
        self.isValue = 0 # <Value>
        self.ValueValue = ""

    def startElement(self, name, attributes):
      if name == self.ValCursName:
          self.isValCurs = 1

      if self.isValCurs:
          if name == self.ValuteName:
              self.isValute = 1
              self.currency = {
                  'id': attributes.get('ID'),
              }

      if self.isValute:
          if name == self.NumCodeName:
              self.isNumCode = 1
          if name == self.CharCodeName:
              self.isCharCode = 1
          if name == self.NominalName:
              self.isNominal = 1
          if name == self.NameName:
              self.isName = 1
          if name == self.ValueName:
              self.isValue = 1

    def characters(self, content):
        if self.isValute:
            if self.isNumCode:
                self.NumCodeValue += content
            if self.isCharCode:
                self.CharCodeValue += content
            if self.isNominal:
                self.NominalValue += content
            if self.isName:
                self.NameValue += content
            if self.isValue:
                self.ValueValue += content

    def endElement(self, name):
        if name == self.ValCursName:
            self.isValCurs = 0

        if name == self.ValuteName:
            nominal = self.currency['nominal']
            self.currency['nominal'] = float(nominal.replace(',', '.'))
            value = self.currency['value']
            self.currency['value'] = float(value.replace(',', '.'))
            self.result.append(self.currency)
            self.currency = {}
            self.isValute = 0

        if self.isValute:
            if name == self.NumCodeName:
                self.currency['num_code'] = self.NumCodeValue
                self.isNumCode = 0
                self.NumCodeValue = ""
            if name == self.CharCodeName:
                self.currency['char_code'] = self.CharCodeValue
                self.isCharCode = 0
                self.CharCodeValue = ""
            if name == self.NominalName:
                self.currency['nominal'] = self.NominalValue
                self.isNominal = 0
                self.NominalValue = ""
            if name == self.NameName:
                self.currency['name'] = self.NameValue
                self.isName = 0
                self.NameValue = ""
            if name == self.ValueName:
                self.currency['value'] = self.ValueValue
                self.isValue = 0
                self.ValueValue = ""

def get_currency_cbr(date=None,
                     url: str = None,
                     cache_time: int = 60 * 60 * 5,
                     force_new: bool = False):
    """Получить курс валют за дату
       :param date: дата за которую запрашиваем курс
       :param url: альтернативный адрес для получения курса валют
       :param cache_time: время кэширования
       :param force_new: ключ кэширования
    """
    if not date:
        date = datetime.date.today()
    elif type(date) in (str, unicode):
        date = str_to_date(date)
        if not date:
            return []

    cache_var = '%s_get_currency_cbr_%s' % (
        settings.PROJECT_NAME,
        date.strftime('%Y-%m-%d')
    )
    inCache = cache.get(cache_var)
    if inCache and not force_new:
        print('--- get_currency_cbr from cache ---')
        return inCache

    currency_file = 'cbr_currency.json'
    # Ввели твари проверку на бота
    urla = 'https://www.cbr.ru/scripts/XML_daily.asp'
    if url:
        urla = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4 (compatible; YandexMobileBot/3.0; +http://yandex.com/bots)',
    }
    params = {
        'date_req': date.strftime("%d/%m/%Y"),
    }
    r = requests.get(urla, params=params, headers=headers, stream=True)
    result = r.text

    try:
        handler = CBRCurrencyParser()
        xml.sax.parseString(result, handler)
        # На всякий случай запишем в файл,
        # Если будет ошибка, хотя бы из файла вытащим
        with open_file(currency_file, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(handler.result))
        cache.set(cache_var, handler.result, cache_time)
        return handler.result
    except Exception as e:
        print('[RESPONSE]: %s' % r.text)
        print(traceback.format_exc())
        print('[ERROR]: %s' % e)

    if not check_path(currency_file):
        with open_file(currency_file, 'r', encoding='utf-8') as f:
            result = json.loads(f.read())
        return result


