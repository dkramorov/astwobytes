# -*- coding:utf-8 -*-
import os
import sys
import subprocess
import requests
import logging
import xml.sax

from zipfile import ZipFile
from envparse import env
env.read_envfile()
API_SERVER = env('API_SERVER')
API_TOKEN = env('API_TOKEN')
PLUGINS_FOLDER = os.path.split(os.path.abspath(__file__))[0]
ROOT_FOLDER = os.path.split(PLUGINS_FOLDER)[0]

logger = logging.getLogger(__file__)


class SeleniumVersionsHandler(xml.sax.ContentHandler):
    """Парсим имеющиеся версии selenium"""
    def __init__(self):
        self.TagListBucketResult = 'ListBucketResult'
        self.TagContents = 'Contents'
        self.TagKey = 'Key'
        self.isListBucketResult = False
        self.isContents = False
        self.isKey = False
        self.KeyValue = ''
        self.selenium_versions = []

    def startElement(self, tag, attributes):
        if tag == self.TagKey:
            self.isKey = True
        elif tag == self.TagContents:
            self.isContents = True
        elif tag == self.TagListBucketResult:
            self.isListBucketResult = True

    def endElement(self, tag):
        if tag == self.TagKey:
            self.isKey = False
            self.selenium_versions.append(self.KeyValue)
            self.KeyValue = ''
        elif tag == self.TagContents:
                self.isContents = False
        elif tag == self.TagListBucketResult:
            self.isListBucketResult = False

    def characters(self, content):
        if self.isKey:
            self.KeyValue += content


def update_robot_helper(folder: str, result: dict):
    """Помощник по обновленияю роботом самого себя
       :param folder: папка
       :param result: словарь с обновлениями
    """
    for key, value in result.items():
        if key.startswith('.'):
            continue
        dest = os.path.join(folder, key)
        if isinstance(value, str):
            with open(dest, 'w+', encoding='utf-8') as f:
                f.write(value)
        elif isinstance(value, dict):
            if not os.path.exists(dest):
                os.mkdir(dest)
            update_robot_helper(dest, value)


def update_robot(**kwargs):
    """Обновление самого себя
       kwargs['updater'] = True (себя/сырцы)
       kwargs['source'] = True (себя/сырцы)
       kwargs['selenium'] = True (селениум файл)
    """
    if not API_SERVER or not API_TOKEN:
        logger.info('API_SERVER / API_TOKEN not set')
        return
    updater_py = 'updater.py'
    headers = {'token': API_TOKEN}
    endpoint = '%s/robots/updater/' % API_SERVER.rstrip('/')
    try:
        r = requests.get(endpoint, params=kwargs, headers=headers)
        #print('[UPDATER]: %s => %s' % (r.status_code, r.text))
    except Exception as e:
        print(e)
        return
    resp = r.json()
    if kwargs.get('updater') == True or kwargs.get('source') == True:
        update_robot_helper(ROOT_FOLDER, resp)


def get_platform():
    """Определяем операционную систему"""
    platform = 'unknown'
    if 'darwin' in sys.platform:
        platform = 'mac'
    elif 'linux' in sys.platform:
        platform = 'linux'
    return platform


def get_chrome_version():
    """Узнаем версию chrome в системе
       Linux:
           google-chrome --product-version
           87.0.4280.88
       Mac OS:
           /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
           Google Chrome 85.0.4183.83
    """
    platform = get_platform()
    cmd = ['google-chrome', '--product-version']
    if platform == 'mac':
        cmd = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version']
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    version = result.stdout.decode('utf-8')
    versions = version.split(' ')
    for version in versions:
        if not '.' in version:
            continue
        v = version.split('.')[0]
        if v.isdigit():
            return v


def update_selenium():
    """Обновление исполняемого бинарника
       название файла выглядит примерно так
       90.0.4430.24/chromedriver_linux64.zip
    """
    xml_file = 'selenium_versions.xml'
    urla = 'https://chromedriver.storage.googleapis.com/'
    r = requests.get(urla)
    with open(xml_file, 'w+', encoding='utf-8') as f:
        f.write(r.text)
    parser = xml.sax.make_parser()
    handler = SeleniumVersionsHandler()
    parser.setContentHandler(handler)
    parser.parse(xml_file)
    versions = handler.selenium_versions
    platform = get_platform()
    chrome_version = get_chrome_version()
    selenium_versions = [version for version in versions if platform in version and chrome_version in version]
    if not selenium_versions:
        logger.info('Do not know which version is used')
        return
    selenium_version = selenium_versions[-1]
    ext = selenium_version.split('.')[-1]
    selenium_arhieve = '%s%s' % (urla, selenium_version)
    r = requests.get(selenium_arhieve)
    fname = '%s.%s' % (chrome_version, ext)
    dest = os.path.join(ROOT_FOLDER, fname)
    with open(dest, 'wb+') as f:
        f.write(r.content)
    with ZipFile(dest, 'r') as zip_obj:
        zip_obj.extractall('env/bin/')
    os.system('chmod +x env/bin/chromedriver')

if __name__ == '__main__':
    update_robot(updater=True, source=False, selenium=False)
    update_selenium()
