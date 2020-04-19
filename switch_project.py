#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import time

import logging

# defaults write com.apple.desktopservices DSDontWriteNetworkStores true

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info(__file__)

started = time.time()

project_name = 'greenfarm'
logger.info('Arguments: %s: %s', len(sys.argv), sys.argv)
if len(sys.argv) > 1:
    project_name = sys.argv[1]

root_dir = os.path.split(os.path.abspath(__file__))[0]
logger.info('root_dir: %s' % root_dir)

# -----------------------------
# Сайт на который переключаемся
# -----------------------------
sites = os.path.join(root_dir, 'SITES')
active_site = os.path.join(sites, project_name)
as_db = os.path.join(active_site, 'db.sql')
as_media = os.path.join(active_site, 'media')
as_my_cnf = os.path.join(active_site, 'my.cnf')
as_site = os.path.join(active_site, 'site')
as_env = os.path.join(active_site, '.env')
if not os.path.exists(as_db):
    logger.error('db not found: %s' % as_db)
    exit()
if not os.path.exists(as_media):
    logger.error('media not found: %s' % as_media)
    exit()
if not os.path.exists(as_my_cnf):
    logger.error('my.cnf not found: %s' % as_my_cnf)
    exit()
if not os.path.exists(as_site):
    logger.error('site not found: %s' % as_site)
    exit()
if not os.path.exists(as_env):
    logger.error('.env not found: %s' % as_env)
    exit()

# ------------
# Текущий сайт
# ------------
media = os.path.join(root_dir, 'media')
site = os.path.join(root_dir, 'apps', 'site')
my_cnf = os.path.join(root_dir, 'conf', 'my.cnf')
env = os.path.join(root_dir, 'conf', '.env')
logger.info('media: %s' % media)
logger.info('site: %s' % site)
logger.info('conf: %s' % my_cnf)
logger.info('.env: %s' % env)
if os.path.exists(media):
    if not os.path.islink(media):
        logger.error('media is not symlink')
        exit()
    else:
        os.unlink(media)
if os.path.exists(site):
    if not os.path.islink(site):
        logger.error('media is not symlink')
        exit()
    else:
        os.unlink(site)
if os.path.exists(my_cnf):
    if not os.path.islink(my_cnf):
        logger.error('media is not symlink')
        exit()
    else:
        os.unlink(my_cnf)
if os.path.exists(env):
    if not os.path.islink(env):
        logger.error('.env is not symlink')
        exit()
    else:
        os.unlink(env)

# -------------
# Переключаемся
# -------------
cmd = 'ln -s %s %s' % (as_media, media)
os.system(cmd)
logger.info(cmd)

cmd = 'ln -s %s %s' % (as_my_cnf, my_cnf)
os.system(cmd)
logger.info(cmd)

cmd = 'ln -s %s %s' % (as_site, site)
os.system(cmd)
logger.info(cmd)

cmd = 'ln -s %s %s' % (as_env, env)
os.system(cmd)
logger.info(cmd)