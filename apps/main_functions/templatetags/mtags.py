# -*- coding:utf-8 -*-
import time
import datetime
import os

from django import template
from django.conf import settings
from django.core.cache import cache
#from django.utils.safestring import mark_safe

from apps.main_functions.string_parser import kill_quotes, translit, summa_format
from apps.main_functions.catcher import defiz_phone
from apps.main_functions.files import check_path, make_folder, copy_file, imageThumb, full_path, imagine_image
from apps.main_functions.date_time import monthToStr, weekdayToStr

register = template.Library()

UPS_PATH = '/static/img/ups.png'

@register.simple_tag
def settings_value(name: str):
    """Получение переменной из settings.py
       USAGE: {% settings_value "LANGUAGE_CODE" %}
    """
    return getattr(settings, name, '')

@register.filter(name = 'defizize')
def defizize(phone: str):
    """Ставим дефизы для телефона
       :param phone: телефон"""
    new_phone = defiz_phone(phone)
    if new_phone:
        phone = new_phone
    return phone

@register.filter(name='textize')
def textize(text: str):
    """Убираем из текста все кавычки и спец символы
       Нужно для вставки в атрибуты тегов,
       например alt="" или title=""
       :param text: текст
    """
    if not text:
        return ''
    if not isinstance(text, str):
        return text
    text = kill_quotes(text, 'strict_text', ' ')
    return text

@register.filter(name='cut_length')
def cut_length(text: str, size: int = 60):
    """Урезаем текст до нужной длины
       :param text: текст
       :param size: длина текста
    """
    if not text:
        return ''
    if not isinstance(text, str):
        return text
    if len(text) > size:
        text = '%s...' % text[:size]
    return text

@register.simple_tag
def imagine(img: str, size: str, source: str, alt: str = ''):
    """Создание миниатюры изображения
       :param img: имя файла, например 1.jpg
       :param size: размер, например 150х150, x разделитель
       :param source: папка с исходным изображением, например, logos
       :param alt: текст alt для изображения, если тип bool вернем просто путь до изображения
       USAGE:
       <img src="{% imagine 'help.png' '150x150' 'img' %}"/>
       {% imagine 'help.png' '150x150' 'img' True %} - просто путь
    """
    ups_path = UPS_PATH
    ups_image = '<img src="%s" />' % ups_path
    if not img:
        if isinstance(alt, bool):
            return ups_path
        return ups_image
    # -----------------------------------
    # Изображение на удаленном хостинге
    # Весь удаленно расположенный контент
    # следует грузить через lazy load js
    # Нужно передать размеры XXXxYYY
    # -----------------------------------
    if img.startswith('http'):
        if isinstance(alt, bool):
            return img
        return '<img data-original="%s?size=%s" alt="%s" class="lazy" src="/static/img/misc/loading.gif"/>' % (img, size, kill_quotes(alt, 'strict_text', ' '))

    path_resized_img = imagine_image(img, size, source)
    if not path_resized_img:
        if isinstance(alt, bool):
            return ups_path
        return ups_image

    if isinstance(alt, bool):
        return path_resized_img

    return '<img src="%s" alt="%s" />' % (path_resized_img, kill_quotes(alt, 'strict_text', ' '))

def reduce_opacity(im, opacity: float):
    """Возвращает изображение с пониженной прозрачностью,
       например, для вотермарки
       :param im: открытое Image по полному пути
       :param opacity: значение прозрачности
    """
    import ImageEnhance
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

@register.simple_tag
def watermark(img_name: str,
              source: str,
              size: str = '',
              mark: str = 'img/apple-touch-icon-114.png',
              position: str = 'tile',
              opacity: float = 0.1,
              folder: str = 'resized'):
    """Вотермарка
       :param img_name: Путь до изображения, например, logos/1.png
       :param source: путь до исходной картинки
       :param size: размер, например 150x150
       :param mark: оверлей-watermark (логотип)
       :param position: позиция вотермарки (tile/scale)
       :param opacity: значение прозрачности
       :param folder: папка, куда сохранить результат
    """
    folder = '%s' % folder
    size_array = (150, 150)
    # Проверяем есть ли вообще с чем работать
    path_img = os.path.join(source, img_name)
    if check_path(path_img):
        return UPS_PATH

    make_folder(os.path.join(source, folder))

    if 'x' in size:
        size_array = size.split('x')
        result = os.path.join(source, folder, 'watermark_%s_%s' % (size, img_name))
        # Если уже есть вотермарка
        if not check_path(result):
            return '/media/%s' % result

        # Если уже есть миниатюра
        path_resized_img =  os.path.join(source, folder, '%s_%s' % (size, img_name))
        if check_path(path_resized_img):
            copy_file(path_img, path_resized_img)
            imageThumb(path_resized_img, size_array[0], size_array[1])

        # Переписываем параметры функции
        img_name = '%s_%s' % (size, img_name)
        # Переписываем рабочую папку
        source = os.path.join(source, folder)
    else:
        result = os.path.join(source, folder, 'watermark_%s' % img_name)
        # Если уже есть вотермарка
        if not check_path(result):
            return '/media/%s' % result

    import Image

    img_path = full_path(os.path.join(source, img_name))
    if not check_path(img_path):
        im = Image.open(img_path)
    else:
        return UPS_PATH

    mark = Image.open(full_path(mark))
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
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
    return '/media/%s' % result

@register.simple_tag
def translit_tag(text: str):
  """Транслит
     :param text: текст"""
  return translit(text)

@register.simple_tag
def monthy(date, rp: bool = 1, socr: bool = None):
  """Месяц из цифр прописью
     :param date: дата
     :param rp: родительный падеж
     :param socr: сокращенно месяц"""
  return monthToStr(date, rp, socr)

@register.simple_tag
def weekly(date, rp: bool = None, socr:bool = None):
  """День недели прописью
     :param date: дата
     :param rp: родительный падеж
     :param socr: сокращенно день недели"""
  return weekdayToStr(date, rp, socr)

@register.filter(name='money_format')
def money_format(summa):
    """Визуальное разделение цифр в сумме по 3
       :param summa: сумма"""
    return summa_format(summa)

@register.filter(name='kopeiko_killer')
def kopeiko_killer(summa: float):
    """Удаление нулевых копеек из суммы
     :param summa: сумма"""
    if summa:
        summa = '%s' % summa
        if summa.endswith('.00'):
            summa = summa_format(summa[:-3])
        else:
            summa = summa_format(summa)
    return summa

@register.filter(name='assembleby')
def assembleby(items: list, count: int = 4):
    """Распределить блоки по контейнерам с n-элементов
       Например, надо вывести контейнеры,
       в каждом по 4 элемента (count = 4)
       :param items: блоки
       :param count: количество блоков в каждом контейнере
    """
    if not items:
        return {}
    result = {}
    i = 0
    j = 0
    result[i] = []
    for item in items:
        if j < count:
            j += 1
        else:
            j = 1
            i += 1
            result[i] = []
        result[i].append(item)
    return result.values()

@register.filter(name='divide')
def divide(items: list, count: int = 2):
    """Разбить блоки на n-контейнеров
       Например, надо вывести 3 контейнера с
       равным кол-вом блоков
       :param items: блоки
       :param count: количество блоков в каждом контейнере
    """
    if not items:
        return []
    result = []
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

@register.filter(name='accumulate')
def accumulate(blocks: list):
    """Собрать подблоки из разных блоков в один контейнер
       Например, надо подготовить из 10 блоков список,
       который затем сделаем assembleby и будем
       выводить по n-элементов
       Работаем с sub в каждом блоке
       :param blocks: блоки
    """
    container = []
    for block in blocks:
        if hasattr(block, 'sub'):
            for item in block.sub:
                # Сохраняем информацию о родительском блоке
                # иначе не сможем, например, отфильтровать по parent
                item.parent = block
                container.append(item)
    return container

@register.filter(name='pass_by_tag')
def pass_by_tag(blocks: list, tag: str = None):
    """Пропускать блоки по тегу/без тега
       Если тег не указан, пропускаем с любым тегом
       :param blocks: блоки
       :param tag: тег
    """
    container = []
    for block in blocks:
        if hasattr(block, 'tag'):
            if not tag:
                if block.tag:
                    container.append(block)
            else:
                if not block.tag == tag:
                    container.append(block)
    return container

@register.filter(name='reverse')
def reverse(blocks):
    """Инвертировать список блоков
       И последние станут первыми
       :param blocks: блоки"""
    if not blocks:
        return []
    return blocks[::-1]

@register.filter(name='sortedby')
def sortedby(blocks: list, field: str):
    """Сортировка блоков
       :param blocks: блоки
       :param field: поле по которому делаем сортировку"""
    if not blocks or not field:
        return []
    if hasattr(blocks[0], field):
        key = lambda x: getattr(x, field)
        reverse = True if '-' in field else False
        return sorted(blocks, key=key, reverse=reverse)
    return blocks
