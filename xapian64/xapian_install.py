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
    """Уставновка xapian"""
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
    """Установка hunspell
       т/к мы в виртуальном окружении,
       TOO: передалать на setup.py install
    """
    os.system('cd %s && ./configure --prefix=%s' % (hunspell_path, xapian_path))
    os.system('cd '+hunspell_path+' && '+ gmake)
    os.system('cd '+hunspell_path+' && '+ gmake + ' install && ldconfig')
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
#xcore()
#xbindings()
#xhunspell()
#xcpulimit()
drop_archs()

"""
/usr/local/bin/virtualenv -p python3.7 env
source env/bin/activate
arch -x86_64 bash
cd /Users/jocker/astwobytes/xapian64
pip install sphinx
tar -xzf xapian-core-1.4.15.tar.gz && cd xapian-core-1.4.15
./configure --prefix=/Users/jocker/astwobytes/xapian64 && make && make install
cd ..
tar -xzf xapian-bindings-1.4.15.tar.gz && cd xapian-bindings-1.4.15
./configure --with-python3 --prefix=/Users/jocker/astwobytes/xapian64 XAPIAN_CONFIG=/Users/jocker/astwobytes/xapian64/bin/xapian-config PYTHON_LIB=/Users/jocker/astwobytes/xapian64/site-packages
make && make install

import xapian


arch -x86_64 bash
cd /Users/jocker/django/xapian64
tar -xzf xapian-core-1.2.12.tar.gz && cd xapian-core-1.2.12
./configure --prefix=/Users/jocker/django/xapian64 && make && make install
cd ..
tar -xzf xapian-bindings-1.2.12.tar.gz && cd xapian-bindings-1.2.12


Python2

arch -x86_64 /usr/local/bin/brew install xapian
Устанавливается в /usr/local/Cellar/xapian/1.4.18
arch -x86_64 /usr/local/bin/brew install sphinx-doc

arch -x86_64 /usr/local/bin/brew install virtualenv
/usr/local/Cellar/virtualenv/20.10.0/bin/virtualenv
/usr/local/Cellar/virtualenv/20.10.0/bin/virtualenv -p python2 env

./configure --prefix=/Users/jocker/django/xapian64 XAPIAN_CONFIG=/usr/local/Cellar/xapian/1.4.18/bin/xapian-config PYTHON_LIB=/Users/jocker/django/xapian64/site-packages --with-python
make && make install
"""
