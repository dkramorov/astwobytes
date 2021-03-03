# -*- coding: utf-8 -*-
import time
import re
import os
import requests
import logging
import urllib.parse

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import check_path, make_folder, drop_folder, open_file
from apps.main_functions.string_parser import kill_quotes

logger = logging.getLogger(__name__)

rega_img = re.compile("url\(([^\)]+)", re.I+re.U+re.DOTALL)
#@import "css/main.css";
#@import"../plugin/bootstrap/css/bootstrap.min.css";
rega_import = re.compile("@import[\surl(\"']+([^\"';]+)", re.I+re.U+re.DOTALL)
root_path = 'new_template'

# 1) https://demo.hasthemes.com/greenfarm-preview/greenfarm/index-2.html

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--template',
            action = 'store',
            dest = 'template',
            type = str,
            default = False,
            help = 'Set template for grabbing')

    def handle(self, *args, **options):
        """Спистануть с темфореста шаблон
           example:
               https://demo.hasthemes.com/greenfarm-preview/greenfarm/index-2.html
        """
        template = options.get('template')
        if template:
            logger.info(template)
            t = Parser(template)
            t.create_structure()
            t.get_index_html()
            t.fix_links()
            t.get_misc_files()
            t.get_js_files()
            t.get_css_files()
        else:
            logger.info('Use --template=...')

# -----------------------------
# Класс для спижжувания шаблона
# -----------------------------
class Parser:
    def __init__(self, url_template: str,
                 template: str = 'new_template',
                 local_index: bool = False,
                 params: str = ''):
        """Инициализация класса
           :param url_template: какой шаблон тырим (полный путь к index)
           :param template: как называется шаблон (наша папка)
           :param local_index: если у нас уже есть локально index.html
           :param params: строка с гет параметрами
        """
        self.url_template = url_template
        self.template = template
        self.local_index = local_index
        self.with_params = params #with_params = "?q=123&w=321"

        self.session = requests.Session()
        ua = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
        self.session.headers.update({
            'User-Agent': ua,
            'Referer': self.url_template
        })
        #headers = {"X-Requested-With":"XMLHttpRequest"}

        self.themeforest = 'themeforest'
        self.css_files = []
        self.js_files = []
        self.img_files = []
        self.img_repeated = []

        self.z = 0

        self.base_path = None
        self.template_path = None
        self.css_path = None
        self.js_path = None
        self.img_path = None
        self.misc_path = None

        self.get_base_path()

    def clean_path(self, path):
        """Убираем ? и # из пути"""
        if '?' in path:
            path = path.split('?')[0]
        if '#' in path:
            path = path.split('#')[0]
        return path

    def get_base_path(self):
        """Базовый путь к шаблону"""
        self.base_path = self.clean_path(self.url_template)

        if self.base_path[-4:] in ('.php', 'html', '.htm'):
            self.base_path = '%s/' % os.path.split(self.base_path)[0]
        logger.info('Базовый путь к шаблону %s' % (self.base_path, ))

    def create_structure(self):
        """Создаем структуру"""
        make_folder(self.themeforest)
        self.template_path = '%s/%s' % (self.themeforest, self.template)
        self.css_path = os.path.join(self.template_path, 'css')
        self.js_path = os.path.join(self.template_path, 'js')
        self.img_path = os.path.join(self.template_path, 'img')
        self.misc_path = os.path.join(self.template_path, 'misc')

        drop_folder(self.css_path)
        drop_folder(self.js_path)
        drop_folder(self.img_path)
        drop_folder(self.misc_path)

        make_folder(self.css_path)
        make_folder(self.js_path)
        make_folder(self.img_path)
        make_folder(self.misc_path)

        # ------------------------------------------
        # Записать ссылку на источник, откуда тыбзим
        # ------------------------------------------
        reference = '%s/%s' % (self.template_path, 'reference.txt')
        with open_file(reference, 'w+') as f:
            f.write(self.url_template)

    def grab_file(self, url, replace_tabs: bool = True):
        """Захомячить файл по url"""
        contents = ''
        if 'base64,' in url:
            logger.info('NEED to decode BASE64')
            return contents
        try:
            r = self.session.get(url, timeout=10)
        except:
            logger.info('[ERROR]: %s' % url)
            return contents

        contents = r.content
        if replace_tabs:
            contents = r.text
            contents = contents.replace('\t', '  ')
        return contents

    def get_index_html(self):
        """Получить индексный файл"""
        self.index_file = os.path.join(self.template_path, 'index.html')
        if self.local_index:
            return
        contents = self.grab_file(self.url_template)
        with open_file(self.index_file, 'w+') as f:
            f.write(contents)

        # ---------
        # BASE HREF
        # Например,
        # <base href="http://kos9.scompiler.ru/oceanic2/" />
        # ---------
        rega_base = re.compile('<base href=["\']([^>"\']+)', re.I+re.U+re.DOTALL)
        matches_base = rega_base.search(contents)
        if matches_base:
            self.base_path = matches_base.group(1)
            # ---------------------------------------------------
            # Наипалово для хитрожопых, юзающих https://
            # которые повторяют ссылку от корня типа yootheme.com
            # ---------------------------------------------------
            if self.base_path.startswith('https://'):
                self.base_path = 'http://%s/' % self.base_path.replace('https://', '').split('/')[0]
            logger.warning('New base path %s' % (self.base_path, ))

        # ------------------------
        # Стилизуем индексный файл
        # ------------------------
        contents = ''
        with open_file(self.index_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.count('<') > 2:
                line = line.replace('<', '\r\n<')
            contents += line

        with open_file(self.index_file, 'w+') as f:
            f.write(contents)

    def findpath(self, path, item):
        """Полный путь к файлу
           :param path: base_path;
           :param item: old_path (то, что нашлось в регулярке)"""
        if item.startswith('//'):
            return 'http:%s' % item
        if item.startswith('http://') or item.startswith('https://'):
            return item
        # Удаляем имя файла если полный путь его содержит
        if path.endswith('.css') or path.endswith('.js'):
            path = os.path.split(path)[0]
        # Если относительный линк, то поднимаемся по полному пути
        # old_path.startswith("../")
        if item.startswith('../'):
            if '/' in path:
                path = os.path.split(path)[0]
            item = item.replace('../', '', 1)
            # Если есть еще куда подниматься, рекурсируем
            if item.startswith('../'):
                self.findpath(path, item)
            else:
                return os.path.join(path, item)
        if item.startswith('/'):
          # -----------
          # Ищем корень
          # Надо попробовать определить корневой путь попыткой скачивания
          # Если скачиваение не происходит при простом сбивании слеша,
          # значит корень другой и надо изменять base_path
          # -----------
          item = item[1:]
          url = self.base_path + item
          # Фикс на слитный адрес, надо чтобы
          # base_path кончался на слеш
          if not self.base_path.endswith('/') and not item.startswith('/'):
              self.base_path += '/'

          check_file = self.grab_file(url, False)
          if check_file:
              return self.base_path + item
          # Разбиваем url - оставляем только домен (+/)
          else:
              url_array = urllib.parse.urlparse(self.base_path)
              url = url_array.scheme + '://' + url_array.netloc + '/' + item
              check_file = self.grab_file(url, False)
              if check_file:
                  path = url_array.scheme + '://' + url_array.netloc + '/'
        return os.path.join(path, item)

    def load_file(self, path: str = None):
        """Прочитать файл
           :param path: путь к файлу, если не указан - индексный"""
        if not path:
            path = self.index_file
        contents = ''
        with open_file(path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            contents += line
        return contents

    def get_misc_files(self):
        """Получить misc файлы"""
        contents = self.load_file()
        # -----------------------
        # search images in styles
        # -----------------------
        rega_imaga_style = re.compile('(url["(]+([\.]*[^")]+)[")]+)', re.I+re.U+re.DOTALL)
        matches_imga_style = rega_imaga_style.findall(contents)
        # ----
        # MISC
        # ----
        rega_imga = re.compile('(<img[^>]+src[\s]*=[\s]*["\']([^>"\']+)[^>])', re.I+re.U+re.DOTALL)
        matches_imga = rega_imga.findall(contents) + matches_imga_style

        counter = 0
        for item in matches_imga:
            counter += 1
            imga = self.findpath(self.base_path, item[1])
            imga_name = os.path.split(imga)[1]

            cur_imga = item[0].replace(item[1], 'misc/' + imga_name)
            contents = contents.replace(item[0], cur_imga)

            imga_contents = self.grab_file(imga, False)
            if imga_contents:
                imga_file_path = os.path.join(self.misc_path, imga_name)
                imga_file_path = self.clean_path(imga_file_path)
                # -----------------
                # ПРОВЕРКА НА ДУБЛИ
                # -----------------
                if not check_path(imga_file_path):
                    if not imga in self.img_repeated:
                        self.z += 1
                        imga_file_path = imga_file_path + str(self.z)
                if not imga in self.img_repeated:
                    self.img_repeated.append(imga)
                try:
                    with open_file(imga_file_path, 'wb+') as f:
                        f.write(imga_contents)
                except:
                    logger.warning('[ERROR]: image %s' % imga_file_path)
        with open_file(self.index_file, "w+") as f:
            f.write(contents)

    def get_js_files(self):
        """Получить js файлы"""
        contents = self.load_file()
        # --
        # JS
        # <script type="text/javascript" src="scripts/jquery-1.4.3.min.js"></script>
        # <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js"></script>
        # --
        rega_js = re.compile('<script[^>]+src[\s]*=[\s]*["\']([^>"\']+\.js)[^>]*', re.I+re.U+re.DOTALL)
        matches_js = rega_js.findall(contents)
        for item in matches_js:
            js = self.findpath(self.base_path, item)
            self.js_files.append(js)
            js_name = os.path.split(js)[1]
            js_name = self.clean_path(js_name)
            contents = contents.replace(item, 'js/%s' % js_name)
        with open_file(self.index_file, "w+") as f:
            f.write(contents)
        # ----------------
        # Дергаем JS файлы
        # ----------------
        for js in self.js_files:
            contents = self.grab_file(js, False)
            if not contents:
                continue
            js_name = os.path.split(js)[1]
            js_file = os.path.join(self.js_path, js_name)
            with open_file(js_file, "wb+") as f:
                f.write(contents)

    def fix_links(self, path: str = None):
        """Подправить ссылки в файле"""
        contents = self.load_file(path)
        # -
        # A
        # <a href="http://demo.mohd-biz.com/envato/thedawn-html/"><img src="images/skins/dark-blue/thedawnlogo.png" alt="" /></a>
        # -
        matches_a = []
        rega_a = re.compile('(<a [^>]*?href=["\']([^"\']+?)["\'][^>])', re.I+re.U+re.DOTALL)
        matches_a = rega_a.findall(contents)
        for item in matches_a:
            if item[1].startswith("http"):
                cur_link = item[0].replace(item[1], "/")
                contents = contents.replace(item[0], cur_link)
        with open_file(self.index_file, "w+") as f:
            f.write(contents)

    def stylizecss(self, path):
        """Облагородить css разметку переносами
           :param path: путь до файла css"""
        contents = ''
        with open_file(path, 'r') as f:
          lines = f.readlines()
        for line in lines:
            if line.count('}') >= 2 and not 'data:' in line:
                line = line.replace('}', '}\r\n')
            if line.count(';') >= 2 and not 'data:' in line:
                line = line.replace(';', ';\r\n')
            contents = contents + line
        with open_file(path, 'w+') as f:
            f.write(contents)

    def get_css_files(self):
        """Получить css файлы"""
        contents = self.load_file()
        # ---
        # CSS
        # <link rel="stylesheet" href="css/style.css" type="text/css" />
        # ---
        if self.with_params:
            rega_css_with_params = re.compile('<link[^>]*?href[\s]*=[\s]*["\']([^>"\']+\.[acsxphle]{3,4}[^"\']*?)["\']', re.I+re.U+re.DOTALL)
            matches_css = rega_css_with_params.findall(contents)
        else:
            rega_css = re.compile('<link[^>]*href[\s]*=[\s]*["\']([^>"\']+\.[acsxphle]{3,4})[^>]*', re.I+re.U+re.DOTALL)
            matches_css = rega_css.findall(contents)
        for item in matches_css:
            css = self.findpath(self.base_path, item)
            self.css_files.append(css)
            css_name = os.path.split(css)[1]
            css_name = self.clean_path(css_name)
            contents = contents.replace(item, 'css/%s' % css_name)

        # -----------------------------------
        # SUPPORT for @import "css/main.css";
        # -----------------------------------
        matches_import = rega_import.findall(contents)
        if matches_import:
            for item in matches_import:
                css = self.findpath(self.base_path, item)
                self.css_files.append(css)
                css_name = os.path.split(css)[1]
                css_name = self.clean_path(css_name)
                contents = contents.replace(item, 'css/%s' % css_name)

        with open_file(self.index_file, 'w+') as f:
            f.write(contents)

        counter = 0
        for css in self.css_files:
            counter += 1
            self.analyze_css_file(css)

    def analyze_css_file(self, css):
        """Отдельно пройтись по каждому css файлу
           :param css: путь к css файлу"""
        contents_css = '' # Для перезаписи css
        # Тащим файл
        contents = self.grab_file(css)
        if not contents:
            logger.warning('[ERROR]: bad file %s' % css)
            return

        css_name = os.path.split(css)[1]
        css_name = self.clean_path(css_name)

        css_file = os.path.join(self.css_path, css_name)
        if not check_path(css_file):
            now = str(time.time()).replace('.', '_')
            css_file = '%s-%s' % (css_file, now)

        with open_file(css_file, 'w+') as f:
            f.write(contents)

        self.stylizecss(css_file)
        # Парсим css файл
        css = self.clean_path(css)
        with open_file(css_file, 'r') as f:
             lines = f.readlines()
        for line in lines:
            line = self.parse_css_line(css, line)
            contents_css = contents_css + line

        with open_file(css_file, 'w+') as f:
            f.write(contents_css)

    def parse_css_line(self, css: str, line: str):
        """Парсинг css строчки в файле css
           :param css: путь к css файлу
           :param line: строка в css файле"""
        # -----------------------------------
        # SUPPORT for @import "css/main.css";
        # -----------------------------------
        matches_import = rega_import.search(line)
        if matches_import:
            old_path = matches_import.group(1)
            if old_path.endswith('.css'):
                # -------------------------------------------------------------
                # Тут ремарка скажем @import url("../medica-parent/style.css");
                # тогда надо брать путь относительно пути текущего css файла,
                # а не базового => смотрим в функцию findpath
                # css => http://demo.themefuse.com/medica-child/style.css?v=1
                # Видно, что надо отбросить финальный элемент пути
                # -------------------------------------------------------------
                if css.endswith('.css') and '/' in css:
                    css = os.path.split(css)[0]

                temp_css_file = self.findpath(css, kill_quotes(old_path, 'quotes'))
                self.css_files.append(temp_css_file)
                temp_css_name = os.path.split(temp_css_file)[1]
                line = line.replace(old_path, '../css/%s' % temp_css_name)

        matches_img = rega_img.findall(line)
        for match_img in matches_img:
            old_path = match_img
            if old_path.endswith('.css"'):
                # SUPPORT FOR @import url(../css/xxx.css);
                temp_css_file = self.findpath(css, kill_quotes(old_path, 'quotes'))
                css_files.append(temp_css_file)
                temp_css_name = os.path.split(temp_css_file)[1]
                line = line.replace(old_path, '../css/%s' % temp_css_name)
                continue
            # -----------------------
            # Бывает, что svg попался
            # -----------------------
            if 'data:' in match_img:
                continue
            # ----------------------------------
            # Какие-то долбаебы в картинку якорь
            # и бывает, что это все что там есть
            # ----------------------------------
            if '#' in old_path:
                old_path = old_path.split('#')[0].strip()
            if not old_path:
                continue

            img = self.findpath(css, kill_quotes(old_path, 'quotes'))
            img_name = os.path.split(img)[1]
            # Меняем путь в css
            img_folder = os.path.split(img)[0]
            line = line.replace(old_path, '../img/%s' % img_name)
            # Тащим картинку
            contents = self.grab_file(img, False)
            if not contents:
                continue
            img_file_path = os.path.join(self.img_path, img_name)
            # ---------------------------
            # Фикс на имя с ? параметрами
            # ---------------------------
            img_file_path = self.clean_path(img_file_path)

            # ПРОВЕРКА НА ДУБЛИ
            if not check_path(img_file_path):
                if not img in self.img_repeated:
                    self.z += 1
                    img_file_path = img_file_path + str(self.z)
            if not img in self.img_repeated:
                self.img_repeated.append(img)

            with open_file(img_file_path, 'wb+') as f:
                f.write(contents)

        return line
