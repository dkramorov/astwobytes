#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#################################################
# Dependencies:
# MAKE need g++ (c++ compiler)
# zlib1g-dev
# uuid-dev
# python-dev (for bindings)
#################################################

import os, sys

gmake = 'make'
arch = '.tar.gz'
xapian_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.split(xapian_path)[0]
xapian_core = 'xapian-core-1.4.15'
xapian_core_path = os.path.join(xapian_path, xapian_core)
xapian_bindings = 'xapian-bindings-1.4.15'
xapian_bindings_path = os.path.join(xapian_path, xapian_bindings)
hunspell = 'hunspell-1.2.15'
hunspell_path = os.path.join(xapian_path, hunspell)
hunspell_bindings = 'hunspell-0.3.5'
hunspell_bindings_path = os.path.join(xapian_path, hunspell_bindings)
cpulimit = 'cpulimit-1.1'
cpulimit_path = os.path.join(xapian_path, cpulimit)

def extract_archs():
    """Распаковка архивов"""
    for item in (xapian_core, xapian_bindings, hunspell, hunspell_bindings):
        path = '%s%s' % (item, arch)
        os.system('tar -xf %s' % path)

def xcore():
    """Уставновка ксапиана"""
    os.system('cd %s && ./configure --prefix=%s' % (xapian_core_path, xapian_path))
    os.system('cd %s && %s' % (xapian_core_path, gmake))
    os.system('cd %s && %s install' % (xapian_core_path, gmake))

def xbindings():
    """Установка биндингов
       для python3 требуется python3-sphinx
       pip install sphinx
       после этого поедет сборка
    """
    os.system("cd %s && ./configure --with-python3 --prefix=%s XAPIAN_CONFIG=%s/bin/xapian-config PYTHON_LIB=%s/site-packages" % (xapian_bindings_path, xapian_path, xapian_path, xapian_path))
    os.system("cd %s && %s" % (xapian_bindings_path, gmake))
    os.system("cd %s && %s install" % (xapian_bindings_path, gmake))

def xhunspell():
    """Установка hunspell"""
    os.system('cd %s && ./configure --prefix=%s' % (hunspell_path, xapian_path))
    os.system('cd '+hunspell_path+' && '+gmake)
    os.system('cd '+hunspell_path+' && '+gmake+' install && ldconfig')
    os.system('ln -s %s/lib/libhunspell-1.2.a %s/lib/libhunspell.a' % (xapian_path, xapian_path))
    os.system('chmod +x '+hunspell_bindings_path+'/setup.py')
    os.environ['LD_LIBRARY_PATH']=xapian_path+'/lib'
    os.system('cd %s && ./setup.py build_ext --include-dirs=%s/include/hunspell --library-dirs=%s/lib --build-lib=%s/lib --rpath=%s/lib' % (hunspell_bindings_path, xapian_path, xapian_path, xapian_path, xapian_path))

def xcpulimit():
    """Установка cpulimit"""
    os.system('cd %s && make' % cpulimit_path)

def drop_archs():
    """Удаление архивов"""
    for item in (xapian_core_path, xapian_bindings_path, hunspell_path, hunspell_bindings_path):
        os.system('rm -R %s' % item)

extract_archs()
xcore()
xbindings()
xhunspell()
#xcpulimit()
drop_archs()
