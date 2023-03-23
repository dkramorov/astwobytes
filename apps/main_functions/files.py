# -*- coding:utf-8 -*-
import requests
import logging
import datetime
import os
import re
import shutil
import time
import random
import traceback

from PIL import Image, ImageEnhance, ImageDraw, ImageFont

from django.conf import settings

logger = logging.getLogger('main')
# Попробовать подзаглушить логи для PIL,
# а то сыпет своими STREAM b'IHDR' 16 13
# STREAM b'IDAT' 41 8192 - подзаебал уже
#pil_logger = logging.getLogger('PIL')
#pil_logger.setLevel(logging.INFO)

DEFAULT_FOLDER = settings.MEDIA_ROOT

def image_size(img_name, path):
    """Открываем изображение и узнаем размер"""
    try:
        img = Image.open(os.path.join(DEFAULT_FOLDER, path, img_name))
    except IOError:
        return None
    return img.size

def unzip(fname: str, folder: str, pref: str = '', z: int = 0):
    """Функция распаковки из zip
    z - счетчик (имя файла), pref - префикс (временное имя файла)"""
    import zipfile
    rega_eng = re.compile('[^0-9a-z\.-]+', re.I+re.U+re.DOTALL)
    fname = os.path.join(DEFAULT_FOLDER, fname) # zip
    folder = os.path.join(DEFAULT_FOLDER, folder)  # folder
    if not folder.startswith(DEFAULT_FOLDER):
        return []
    make_folder(folder)
    items = []
    if zipfile.is_zipfile(fname):
        with zipfile.ZipFile(fname, 'r') as archive:
            names = archive.namelist()
            for name in names:
                if name.endswith('/'): # Директория
                    continue
                ext = name.split('.')[-1]

                cur_name = name.split('/')[-1]
                cur_name = '%s___%s' % (z, rega_eng.sub('-', cur_name))
                #cur_name = '%s%s.%s' % (z, pref, ext) # Новое имя файла
                #cur_name = '%s-%s.%s' % (name, z, ext) # Новое имя файла
                dest = os.path.join(folder, cur_name)
                outfile = open(dest, 'wb+')
                outfile.write(archive.read(name))
                outfile.close()
                items.append(cur_name)
                z += 1
    return items

def docx2html(path: str):
    """Конвертация docx в html
       :param path: путь к docx файлам
    """
    import mammoth
    if check_path(path):
        return
    path = os.path.join(DEFAULT_FOLDER, path)
    if not path.startswith(DEFAULT_FOLDER):
        return
    files = ListDir(path)
    for item in files:
        cur_item = os.path.join(path, item)
        if not item.endswith('.docx'):
            drop_file(cur_item)
            continue
        with open(full_path(cur_item), 'rb') as docx_file:
            try:
                result = mammoth.convert_to_html(docx_file)
            except Exception as e:
                drop_file(cur_item)
                logger.info('[ERROR]: %s' % e)
                continue
            html = result.value
            #messages = result.messages
            dest = os.path.join(path, item.replace('.docx', '.html'))
            with open_file(dest, 'w+') as f:
                f.write(html)
            drop_file(cur_item)

def copy_file(fname, dest):
    """Функция копирования файла"""
    fname = os.path.join(DEFAULT_FOLDER, fname)
    dest = os.path.join(DEFAULT_FOLDER, dest)
    if not dest.startswith(DEFAULT_FOLDER):
        return False
    # Перед копированием, убедимся, что папка есть
    dest_folder = os.path.split(dest)[0]
    if dest_folder:
        make_folder(dest_folder)
    try:
        shutil.copy2(fname, dest)
    except Exception:
        logger.exception('copy_file from %s to %s failed' % (fname, dest))
        return False
    return True

def copy_folder(fname, dest):
    """Функция копирования папки РЕКУРСИЯ"""
    if check_path(dest):
        make_folder(dest)
    if isForD(fname) == 'dir' and isForD(dest) == 'dir':
        content = ListDir(fname)
        for item in content:
            cur_path = os.path.join(fname, item)
            if isForD(cur_path) == 'file':
                copy_file(cur_path, dest)
            if isForD(cur_path) == 'dir':
                new_dest = os.path.join(dest, item)
                make_folder(new_dest)
                copy_folder(cur_path, new_dest)

def move_file(fname, dest):
    """Функция переноса"""
    fname = os.path.join(DEFAULT_FOLDER, fname)
    dest = os.path.join(DEFAULT_FOLDER, dest)
    if not dest.startswith(DEFAULT_FOLDER):
        return 0
    try:
        shutil.move(fname, dest)
        return 1
    except:
        return 0

def open_file(fname, mode: str = 'rb', encoding: str = 'utf-8'):
    """Функция открытия файла, после использования надо f.close()
       :param fname: имя файла (или относительный путь)
       :param mode: режим открытия (r/w)
       :param encoding: кодировка
    """
    modes = ['r', 'r+', 'rb', 'rb+', 'w', 'w+', 'wb', 'wb+', 'a', 'ab', 'a+', 'ab+']
    path = os.path.join(DEFAULT_FOLDER, fname)
    if not mode in modes:
        mode = 'rb'
    kwargs = {}
    if not 'b' in mode:
        kwargs['encoding'] = encoding
    try:
        f = open(path, mode, **kwargs)
    except IOError:
        return 0
    return f

def image_to_RGB(fname):
    """Функция конвертирования изображения в RGB
       Полезно, при ошибке IOError: cannot write mode P as JPEG
       обычно на gif изображениях"""
    path = os.path.join(DEFAULT_FOLDER, fname)
    if not path.startswith(DEFAULT_FOLDER):
        return False
    try:
        f = Image.open(path)
    except IOError:
        return False
    # Может возникать ошибка IOError: image file is truncated (10 bytes not processed), но после работа ведется с кэшированным изображением
    try:
        f.load() # Прогоняем вхолостую
    except IOError:
        pass
    newf = f.convert('RGB')
    newf.save(path)
    return True

def imageThumb(img, *args):
    """Функция создания уменьшенной копии изображения
     img - путь к изображению"""
    if img.endswith('.svg'):
        return True
    width = 800
    height = 800
    if args:
        try:
            width = int(args[0])
        except ValueError:
            pass
        try:
            height = int(args[1])
        except ValueError:
            pass
    size = width, height
    our_img = os.path.join(DEFAULT_FOLDER, img)
    if not our_img.startswith(DEFAULT_FOLDER):
        return False
    try:
        im = Image.open(our_img)
    except IOError:
        drop_file(our_img)
        return False
    if im.mode == 'RGBA':
        if img[-3:].lower() == 'jpg':
            im = im.convert('RGB')
    original_width, original_height = im.size
    # --------------------------------------------
    # Масштабируем только если размеры изображения
    # превышают те, что мы взяли за максимум
    # --------------------------------------------
    if original_width > width or original_height > height:
        try:
            im.thumbnail(size, Image.ANTIALIAS)
        except IOError:
            drop_file(our_img)
            return False
        try:
            im.save(our_img)
        except IOError:
            logger.info('NOTHING HELP, removing img %s, mode %s' % (our_img, im.mode))
            drop_file(our_img)
            return False
    return True

def imageResize(img: str, min_size: int = 800, new_name_prefix: str = 'resized_'):
    """Изменение размеров изображения пропорционально
       1) Находим соотношение
           max_size - 100%
           other    - x
           ratio = 100 * other / max_size
       2) БОльшую сторону рассчитываем добавлением соотношения
           max_size - 100%
           x        - ratio
           diff = max_size * ratio / 100
           other_side = max_size + diff
       3) проверяем снова находя соотношение между вычисленными сторонами
       :param img: путь к изображению
       :param min_size: минимальная сторона (не важно ширина или высота)
       :param new_name_prefix: префикс для имени файла масштабированного изображения
    """
    if img.endswith(".svg"):
        return True
    our_img = os.path.join(DEFAULT_FOLDER, img)
    if not our_img.startswith(DEFAULT_FOLDER):
        return False
    try:
        im = Image.open(our_img)
    except IOError:
        traceback.print_exc()
        return False

    original_width, original_height = im.size
    if original_width > original_height:
        height = min_size
        ratio = original_height * 100 / original_width
        diff = height * ratio / 100
        width = height + diff
    elif original_width < original_height:
        width = min_size
        ratio = original_width * 100 / original_height
        diff = width * ratio / 100
        height = width + diff
    else:
        width = height = min_size
    try:
        width = int(width)
        height = int(height)
        resized = im.resize((width, height), Image.ANTIALIAS)
        folder, fname = os.path.split(our_img)
        dest = os.path.join(folder, '%s%s' % (new_name_prefix, fname))
        resized.save(dest)
        return True
    except Exception:
        traceback.print_exc()
    return False

def reduce_opacity(im, opacity: float):
    """Возвращает изображение с пониженной прозрачностью,
       например, для вотермарки
       :param im: открытое Image по полному пути
       :param opacity: значение прозрачности
    """
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def blank_image(size: str = '150x150', color: list = (200, 200, 200)):
    """Создание пустого изображения
       :param size: размер изображения
       :param color: цвет изображения
       :return img: изображение,
                    которое можно .save(path) или юзнуть
    """
    size = size.split('x')
    size = (int(size[0]), int(size[1]))
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    img.paste(color, [0, 0, img.size[0], img.size[1]])
    #img.save(full_path('test.png'))
    return img

def watermark_image(img_name: str,
              source: str,
              size: str = '',
              mark: str = 'img/apple-touch-icon-114.png',
              position: str = 'tile',
              opacity: float = 0.1,
              folder: str = 'resized',
              rotate: int = None, ):
    """Вотермарка
       :param img_name: Путь до изображения, например, logos/1.png
       :param source: папка исходной картинки
       :param size: размер, например 150x150
       :param mark: оверлей-watermark (логотип)
       :param position: позиция вотермарки (tile/scale)
       :param opacity: значение прозрачности
       :param folder: папка, куда сохранить результат
       :param rotate: угол поворота вотермарки
    """
    UPS_PATH = '/static/img/ups.png'
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
                if rotate:
                    mark = mark.rotate(rotate)
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        if rotate:
            mark = mark.rotate(rotate)
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        if rotate:
            mark = mark.rotate(rotate)
        layer.paste(mark, position)

    # composite the watermark with the layer
    img = Image.composite(layer, im, layer)
    img.save(full_path(result))
    return '/media/%s' % result

def catch_file(f, path):
    """Сохраняем файл f в путь path
       :param f: FILES['file']
       :param path: относительный путь к файлу
    """
    destination = open_file(path ,'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return 1

def check_path(fname):
    """Проверяем есть ли такой путь"""
    path = os.path.join(DEFAULT_FOLDER, fname)
    if not os.path.exists(path):
        return 1
    return 0

def drop_file(fname):
    """Удаляем файл"""
    path = os.path.join(DEFAULT_FOLDER, fname)
    if not path.startswith(DEFAULT_FOLDER):
        return 0
    try:
        os.unlink(path)
        return 1
    except:
        return 0

def drop_folder(fname):
    """Удаляем каталог"""
    path = os.path.join(DEFAULT_FOLDER, fname)
    if not path.startswith(DEFAULT_FOLDER):
        return 0
    if path.endswith('media/') or path.endswith('media'):
        assert False
    try:
        shutil.rmtree(path)
        return 1
    except:
        return 0

def make_folder(fname):
    """Создаем каталог"""
    path = os.path.join(DEFAULT_FOLDER, fname)
    if not path.startswith(DEFAULT_FOLDER):
        return 0
    # Проверяем - возможно надо создать структуру
    if '/' in fname:
        if fname.startswith(DEFAULT_FOLDER):
            fname = fname.replace(DEFAULT_FOLDER, '').lstrip('/')
        fname_array = fname.split('/')
        middle_folder = ''
        for item in fname_array:
            if item:
                middle_folder = os.path.join(middle_folder, item)
                if check_path(middle_folder):
                    # Нету такой папки
                    if not full_path(middle_folder).startswith(DEFAULT_FOLDER):
                        return 0
                    try:
                        os.umask(0)
                        os.mkdir(full_path(middle_folder))
                    except:
                        logger.error('can not make folder %s' % (middle_folder, ))
                        return 0
        return 1
    try:
        os.umask(0)
        os.mkdir(path)
        return 1
    except:
        return 0

def extension(fname, mime='image'):
    """Узнаем расширение
       :param fname: имя файла изображения
       :param mime: указываем миме тип
    """
    result = None
    if not '.' in fname:
        return result
    part = fname.rsplit('.', 1)[-1]
    if 'image' in mime:
        if part in ('jpg', 'jpeg', 'gif', 'png', 'bmp', 'svg'):
            result = '.%s' % part
    elif 'flash' in mime:
        if part in ('swf', 'flv'):
            result = '.%s' % part
    elif 'movie' in mime:
        if part in ('mp4', ):
            result = '.%s' % part
    elif 'excel' in mime:
        if part in ('xls', 'csv', 'xlsx'):
            result = '.%s' % part
    elif 'xml' in mime:
        if part in ('xml', 'yml', 'yaml'):
            result = '.%s' % part
    elif mime == 'any':
        result = '.%s' % part
    return result

def ListDir(path, ignore_default_folder=False):
    """Список папок и файлов
       :param path: путь
       :param ignore_default_folder: если надо список не в media
    """
    path = os.path.join(DEFAULT_FOLDER, path)
    if not path.startswith(DEFAULT_FOLDER) and not ignore_default_folder:
        return []
    dirs = []
    try:
        dirs = os.listdir(path)
    except OSError:
        pass
    return dirs

def isForD(path):
    """Проверка пути - файл это или папка
       :param path: путь
    """
    path = os.path.join(DEFAULT_FOLDER, path)
    if os.path.isdir(path):
        return 'dir'
    if os.path.isfile(path):
        return 'file'
    return None

def convert_file(source, dest, cfrom='cp1251', cto='utf-8'):
    """Конвертирование файла из одной кодировы в другую
     (нужно при загрузке csv)
     source может быть равно dest"""
    doCoding = 0
    tmp_name = str(time.time()).split('.')[0] + '.txt'
    tmp_folder = os.path.split(source)[0] # узнаем папку (отсекая файл)
    tmp_name = os.path.join(tmp_folder, tmp_name)

    # Открываем файл
    f = open_file(source)
    while 1:
        content = f.readline()
        try:
            content = unicode(content, "utf-8")
        except UnicodeDecodeError:
            # Файл не в utf-8
            doCoding = 1
            break
        if not content:
            return source # Возвращем путь source - кодировка utf-8

    f.seek(0) # Перемещаемся в начало
    if doCoding == 1:
        out = open_file(tmp_name, "wb+")   # В папке назначения создаем временный файл
        # Надо перекодировать
        while 1:
            content = f.readline()
            try:
                content = unicode(content, "cp1251")
            except UnicodeDecodeError:
                return 0 # нифига не cp1251 и не utf-8
            # Пишем в новой кодировке в файл
            out.write(content.encode("utf-8"))
            if not content:
                break
        out.close()
    f.close()
    drop_file(source)
    move_file(tmp_name, source)
    return source

def upload_image(image, path, img_name=None):
    """Загрузка изображения в папку path
     image - файл, path - куда ложим,
     img_name - айдишник без расширения"""
    # Проверяем папку, куда загружаем
    if check_path(path):
        make_folder(path)
    # Проверяем расширение файла
    ext = extension(image.name, 'image/flash')
    # Хаваем файл
    if ext:
        if not img_name:
            img_name = str(time.time()).replace('.', '_')
        img_name = img_name + ext
        catch_file(image, os.path.join(path, img_name))
        return img_name
    return 0

def get_fname_from_url(urla):
    """Достаем имя файла и расширение из ссылки"""
    ext = ''
    fname = urla
    if '#' in fname:
        fname = fname.split('#')[0]
    if '?' in fname:
        fname = fname.split('?')[0]
    if '//' in fname:
        fname = fname.split('//')[1]
    if '/' in fname:
        fname = fname.split('/')[-1]
    if '.' in fname:
        fname, ext = fname.rsplit('.', 1)
    if not ext:
        fname = 'undefined'
        ext = 'jpg'
    return (fname, ext)

def grab_image_by_url(url, dest, name=None):
    """Вытащить картинку по URL и сохранить
       url - полный веб-адрес картинки
       dest - папка для сохранения
       name - новое имя картинки"""
    if not 'http' in url:
        return None
    # -----------------
    # Проверка на папку
    # -----------------
    if check_path(dest):
        make_folder(dest)

    img_name, ext = get_fname_from_url(url)
    img = '%s.%s' % (img_name, ext)
    if name:
        img = name
        if not img.endswith(ext):
            img = '%s.%s' % (img, ext)

    fname = os.path.join(dest, img)
    fname_path = full_path(fname)

    if not fname_path:
        return None

    # CertificateError: hostname '...:443' doesn't match '...'
    # You can avoid this error by monkey patching ssl:
    #import ssl
    #ssl.match_hostname = lambda cert, hostname: True

    #r = requests.get(url, verify = False)
    r = requests.get(url)
    if r.status_code == 200:
        with open(fname_path, 'wb+') as f:
            for chunk in r:
                f.write(chunk)
        return img
    return None

def full_path(path):
    """Возвращает абсолютный путь к файлу (/home/...)"""
    if not path:
        return ''
    if path.startswith('/media/'):
        path = path.replace('/media/', '')
    path = os.path.join(DEFAULT_FOLDER, path)
    if not path.startswith(DEFAULT_FOLDER):
        return ''
    return path

def do_archive(source_dir, archive_name=None):
    """Do tar.gz archive"""
    import tarfile
    source_dir = os.path.join(DEFAULT_FOLDER, source_dir)
    if not source_dir.startswith(DEFAULT_FOLDER):
        return 0
    if not archive_name:
        archive_name = str(time.time()).replace('.', '_')
    archive_path = os.path.join(source_dir, archive_name)
    if not archive_path.startswith(DEFAULT_FOLDER):
        return 0
    content = ListDir(source_dir)
    tar = tarfile.open(archive_path + '.tar.gz', 'w:gz')

    for item in content:
        cur_file = os.path.join(source_dir, item)
        cur_type= isForD(cur_file)
        if cur_type == "file" or cur_type == "dir":
            tar.add(cur_file, arcname=item)

    tar.close()
    #shutil.make_archive(archive_path, "gztar", source_dir)
    return archive_name + '.tar.gz'

def extract_archive(archive):
    """Extract tar.gz archive
       распаковываем только файлы с указанным ext"""
    import tarfile
    tree = []
    archive = os.path.join(DEFAULT_FOLDER, archive)
    if not archive.startswith(DEFAULT_FOLDER):
        return 0
    path = os.path.abspath(os.path.dirname(archive))
    if tarfile.is_tarfile(archive):
        tar = tarfile.open(archive, 'r:gz')
        tar.extractall(path=path)
        tree = tar.getnames()
        tar.close()
        return tree
    return 0

def analyze_res_path(img, get_folder_path):
    """Разбираем путь по которому нам дали медиа файл
       :param img: путь к медиа файлу
       :param get_folder_path: результат get_folder()
    """
    if not img:
        return '/static/img/ups.png'
    if img.startswith('http'):
        return img
    if img.startswith('/media/'):
        return '%s%s' % (get_folder_path, img.replace('/media/', ''))
    if img.startswith('/'):
        return img[1:]
    return '%s%s' % (get_folder_path, img)

def imagine_image(img, size, source, dest='resized'):
    """Изменение размера изображения
       :param img: имя файла, например 1.jpg
       :param size: размер, например 150х150 x - разделитель
       :param source: папка с исходным изображением, например, logos или get_folder()
       :param dest: папка, куда будем складировать
    """
    # TODO: в settings положить путь к пустой картинке
    ups = '/static/img/ups.png'
    path_img = analyze_res_path(img, source)
    if path_img.startswith('/static/') or path_img.startswith('http'):
        return path_img
    if img.endswith('.svg'):
        return os.path.join('/media/', path_img)
    size_array = size.split('x')
    #path_img = os.path.join(source, img) # заменил на analyze_res_path
    if check_path(path_img):
        return ups
    dest = str(dest)
    path_resized = os.path.join(source, dest)
    if check_path(path_resized):
        make_folder(path_resized)
    path_resized_img =  os.path.join(path_resized, '%s_%s' % (size, img.split('/')[-1]))
    if check_path(path_resized_img):
        copy_file(path_img, path_resized_img)
        imageThumb(path_resized_img, size_array[0], size_array[1])
    path_resized_img = os.path.join('/media/', path_resized_img)
    return path_resized_img

def file_size(fname):
    """Размер файла
       :param fname: Путь до файла
       :return: размер в байтах
    """
    result = 0
    path = os.path.join(DEFAULT_FOLDER, fname)
    if not check_path(path):
        statinfo = os.stat(path)
        result = statinfo.st_size
    return result

def get_data_size(data):
    """Размер данных в байтах, например, для memcached"""
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
    try:
        import cPickle as pickle
    except ImportError:
        import pickle
    fp = StringIO()
    pickler = pickle.Pickler(fp, protocol=0)
    pickler.dump(data)
    val = fp.getvalue()
    return len(val)

def disk_usage(path, block_size='Mb'):
    """Использование диска
       USAGE: disk_usage("/", "Gb")"""
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    result = {'total':total, 'used':used, 'free':free}
    if block_size:
        result['block_size'] = block_size
        if block_size.lower() == 'mb':
            mb = 1024*1024
            result['free'] = free/mb
            result['total'] = total/mb
            result['used'] = used/mb
        elif block_size.lower() == 'gb':
            gb = 1024*1024*1024
            result['free'] = free/gb
            result['total'] = total/gb
            result['used'] = used/gb
        else:
            result['block_size'] = 'bytes'
    else:
        result['block_size'] = 'bytes'
    return result

def create_captcha(alphabet: list = None,
                   captcha_size: int = 4,
                   font: str = 'fonts/PerfoCone.ttf',
                   font_size: int = 26, ) -> [str, Image]:
    """Создание цифрового изображения,
       например, капчи
       :param alphabet: символы из которых будем делать капчу
       :param captcha_size: количество символов в изображении
       :param font: путь к шрифту в static
       :param font_size: размер шрифта
       :return [str, Image]: возвращаем сгенерированную строку и изображение
    """
    result = ''
    if not alphabet:
        alphabet = [i for i in range(10)]

    ypos = 10
    letter_width = 25 # надо высчитывать на основании шрифта и размера шрифта
    # из расчета на то, что каждый глиф 25 пихалей при 26 кеге
    img_size = [captcha_size * letter_width, 50]
    # create WHITE image
    img = Image.new('RGB', img_size, (255,255,255))

    # create a drawing object that is used to draw on the new image
    draw = ImageDraw.Draw(img)

    # text color
    color_black = (0,0,0)
    font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, font), font_size)

    alphabet_len = len(alphabet)
    for i in range(captcha_size):
        rand_int = random.randrange(0, alphabet_len)
        letter_pos = (i * letter_width, ypos) # TODO: в параметры
        letter = str(alphabet[rand_int])
        result += letter
        draw.text(letter_pos, letter, fill=color_black, font=font)
    del draw

    return [result, img]
