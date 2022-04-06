#-*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import (
    search_process,
    get_platform,
    search_binary,
)
from apps.main_functions.files import (
    check_path,
    full_path,
    image_to_RGB,
    imageThumb,
    drop_folder,
    isForD,
    ListDir,
    extension,
    move_file,
    drop_file,
    file_size,
    copy_file,
)

logger = logging.getLogger('main')

FOLDERS_BLACK_LIST = (
    '.DS_Store',
)

class Optimizer:
    """Оптимизатор изображений
       USAGE:
       python manage.py clean_media --optimize_images --folder=flatcontent_blocks/43/ --compress=1 --chown
    """
    profit = 0
    platform = None
    jpegtran = None
    jpegoptim = None
    pngquant = None
    optipng = None

def drop_if_empty(folder: str = ''):
    """Удалить папку если она пустая
       :param folder: папка
    """
    items = ListDir(folder)
    if not items:
        logger.info('[DROP because EMPTY]: %s' % folder)
        drop_folder(folder)
        return
    # Перебираем мусор
    for item in items:
        path = os.path.join(folder, item)
        if item in FOLDERS_BLACK_LIST:
            logger.info('[DROP from BLACK LIST]: %s' % path)
            drop_folder(path)
        else:
            if isForD(path) == 'folder':
                drop_if_empty(path)

def optimize_all_images(folder: str = settings.MEDIA_ROOT, compress: int = 90):
    """Скукожить пухлые картинки"""
    media = settings.MEDIA_ROOT
    dirs = ListDir(folder)
    print(len(dirs), 'total object')
    z = 0

    for item in dirs:
        # -----------------
        # Немного прогресса
        # -----------------
        z += 1
        if z % 50 == 0:
            print(z, 'of', len(dirs))

        cur_path = os.path.join(folder, item)
        print(cur_path)
        if isForD(cur_path) == 'file':
            ext = extension(cur_path)
            if not ext:
                continue

            if ext.lower() in ('.jpg', '.jpeg'):
                if folder.endswith('resized'):
                    drop_file(cur_path)
                    continue
                fsize_before = file_size(cur_path)/1024
                os.system('%s -optimize -copy none -progressive %s>%s' % (Optimizer.jpegtran, cur_path, cur_path + '_'))
                move_file(cur_path + '_', cur_path)
                fsize_after = file_size(cur_path)/1024
                Optimizer.profit += fsize_before - fsize_after
                # -------------------------------
                # Дополнительная lose оптимизация
                # -------------------------------
                # jpegoptim --size=50% 24.JPG
                # jpegoptim -m90 24.JPG => (for linux)
                if compress:
                    copy_file(cur_path, cur_path + '_')
                    cmd = '%s -m%s %s' % (Optimizer.jpegoptim, compress, cur_path + '_')
                    if Optimizer.platform == 'mac':
                        cmd = '%s --size=%s%s %s' % (Optimizer.jpegoptim, compress, '%', cur_path + '_')
                    os.system(cmd)
                    fsize_after_trim = file_size(cur_path + '_')/1024
                    move_file(cur_path + '_', cur_path)
                    Optimizer.profit += fsize_after - fsize_after_trim
                    print('[COMPRESS]:', cur_path.replace(media, ''), 'before=>', fsize_after, 'Kb, fsize_after_trim=>', fsize_after_trim, 'Kb')
                else:
                    print(cur_path.replace(media, ''), 'before=>', fsize_before, 'Kb, fsize_after=>', fsize_after, 'Kb')
            elif ext.lower() in ('.png', ):
                if folder.endswith('resized'):
                    drop_file(cur_path)
                    continue
                fsize_before = file_size(cur_path)/1024
                os.system('%s -quiet -o 7 %s' % (Optimizer.optipng, cur_path))
                fsize_after = file_size(cur_path)/1024
                Optimizer.profit += fsize_before - fsize_after
                # -------------------------------
                # Дополнительная lose оптимизация
                # -------------------------------
                # pngquant -f --ext .png --quality 70-95 image.png
                if compress:
                    copy_file(cur_path, cur_path+"_")
                    cmd = '%s --force --ext .png --quality %s-100 %s' % (Optimizer.pngquant, compress, cur_path + '_')
                    #if Optimizer.platform == 'mac':
                        #cmd = '%s --size=%s%s %s' % (Optimizer.jpegoptim, compress, "%", cur_path+"_")
                    print(cmd)
                    os.system(cmd)
                    fsize_after_trim = file_size(cur_path + '_')/1024
                    move_file(cur_path+"_", cur_path)
                    Optimizer.profit += fsize_after - fsize_after_trim
                    print('[COMPRESS]:', cur_path.replace(media, ''), 'before=>', fsize_after, 'Kb, fsize_after_trim=>', fsize_after_trim, 'Kb')
                    ###exit()
                else:
                    print(cur_path.replace(media, ''), 'before=>', fsize_before, 'Kb, fsize_after=>', fsize_after, 'Kb')
        elif isForD(cur_path) == 'dir':
            optimize_all_images(folder=cur_path, compress=compress)

class Command(BaseCommand):
    """Почистить папку media"""
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--drop_empty_folders',
            action = 'store_true',
            dest = 'drop_empty_folders',
            default = False,
            help = 'Drop empty folders')
        parser.add_argument('--drop_pyc',
            action = 'store_true',
            dest = 'drop_pyc',
            default = False,
            help = 'Drop pyc files')
        parser.add_argument('--optimize_images',
            action = 'store_true',
            dest = 'optimize_images',
            default = False,
            help = 'Optimize images')
        parser.add_argument('--compress',
            action = 'store',
            dest = 'compress',
            type = str,
            default = False,
            help = 'Set compress ratio for optimize images')
        parser.add_argument('--folder',
            action = 'store',
            dest = 'folder',
            type = str,
            default = False,
            help = 'Set folder for optimize images')
        parser.add_argument('--chown',
            action = 'store_true',
            dest = 'chown',
            default = False,
            help = 'Set chown after operation')

    def handle(self, *args, **options):

        is_running = search_process(q = ('clean_media', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        if options.get('drop_empty_folders'):
            drop_if_empty()

        if options.get('drop_pyc'):
            os.system('find %s -name "*.pyc" -exec rm -f {} \;' % (settings.BASE_DIR, ))
            os.system('find %s -name ".DS_Store" -exec rm -f {} \;' % (settings.BASE_DIR, ))
            os.system('find %s -name __pycache__ -exec rmdir {} \+' % (settings.BASE_DIR, ))

        if options.get('optimize_images'):
            """оптимизация jpeg изображений"""
            Optimizer.platform = get_platform()
            print('platform is', Optimizer.platform)

            compress = None
            media = settings.MEDIA_ROOT
            if options.get('folder'):
                folder = options['folder']
                if not folder.startswith('/'):
                    media = os.path.join(media, folder)
            if options.get('compress'):
                try:
                    compress = int(options['compress'])
                except ValueError:
                    compress = None
            if compress:
                if compress < 60:
                    compress = 60
                    print('[WARN]: sorry, you set quality lower than 60%, we re-set it to 60%')

            # -------------------------
            # Сжатие с потерей качества
            # -------------------------
            Optimizer.jpegoptim = search_binary('jpegoptim')
            if not Optimizer.jpegoptim:
                print('[ERROR]: jpegoptim not found')
                exit()
            Optimizer.pngquant = search_binary('pngquant')
            if not Optimizer.pngquant:
                print('[ERROR]: pngquant not found')
                exit()
            # --------------------------
            # Сжатие без потери качества
            # --------------------------
            Optimizer.jpegtran = search_binary('jpegtran')
            if not Optimizer.jpegtran:
                print('[ERROR]: jpegtran not found')
                exit()
            Optimizer.optipng = search_binary('optipng')
            if not Optimizer.optipng:
                print('[ERROR]: optipng not found')
                exit()

            # -----------------------------------------
            # imga = full_path("imga.png")
            # os.system("%s %s" % (optipng, imga))
            # -----------------------------------------
            optimize_all_images(folder=media, compress=compress)
            print('[PROFIT]:', Optimizer.profit, 'Kb')
            if options.get('chown'):
                chown = search_binary('chown')
                os.system('%s -R www-data:www-data %s' % (chown, media))
