# -*- coding:utf-8 -*-
import time
import datetime
import os

from django import template
from django.conf import settings
from django.core.cache import cache

from apps.main_functions.catcher import defiz_phone

register = template.Library()

@register.filter(name = 'defizize')
def defizize(item):
    """Ставим дефизы для телефона"""
    new_phone = defiz_phone(item)
    if new_phone:
        item = new_phone
    return item

#################################################
# Убираем из текста все кавычки и спец символы
# Нужно для вставки в атрибуты тегов,
# например alt="" или title=""
#################################################
@register.filter(name="textize")
def textize(item):
  if not item:
    item = ""
  if not type(item) == str or not type(item) == unicode:
    try:
      item = unicode(item)
    except:
      item = ""
  item = item.replace("\r", " ")
  item = item.replace("\n", " ")
  item = kill_quotes(item, "just_text")
  return item

#################################################
# Урезаем текст до нужной длины
#################################################
@register.filter(name="cut_length")
def cut_length(item, size=60):
  if not item:
    item = ""
  if not type(item) == unicode:
    try:
      item = unicode(item)
    except:
      return ""
  if len(item) > size:
    item = item[:size]+"..."
  return item

#################################################
# img - имя файла, например 1.jpg
# size - размер, например 150х150 икс разделитель
# source - папка с исходным изображением, например, logos
# dest - папка, куда будем складировать масштабированные изображения, например id_parent
# Например, <img src="{% imagine 'help.png' '150x150' 'img' 1 %}"/>
# Например, <img src="{% imagine client_value.properties.logo '150x150' 'logos' client_value.properties.id %}" />
# now - для параметра в изображении
# alt = path => вернет просто путь до изображения
#################################################
@register.simple_tag
def imagine(img, size, source, alt="", dyn=None):
  if not img:
    return ""
  now = ""
  if dyn:
    now = str(time.time())
    now = now.replace(".", "_")
    now = "?%s" % now

  alt = kill_quotes(alt, "strict_text", " ")
  # -----------------------------------
  # Изображение на удаленном хостинге
  # Весь удаленно расположенный контент
  # следует грузить через lazy load js
  # Нужно передать размеры XXXxYYY
  # NOW не следует использовать - пусть
  # удаленный сервер отвечает правильно
  # -----------------------------------
  if img.startswith("http"):
    return "<img data-original=\"%s?size=%s\" alt=\"%s\" class=\"lazy\" src=\"/static/img/misc/loading.gif\"/>" % (img, size, alt)

  size_array = size.split("x")
  ups_path = "/static/img/misc/ups.png"
  ups_image = "<img src=\"%s\" />" % ups_path
  if not img:
    return ups_image
  path_resized_img = imagine_image(img, size, source)
  if not path_resized_img:
    return ups_image
  # ----------------------------------
  # Добавляем alt="..." или возвращаем
  # путь до изображения
  # ----------------------------------
  if alt:
    alt = kill_quotes(alt, "strict_text", " ")
    if alt == "path":
      return path_resized_img
    alt="alt=\"%s\"" % alt

  return "<img src=\"%s%s\" %s />" % (path_resized_img, now, alt)

#################################################
# Фильтр для проверки изображения
# на наличие/локальность
#################################################
@register.filter(name="check_img")
def check_img(item):
  if not item: # Нет картинки
    return 0
  if item.startswith("http"): # Изображение на удаленном хосте
    return 2
  return 1 # Локальное изображение

#################################################
# Количество новых сообщений пользователя
# Нужно кэшить на 30 секунд функцию по
# settings.DATABASES['default']['NAME'] + "messages" + request.user.id
#################################################
@register.simple_tag
def messages_count(request):
  html = ""
  if not isMessages:
    return ""
  cache_time = 30
  cache_var = "%s_messages_%s" % (settings.DATABASES['default']['NAME'], request.user.id)
  inCache = cache.get(cache_var)
  if inCache:
    html = inCache
  else:
    now  = datetime.datetime.today()
    try:
      count = Message.objects.filter(to_user=request.user.id, state_to=0, date_show__lte=now).aggregate(Count("id"))['id__count']
    except:
      return ""
    if count > 0:
      html += "<img src=\"/static/img/noizum/icons/packs/fugue/16x16/mail.gif\">"
      html += u"&nbsp;Новые сообщения: %s" % (count, )
    else:
      html += "<img src=\"/static/img/noizum/icons/packs/fugue/16x16/mail.png\">"
    cache.set(cache_var, html, cache_time)
  return html

#################################################
# Стат. страничка по тегу
# При отсутствии она создается по тегу
# Нужно кэшить на 15 секунд функцию по
# settings.DATABASES['default']['NAME'] + "statcontent" + tag
#################################################
@register.simple_tag
def statcontent(tag):
  from flatpages.models import Arts
  art = []
  cache_time = 30
  cache_var = "%s_statcontent_%s" % (settings.DATABASES['default']['NAME'], tag)
  inCache = cache.get(cache_var)
  if inCache:
    art = inCache
  else:
    arts = Arts.objects.filter(tag=tag)
    if arts:
      art = arts[0]
    else:
      art = Arts.objects.create(name=tag, tag=tag, body="")
    cache.set(cache_var, art.body, cache_time)
    art = art.body
  return art

#################################################
# Понижение прозрачности для вотермарки
# im - уже открытое Image по полному пути
def reduce_opacity(im, opacity):
  import ImageEnhance
  """Returns an image with reduced opacity."""
  assert opacity >= 0 and opacity <= 1
  if im.mode != 'RGBA':
    im = im.convert('RGBA')
  else:
    im = im.copy()
  alpha = im.split()[3]
  alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
  im.putalpha(alpha)
  return im

#################################################
# Вотермарка
# Пути до изображений (logos/1.png, например)
# source - путь до исходной картинки, mark - оверлей (логотип)
# img_name - имя изображения
#################################################
@register.simple_tag
def watermark(img_name, source, size="", mark="img/logo.png", position="tile", opacity=0.1, folder="resized"):
  folder = str(folder)
  size_array = (150, 150)
  # Проверяем есть ли вообще с чем работать
  path_img = os.path.join(source, img_name)
  if check_path(path_img):
    return "/static/img/misc/ups.png"

  if check_path(os.path.join(source, folder)):
    make_folder(os.path.join(source, folder))

  if "x" in size:
    size_array = size.split("x")
    result = os.path.join(source, folder, "watermark_"+size+"_"+img_name)
    if not check_path(result): # Если уже есть вотермарка
      return "/media/"+result

    #############################################
    # Проверяем есть ли уже миниатюра, дабы не создавать
    path_resized_img =  os.path.join(source, folder, size+"_"+img_name)
    if check_path(path_resized_img):
      copy_file(path_img, path_resized_img)
      imageThumb(path_resized_img, size_array[0], size_array[1])
    #############################################
    # Переписываем параметры функции
    img_name = size+"_"+img_name
    source = os.path.join(source, folder) # Переписываем рабочую папку
  else:
    result = os.path.join(source, folder, "watermark_"+img_name)
    if not check_path(result): # Если уже есть вотермарка
      return "/media/"+result

  import Image

  img_path = full_path(os.path.join(source, img_name))
  if not check_path(img_path):
    im = Image.open(img_path)
  else:
    return "/static/img/misc/ups.png"
  mark = Image.open(full_path(mark))
  #Adds a watermark to an image
  if opacity < 1:
    mark = reduce_opacity(mark, opacity)
  if im.mode != 'RGBA':
    im = im.convert('RGBA')
  # create a transparent layer the size of the image and draw the
  # watermark in that layer.
  layer = Image.new('RGBA', im.size, (0,0,0,0))
  if position == 'tile':
    for y in range(0, im.size[1], mark.size[1]):
      for x in range(0, im.size[0], mark.size[0]):
        layer.paste(mark, (x, y))
  elif position == 'scale':
    # scale, but preserve the aspect ratio
    ratio = min(float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
    w = int(mark.size[0] * ratio)
    h = int(mark.size[1] * ratio)
    mark = mark.resize((w, h))
    layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
  else:
    layer.paste(mark, position)
  # composite the watermark with the layer
  img = Image.composite(layer, im, layer)
  img.save(full_path(result))
  return "/media/"+result

#################################################
# TRANSLIT TAG
#################################################
@register.simple_tag
def translit_tag(text):
  text = translit(text)
  return text

#################################################
# Месяц из цифр прописью
#################################################
@register.simple_tag
def monthy(date, rp=1, socr=None):
  month = monthToStr(date, rp, socr)
  return month

#################################################
# День недели прописью
#################################################
@register.simple_tag
def weekly(date, rp=None, socr=None):
  weekday = weekdayToStr(date, rp, socr)
  return weekday

#################################################
# Визуальное разделение цифр в сумме по 3
#################################################
@register.filter(name="money_format")
def money_format(summa):
  return summa_format(summa)

#################################################
# Скидка на сумму по процентам (от суммы)
#################################################
@register.filter(name="percent_discont")
def percent_discont(summa, percent):
  if not summa or not percent:
    return summa
  try:
    result = float(summa)
  except ValueError:
    return summa
  p = summa/100 * percent
  result = summa - p
  return result

#################################################
# Удаление копеек
#################################################
@register.filter(name="kopeiko_killer")
def kopeiko_killer(summa):
  if summa:
    #if type(summa) == int or type(summa) == long:
    summa = str(summa)
    #else:
    #summa = summa.encode("utf-8")
    if summa.endswith(".00") or summa.endswith(",00"):
      summa = summa_format(summa[:-3])
    else:
      summa = summa_format(summa)
  return summa

#################################################
# ТЕГ ДЛЯ САЙТА
# Необходимо, чтобы шаблон был в web/ папке сайта
#################################################
@register.inclusion_tag("web/main_menu.html")
def mainmenu(request):
  from flatpages.models import Menu
  result = {}
  cache_time = 30
  cache_var = "%s_mainmenu" % settings.DATABASES['default']['NAME']
  inCache = cache.get(cache_var)
  if inCache:
    result = inCache
  else:
    menu = Menu.objects.filter(manager__domain="main")
    menu_queryset = []
    recursive_fill(menu, menu_queryset, "")
    menus = sort_voca(menu_queryset)
    result['menus'] = menus
    cache.set(cache_var, result, cache_time)
  result['request'] = request
  return result

#################################################
# ТЕГ ДЛЯ САЙТА
# Необходимо, чтобы шаблон был в web/ папке сайта
#################################################
@register.inclusion_tag("web/top_menu.html")
def topmenu(request):
  from flatpages.models import Menu
  result = {}
  cache_time = 30
  cache_var = "%s_topmenu" % settings.DATABASES['default']['NAME']
  inCache = cache.get(cache_var)
  if inCache:
    result = inCache
  else:
    menu = Menu.objects.filter(manager__domain="top")
    menu_queryset = []
    recursive_fill(menu, menu_queryset, "")
    menus = sort_voca(menu_queryset)
    result['menus'] = menus
    cache.set(cache_var, result, cache_time)
  result['request'] = request
  return result

#################################################
# ТЕГ ДЛЯ САЙТА
# Необходимо, чтобы шаблон был в web/ папке сайта
#################################################
@register.inclusion_tag("web/bottom_menu.html")
def bottommenu(request):
  from flatpages.models import Menu
  result = {}
  cache_time = 30
  cache_var = "%s_bottommenu" % settings.DATABASES['default']['NAME']
  inCache = cache.get(cache_var)
  if inCache:
    result = inCache
  else:
    menu = Menu.objects.filter(manager__domain="bottom")
    menu_queryset = []
    recursive_fill(menu, menu_queryset, "")
    menus = sort_voca(menu_queryset)
    result['menus'] = menus
    cache.set(cache_var, result, cache_time)
  result['request'] = request
  return result

#################################################
# ТЕГ ДЛЯ САЙТА
# Необходимо, чтобы шаблон был в web/ папке сайта
#################################################
@register.inclusion_tag("web/main_news.html")
def mainnews(count):
  from news.models import News
  result = {}
  try:
    count = int(count)
  except ValueError:
    count = 2
  cache_time = 20
  cache_var = "%s_news" % settings.DATABASES['default']['NAME']
  inCache = cache.get(cache_var)
  if inCache:
    result = inCache
  else:
    menus = News.objects.filter(section__isnull=True).order_by("-date_start")[:count]
    result['menus'] = menus
    cache.set(cache_var, result, cache_time)
  return result

#################################################
# Счетчики по модели Config
# counter = yandex_metrika, google_analytics
#################################################
@register.simple_tag
def counters(counter):
  result = ""
  if settings.DEBUG:
    return "<script type=\"text/javascript\">console.log(\"%s:there are no counters in debug\");</script>" % counter
  cache_time = 120
  cache_var = "%s_counters_%s" % (settings.DATABASES['default']['NAME'], counter)
  inCache = cache.get(cache_var)
  if inCache:
    result = inCache
  else:
    site_counters = Config.objects.filter(name="counters", attr=counter)
    if site_counters:
      site_counter = site_counters[0]
      cache.set(cache_var, site_counter.value, cache_time)
      result = site_counter.value
  return result

#################################################
# Перегруппировать объекты в контейнеры
# по n-элементов
# Например, надо вывести блоки, 
# в каждом по 4 элемента (count = 4)
#################################################
@register.filter(name="assembleby")
def assembleby(items, count=4):
  result = {}
  if not items:
    return result
  i = 0
  j = 0
  result[0] = []
  for item in items:
    if j < count:
      j += 1
    else:
      j = 1
      i += 1
      result[i] = []
    result[i].append(item)
  return result.values()

#################################################
# Разбить объекты на n-контейнеров
# Например, надо вывести 2 контейнера с
# равным кол-вом блоков (в первом больше)
#################################################
@register.filter(name="divide")
def divide(items, count=2):
  result = []
  if not items:
    return result
  items_len = len(items)
  per_container = items_len / count
  reminder = items_len % count
  diff = 0 
  for i in range(count):
    container = items[i*per_container+diff:i*per_container+per_container+diff]
    if reminder > 0:
      ind = i*per_container + per_container + diff
      container.append(items[ind])
      diff += 1
      reminder -= 1
    result.append(container)
  return result

#################################################
# Перегруппировать объекты в один контейнер
# Например, надо подготовить из 10 блоков список,
# который затем сделаем assembleby и будем
# выводить по n-элементов
# Работаем с sub в каждом блоке
#################################################
@register.filter(name="accumulate")
def accumulate(blocks):
  container = []
  for block in blocks:
    if hasattr(block, "sub"):
      for item in block.sub:
        # Сохраняем информацию о родительском блоке
        # иначе не сможем, например, отфильтровать по parent
        item.parent = block 
        container.append(item)
  return container

#################################################
# Пропускать блоки по тегу/без тега
# Если тег не указан, пропускаем с любым тегом
#################################################
@register.filter(name="pass_by_tag")
def pass_by_tag(blocks, tag=None):
  container = []
  for block in blocks:
    if hasattr(block, "tag"):
      if not tag:
        #if not block.tag:
        if block.tag:
          container.append(block)
      else:
        if not block.tag == tag:
          container.append(block)
  return container

#################################################
# Инвертировать массив
# И последние станут первыми :)
#################################################
@register.filter(name="reverse")
def reverse(blocks):
  if not blocks:
    return blocks
  return blocks[::-1]

#################################################
# Сортировка блоков
#################################################
@register.filter(name="sortedby")
def sortedby(blocks, field):
  if not blocks:
    return blocks
  key = lambda x:x.id
  if hasattr(blocks[0], field):
    key = lambda x:getattr(x, field)
  reverse = False
  if "-" in field:
    reverse = True
  return sorted(blocks, key=key, reverse=reverse)

#################################################
# В целое число
#################################################
@register.filter(name="parseInt")
def parseInt(text):
  if not text:
    return 0
  try:
    digit = int(text.strip())
  except ValueError:
    return 0
  return digit