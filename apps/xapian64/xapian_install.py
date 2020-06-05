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
xapian_core = 'xapian-core-1.2.12'
xapian_core_path = os.path.join(xapian_path, xapian_core)
xapian_bindings = 'xapian-bindings-1.2.12'
xapian_bindings_path = os.path.join(xapian_path, xapian_bindings)
#xapian_omega = 'xapian-omega-1.2.10'
#xapian_omega_path = os.path.join(xapian_path, xapian_omega)
xapian_djapian = 'Djapian-2.3.1'
xapian_djapian_path = os.path.join(xapian_path, xapian_djapian)
hunspell = 'hunspell-1.2.15'
hunspell_path = os.path.join(xapian_path, hunspell)
hunspell_bindings = 'hunspell-0.1'
hunspell_bindings_path = os.path.join(xapian_path, hunspell_bindings)
cpulimit = 'cpulimit-1.1'
cpulimit_path = os.path.join(xapian_path, cpulimit)

def extract_archs():
    """Распаковка архивов"""
    for item in (xapian_core, xapian_bindings, xapian_djapian, hunspell, hunspell_bindings):
        path = '%s%s' % (item, arch)
        os.system('tar -xf %s' % path)

def xcore():
    """Уставновка ксапиана"""
    os.system('cd %s && ./configure --prefix=%s' % (xapian_core_path, xapian_path))
    os.system('cd %s && %s' % (xapian_core_path, gmake))
    os.system('cd %s && %s install' % (xapian_core_path, gmake))

def xbindings():
    """Установка биндингов"""
    os.system("cd %s && ./configure --prefix=%s --with-python XAPIAN_CONFIG=%s/bin/xapian-config PYTHON_LIB=%s/site-packages" % (xapian_bindings_path, xapian_path, xapian_path, xapian_path))
    os.system("cd %s && %s" % (xapian_bindings_path, gmake))
    os.system("cd %s && %s install" % (xapian_bindings_path, gmake))

def xdjapian():
    """Установка djapian"""
    os.system('chmod +x %s/setup.py' % xapian_djapian_path)
    os.system("cd %s && ./setup.py build --build-lib=%s/site-packages" % (xapian_djapian_path, xapian_path))

def xhunspell():
    """Установка hunspell"""
    os.system('cd %s && ./configure --prefix=%s' % (hunspell_path, xapian_path))
    os.system('cd '+hunspell_path+' && '+gmake)
    os.system('cd '+hunspell_path+' && '+gmake+' install')
    os.system('chmod +x '+hunspell_bindings_path+'/setup.py')
    os.environ['LD_LIBRARY_PATH']=xapian_path+'/lib'
    os.system('cd %s && ./setup.py build_ext --include-dirs=%s/include/hunspell --library-dirs=%s/lib --build-lib=%s/lib --rpath=%s/lib' % (hunspell_bindings_path, xapian_path, xapian_path, xapian_path, xapian_path))

def xcpulimit():
    """Установка cpulimit"""
    os.system('cd %s && make' % cpulimit_path)

def drop_archs():
    """Удаление архивов"""
    for item in (xapian_core_path, xapian_bindings_path, xapian_djapian_path, hunspell_path, hunspell_bindings_path):
        os.system('rm -R %s' % item)

extract_archs()
#xcore()
#xbindings()
#xdjapian()
#xhunspell()
#xcpulimit()
#drop_archs()
