# -*- coding:utf-8 -*-
import requests
import logging
import datetime
import os
import re
import shutil
import time

from PIL import Image

from django.conf import settings

logger = logging.getLogger(__name__)
DEFAULT_FOLDER = settings.MEDIA_ROOT

def image_size(img_name, path):
    """Открываем изображение и узнаем размер"""
    try:
        img = Image.open(os.path.join(DEFAULT_FOLDER, path, img_name))
    except IOError:
        return None
    return img.size


def unzip(fname, folder, pref='', z=0):
    """Функция распаковки изображений из zip
     z - счетчик (имя файла), pref - префикс (временное имя файла)"""
    import zipfile
    fname = os.path.join(DEFAULT_FOLDER, fname) # zip
    folder = os.path.join(DEFAULT_FOLDER, folder)  # folder
    if not folder.startswith(DEFAULT_FOLDER):
        return None
    if  zipfile.is_zipfile(fname):
        archive = zipfile.ZipFile(fname, 'r')
        names = archive.namelist()
        images = []
        for name in names:
            if name.endswith("/"): # Директория
              continue
            ext = extension(name)
            if ext:
                cur_name = str(z)+pref+ext # Новое имя файла
                outfile = open(os.path.join(folder, cur_name), 'wb')
                outfile.write(archive.read(name))
                outfile.close()
                images.append(cur_name)
                z = z + 1
        return images
    return None

def copy_file(fname, dest):
    """Функция копирования файла"""
    fname = os.path.join(DEFAULT_FOLDER, fname)
    dest = os.path.join(DEFAULT_FOLDER, dest)
    if not dest.startswith(DEFAULT_FOLDER):
        return False
    try:
        shutil.copy2(fname, dest)
    except:
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
    """Функция открытия файла, после использования надо f.close()"""
    path = os.path.join(DEFAULT_FOLDER, fname)
    if not mode in ['r', 'r+', 'rb', 'rb+', 'w', 'w+', 'wb', 'wb+', 'a', 'ab', 'a+', 'ab+']:
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
    #if not im.mode == "RGB":
        #im = im.convert("RGB")
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
            logger.error('NOTHING HELP, removing img %s, mode %s' % (our_img, im.mode))
            drop_file(our_img)
            return False
    return True

def catch_file(f, path):
    """Сохраняем файл f (FILES['file']) в полное имя"""
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
    if "/" in fname:
        fname_array = fname.split("/")
        middle_folder = ""
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
    """Узнаем расширение"""
    result = None
    if not '.' in fname:
        return result
    part = fname.rsplit('.', 1)[-1]
    if 'image' in mime:
        if part in ('jpg', 'jpeg', 'gif', 'png', 'bmp'):
            result = '.%s' % (part, )
    elif "flash" in mime:
        if part in ('swf', 'flv'):
            result = '.%s' % (part, )
    elif "movie" in mime:
        if part in ('mp4', ):
            result = '.%s' % (part, )
    elif "excel" in mime:
        if part in ('xls', 'csv', 'xlsx'):
            result = '.%s' % (part, )
    elif "xml" in mime:
        if part in ('xml', 'yml', 'yaml'):
            result = '.%s' % (part, )
    elif mime == "any":
        result = '.%s' % (part, )
    return result

def ListDir(path, ignore_default_folder=False):
    """Список папок и файлов"""
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
    """Проверка пути - файл это или папка"""
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

def imagine_image(img, size, source, dest='resized'):
    """img - имя файла, например 1.jpg
       size - размер, например 150х150 икс разделитель
       source - папка с исходным изображением, например, logos
       dest - папка, куда будем складировать
       масштабированные изображения, например id_parent"""
    ups = '/static/img/ups.png'
    dest = str(dest)
    size_array = size.split('x')
    path_img = os.path.join(source, img)
    if check_path(path_img):
        return ups
    path_resized = os.path.join(source, dest)
    if img.endswith('.svg'):
        return os.path.join("/media/", path_img)
    if check_path(path_resized):
        make_folder(path_resized)
    path_resized_img =  os.path.join(path_resized, size+"_"+img)
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
