# -*- coding: utf-8 -*-
import requests

from django.conf import settings

from apps.main_functions.catcher import json_pretty_print

YANDEX_GEOCODE_URL = 'https://geocode-maps.yandex.ru/1.x/'

def ask_yandex_address_by_point(point: list):
    """Спросить yandex об адресе (по координатам)
       В геокодере координаты перевернуты
       :param point: массив с координатами
    """
    return ask_yandex_address_by_coords(point[0], point[1])

def ask_yandex_address_by_coords(latitude: float, longitude: float):
    """Спросить yandex об адресе (по координатам)
       В геокодере координаты перевернуты
       :param latitude: latitude
       :param longitude: longitude
    """
    params = {
        'apikey': settings.YANDEX_MAPS_API_KEY,
        'geocode': '{},{}'.format(longitude, latitude),
        'format': 'json',
    }
    r = requests.get(YANDEX_GEOCODE_URL,
                     params=params,
                     headers={"User-Agent" : "Googlebot/2.1"})
    resp = r.json()
    return resp

def parse_yandex_address(resp: dict):
    """Разобрать ответ, полученный от Яндекса
       :param resp: ответ от Яши на запрос по координатам
    """
    address = {}
    geo_obj_collection = resp['response']['GeoObjectCollection']
    members = geo_obj_collection.get('featureMember', [])
    if not members:
        return
    member = members[0]
    geo_obj = member.get('GeoObject')

    coord1, coord2 = geo_obj['Point']['pos'].split(' ')
    address['latitude'] = coord2
    address['longitude'] = coord1

    meta = geo_obj['metaDataProperty']
    geo = meta['GeocoderMetaData']
    details = geo['AddressDetails']
    address['addressLines'] = geo['text']
    country = details['Country']
    address['country'] = country['CountryName']

    subadministrative_area = None
    locality = None
    dependent_locality = None
    sub_dependent_locality = None
    thoroughfare = None
    premise = None
    postal_code = None

    administrative_area = country.get('AdministrativeArea')
    if administrative_area:
        address['state'] = administrative_area['AdministrativeAreaName']
        subadministrative_area = administrative_area.get('SubAdministrativeArea')
        locality = administrative_area.get('Locality')

    if subadministrative_area:
        address['county'] = subadministrative_area.get('SubAdministrativeAreaName')
        locality = subadministrative_area.get('Locality') if not locality else locality

    if locality:
        address['city'] = locality.get('LocalityName')
        dependent_locality = locality.get('DependentLocality')
        thoroughfare = locality.get('Thoroughfare')

    if thoroughfare:
        address['street'] = thoroughfare.get('ThoroughfareName')
        premise = thoroughfare.get('Premise')

    if dependent_locality:
        address['street'] = dependent_locality.get('DependentLocalityName')
        premise = dependent_locality.get('Premise') or premise
        sub_dependent_locality = dependent_locality.get('DependentLocality')

    if sub_dependent_locality:
        address['subdistrict'] = sub_dependent_locality.get('DependentLocalityName')

    if premise:
        address['houseNumber'] = premise.get('PremiseNumber')
        postal_code = premise.get('PostalCode')

    if postal_code:
        address['postalCode'] = postal_code.get('PostalCodeNumber')

    return address

def ask_yandex_address_by_str(adr):
    """Получить от Яши данные по адресу по строке
       :param adr: адрес строкой
    """
    geo_object = None
    params = {
        'apikey': settings.YANDEX_MAPS_API_KEY,
        'geocode': adr,
        'format': 'json',
    }
    r = requests.get(YANDEX_GEOCODE_URL,
                     params=params,
                     headers={"User-Agent" : "Googlebot/2.1"})
    resp = r.json()
    return resp

# TODO переделать
def ask_2gis_address_by_str(adr):
    """Спросить 2gis об адресе (по строке)"""
    geo_object = None
    adr = adr.encode("utf-8")
    key = "ruoedw9225"
    params = urllib.urlencode({"q":adr, "key":key, "version":"1.3"})
    urla  = "http://catalog.api.2gis.ru/geo/search?%s" % params
    req = urllib2.Request(urla, headers={"User-Agent" : "Googlebot/2.1"})
    try:
      resp = urllib2.urlopen(req)
      content = json.loads(resp.read())
    except:
      return None
    if "response_code" in content:
      try:
        code = int(content['response_code'])
      except ValueError:
        code = 0
      if not code == 200:
        error = u"response code is not 200, but %s %s" % (content['response_code'], content['error_message'])
        return None
      if "total" in content:
        try:
          total = int(content['total'])
        except ValueError:
          total = None
        if total:
          if total == 1:
            geo_object = content['result'][0]
    return geo_object

# TODO переделать
def parse_2gis_address(geo_object):
    """Пропарсить адрес, полученный от 2gis
       Возвращаем models Address или None
    """
    result = None
    coords = geo_object['selection'].replace("POINT(", "").replace(")", "").split(" ")
    new_address = {}
    for kind, name in geo_object['attributes'].items():
      if kind == "city":
        new_address['city'] = name
      if kind == "index":
        new_address['postalCode'] = name
      if kind == "street":
        new_address['street'] = name
      if kind == "number":
        new_address['houseNumber'] = name
    # ----------------------------
    # Если номера дома нету,
    # тогда какой нахер это адрес?
    # ----------------------------
    if "houseNumber" in new_address:
      # ---------------------------------
      # По координатам ищем запись в базе
      # ---------------------------------
      latitude = "%.25f" % float(coords[1])
      longitude = "%.25f" % float(coords[0])
      new_address['latitude'] = latitude
      new_address['longitude'] = longitude
      analogs = Addresses.objects.filter(latitude=latitude, longitude=longitude)
      # ----------------------------------------
      # Если в старом адресе имеются координаты,
      # нужно вычислять погрешность и проверять
      # ----------------------------------------
      if analogs:
        result = analogs[0]
      else:
        result = Addresses()
        for key, value in new_address.items():
          setattr(result, key, value)
    return result
