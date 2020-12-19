# -*- coding: utf-8 -*-
from apps.addresses.models import Address

def ask_yandex_address_by_coords(lat, lon):
    """Спросить yandex об адресе (по координатам)"""
    key = "c25babc5-3c2c-4831-90d8-3900fda08fda"
    params = urllib.urlencode({
      "apikey":key,
      "geocode": "{},{}".format(latitude, longitude),
      "format": "json",
    })
    urla = "https://geocode-maps.yandex.ru/1.x/?%s" % params
    req = urllib2.Request(urla, headers={"User-Agent" : "Googlebot/2.1"})
    try:
      resp = urllib2.urlopen(req)
      content = json.loads(resp.read())
    except:
      print "[ERROR] urlopen", urla
      return None
    return content

def ask_yandex_address_by_str(adr):
    """Спросить Яндекс об адресе (по строке)
    """
    geo_object = None
    adr = adr.encode("utf-8")
    params = urllib.urlencode({"geocode":adr, "format":"json"})
    urla = "https://geocode-maps.yandex.ru/1.x/?%s" % params
    req = urllib2.Request(urla, headers={"User-Agent" : "Googlebot/2.1"})
    try:
      resp = urllib2.urlopen(req)
      content = json.loads(resp.read())
    except:
      print "[ERROR] urlopen", urla
      return None
    # -------------------------------
    # featureMember может быть пустым
    # в нем GeoObject массив
    # -------------------------------
    collection = content['response']['GeoObjectCollection']['featureMember']
    # ----------------------------------------------------------
    # Если не найдем exact, тогда будем показывать то, что рядом
    # ----------------------------------------------------------
    number = None
    near = None

    for item in collection:
      item = item['GeoObject']
      meta_data_property = item['metaDataProperty']
      geocoder_meta_data = meta_data_property['GeocoderMetaData']
      kind = geocoder_meta_data['kind']
      precision = geocoder_meta_data['precision']
      # https://tech.yandex.ru/maps/doc/geocoder/desc/reference/precision-docpage/
      if kind == "house" and not geo_object:
        if precision == "exact":
          geo_object = item
          break
        if precision == "number":
          number = item
        if precision == "near":
          near = item
    if not geo_object:
      if number:
        geo_object = number
      elif near:
        geo_object = near
      else:
        pass
    return geo_object

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
      print "[ERROR] urlopen", urla
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

def parse_yandex_address(geo_object):
    """Пропарсить адрес, полученный от Яндекса
       Возвращаем models Address или None
    """
    result = None
    if not geo_object:
      return result
    coords = geo_object['Point']['pos'].split(" ")
    meta_data_property = geo_object['metaDataProperty']
    geocoder_meta_data = meta_data_property['GeocoderMetaData']
    geo_object_address = geocoder_meta_data['Address']
    # route Приволжская железная дорога
    # railway станция Садовая
    kind_vars = ("country", "province", "area", "locality", "district", "street", "house", "route", "railway")
    new_address = {}
    for component in geo_object_address['Components']:
      kind = component['kind']
      name = component['name']
      if not kind in kind_vars:
        print "[ERROR]:", kind
        return new_address
      if kind == "country":
        new_address['country'] = name
      if kind == "province":
        new_address['state'] = name
      if kind == "area":
        new_address['county'] = name
      if kind == "locality":
        new_address['city'] = name
      if kind == "district":
        new_address['district'] = name
      if kind == "route":
        new_address['route'] = name
      if kind == "railway":
        new_address['railway'] = name
      if kind == "street":
        new_address['street'] = name
      if kind == "house":
        new_address['houseNumber'] = name
    # ----------------------------
    # Если номера дома нету,
    # тогда какой нахер это адрес?
    # ----------------------------
    if "houseNumber" in new_address:
      # ------------------
      # Дозаполняем ерунду
      # ------------------
      if not "district" in new_address:
        if "route" in new_address:
          new_address['district'] = new_address['route']
      if not "district" in new_address:
        if "railway" in new_address:
          new_address['district'] = new_address['district']
      # ---------------------------------
      # По координатам ищем запись в базе
      # ---------------------------------
      latitude = "%.25f" % float(coords[1])
      longitude = "%.25f" % float(coords[0])
      new_address['latitude'] = latitude
      new_address['longitude'] = longitude
      analogs = Addresses.objects.filter(latitude=latitude, longitude=longitude)
      #print analogs, latitude, longitude
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
    else:
      print "[WARN]: There is no houseNumber", geo_object
    return result
