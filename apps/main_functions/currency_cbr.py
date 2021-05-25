#-*- coding:utf-8 -*-
import datetime
import xml.sax
import requests

from apps.main_functions.date_time import str_to_date

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
          self.isValCursName = 1

      if self.isValCursName:
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

def get_currency_cbr(date=None):
    """Получить курс валют за дату
       :param date: дата за которую запрашиваем курс
    """
    if not date:
        date = datetime.date.today()
    elif type(date) in (str, unicode):
        date = str_to_date(date)
        if not date:
            return []

    urla = 'https://www.cbr.ru/scripts/XML_daily.asp'
    params = {
        'date_req': date.strftime("%d/%m/%Y"),
    }
    r = requests.get(urla, params=params)
    result = r.text

    handler = CBRCurrencyParser()
    xml.sax.parseString(result, handler)
    return handler.result
