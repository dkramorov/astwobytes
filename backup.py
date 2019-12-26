#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import time
import shutil
import logging

# defaults write com.apple.desktopservices DSDontWriteNetworkStores true

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info(__file__)

started = time.time()

dest = '/home/jocker/tmp'
# архивируем нужные папки
ignore_arr = ['dump.rdb', '.DS_Store', '.git', '*__pycache__*', '*.pyc']
sources = [
    {'path': '/home/jocker/astwobytes', 'exclude': ['env', 'media', 'packaging/django*']},
    {'path': '/home/jocker/nextgen', 'exclude': ['env', 'media']},
    {'path': '/home/jocker/selenium', 'exclude': ['env', 'profiles', '.pytest_cache', 'json_queries.json_back', 'yandex_clicks_count.txt']},
    {'path': '/home/jocker/django',
     'exclude': [
       'xapian/bin',
       'xapian/cpulimit-1.1',
       'xapian/include',
       'xapian/lib',
       'xapian/share',
       'xapian64/bin',
       'xapian64/cpulimit-1.1',
       'xapian64/include',
       'xapian64/lib',
       'xapian64/share',
       'SITES/*/djapian_base',
       'SITES/prostata',
       'SITES/pizzahot',
       'SITES/perestroika',
       'SITES/a223/media/products',
       'SITES/a223/media/xml_yml',
       'SITES/a223/media/user_files',
       'SITES/a223/media/flatcontent*',
       'SITES/a223/media/files_Files',
       'SITES/a223/media/app_json',
       'SITES/a223/media/app',
       'SITES/a223/media/afish*',
    ]},
]
# Пример архивирования
#tar -czf /home/jocker/tmp/astwobytes.tar.gz --exclude=/home/jocker/astwobytes/{env,dump.rdb,.git} /home/jocker/astwobytes
for source in sources:
    fname = source['path'].rsplit('/', 1)[-1]
    source['exclude'] += ignore_arr
    os.system('/usr/bin/tar -czf %s/%s.tar.gz --exclude=%s/{%s} %s' % (
        dest, fname, source['path'], ",".join(source['exclude']), source['path'])
    )




exit()




#yandex_disk = '/home/jocker/yandex_disk'
#if not os.path.exists(yandex_disk):
#    os.mkdir(yandex_disk)
#logger.info('--- mounting %s ---' % (yandex_disk, ))
#os.system('./backup_transport.sh %s' % (yandex_disk, ))

def copy_object(source, dest, buffer_size=1024*1024):
    """Copy object"""
    while True:
        copy_buffer = source.read(buffer_size)
        if not copy_buffer:
            break
        dest.write(copy_buffer)

for source in sources:
    fname = source['path'].rsplit('/', 1)[-1]
    archive_source = '%s/%s.tar.gz' % (dest, fname)
    #archive_dest = '%s/%s.tar.gz' % (yandex_disk, fname)
    #logger.info('%s => %s' % (archive_source, archive_dest))

    # curl
    os.system('curl --user kimadav@yandex.ru:rbvflfd -T "%s" https://webdav.yandex.ru/' % (archive_source, ))

    # shutil.copyfile
    #try:
    #    shutil.copyfile(archive_source, archive_dest)
    #    logger.info('copied %s to %s' % (archive_source, archive_dest))
    #except Exception as e:
    #    logger.error('[ERROR]: %s' % (e, ))

    # system cp
    #os.system('/bin/cp %s %s' % (archive_source, archive_dest))

    # steam copy
    #try:
    #    with open(archive_source, 'rb') as s, open(archive_dest, 'wb+') as d:
    #        copy_object(s, d)
    #except Exception as e:
    #    logger.error(e)

#os.system('/sbin/umount %s' % (yandex_disk, ))
#if os.path.exists(yandex_disk):
#    os.rmdir(yandex_disk)

elapsed = time.time() - started
logger.info('[ELAPSED]: %.2f' % (elapsed, ))

