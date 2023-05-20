#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#################################################
# Dependencies:
# MAKE need g++ (c++ compiler)
# zlib1g-dev
# uuid-dev
# python-dev (for bindings)
#################################################


"""
M1 arm64 silicon

pip cache dir - чистим, ставим только arm64
/Users/jocker/Library/Caches/pip

https://xapian.org/download
macOS

Python 3.9.7 (default, Oct 12 2021, 22:38:23) 
[Clang 13.0.0 (clang-1300.0.29.3)] on darwin

xapian-bindings-1.4.18.tar.xz

Homebrew has xapian-core and the bindings for several languages packaged. For example, use
brew install --build-from-source xapian

error: Couldn't import sphinx module for Python3 - try package python3-sphinx
=>pip3 install sphinx

# Если поставить в систему, то все заработает,
# но после, мы будем компилить в папку
brew install --build-from-source xapian
Напишут
==> ./configure --prefix=/opt/homebrew/Cellar/xapian/1.4.18
==> make install
==> ./configure --prefix=/opt/homebrew/Cellar/xapian/1.4.18 --with-python3
==> make install
🍺  /opt/homebrew/Cellar/xapian/1.4.18: 584 files, 15.7MB, built in 51 seconds

# компилим биндинг для питон в папке
./configure --help
./configure --with-python3 --prefix=/Users/jocker/astwobytes/xapian64/xapian-bindings-1.4.18 XAPIAN_CONFIG=/opt/homebrew/Cellar/xapian/1.4.18/bin/xapian-config PYTHON3_LIB=/Users/jocker/astwobytes/xapian64/site-packages
make && make install

import xapian

# HUNSPELL WITH BINDINGS
brew install pkg-config
brew install --build-from-source hunspell
/opt/homebrew/Cellar/hunspell/1.7.0_2

/Users/jocker/astwobytes/xapian64/hunspell-0.3.5

cd /opt/homebrew/Cellar/hunspell/1.7.0_2/lib
(env) iMac:lib jocker$ ln -s libhunspell.dylib libhunspell-1.7.0.dylib
(env) iMac:lib jocker$ ln -s libhunspell-1.7.0.dylib libhunspell.dylib

./setup.py build_ext --build-lib=/Users/jocker/astwobytes/xapian64/lib --rpath=/Users/jocker/astwobytes/xapian64/lib --include-dirs=/opt/homebrew/Cellar/hunspell/1.7.0_2/include/hunspell --library-dirs=/opt/homebrew/Cellar/hunspell/1.7.0_2/lib

import hunspell

# hunspell.h для ubuntu - apt-get install libhunspell-dev

"""

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
       apt-get install python3-sphinx
       pip uninstall sphinx
       pip install sphinx
       после этого поедет сборка
    """
    os.system("cd %s && ./configure --with-python3 --prefix=%s XAPIAN_CONFIG=%s/bin/xapian-config PYTHON_LIB=%s/site-packages" % (xapian_bindings_path, xapian_path, xapian_path, xapian_path))
    os.system("cd %s && %s" % (xapian_bindings_path, gmake))
    os.system("cd %s && %s install" % (xapian_bindings_path, gmake))

def xhunspell():
    """Установка hunspell
       т/к мы в виртуальном окружении,
       apt install hunspell libhunspell-dev python3-hunspell
       затем через setup.py install
       TOOO: передалать на setup.py install
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
