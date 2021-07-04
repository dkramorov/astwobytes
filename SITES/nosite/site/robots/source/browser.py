# -*- coding:utf-8 -*-
import os
import json
import time
import datetime
import random
import sys
import shutil
import logging
import requests
import pytest

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from plugins.generic import GenericBrowser
from plugins.yandex_search import YandexSearch
from plugins.telegram import TelegramBot
from plugins.skype import SkypePlugin
from plugins.search_queries import get_search_queries
from plugins.ua import (
    fill_screen_resolution,
    pick_user_agent,
)
from plugins.utils import (
    hd_clear_space,
    fill_starts_counter,
    simpler,
    check_connection_over_proxy,
    inform_server,
)

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ------------------------------------
# Usage: pytest example.py
# $ pytest --cache-clear example.py -s
# чтобы stdout писался
# ------------------------------------
# cron.d :
# SHELL=/bin/bash
# */5 * * * * root source /home/jocker/selenium/env/bin/activate && pytest -s --cache-clear /home/jocker/selenium/a223223.py >/dev/null 2>&1
# ------------------------------------

class Browser(GenericBrowser):
    """Реализация класса для удобной эксплуатации selenium"""
    def __init__(self, driver=None, **kwargs):
        """Инициализация браузера
           :param kwargs: словарь переменных
               :kwargs['driver_type'] (str): задать драйвер (хром/мозила)
               :kwargs['proxy'] (str): задать проксик
               :kwargs['proxy_percent'] (int): задать процент использования прокси
               :kwargs['custom_profile'] (str): папка с профилем
               :kwargs['custom_profile_arr'] (list): Список профилей на выбор
               :kwargs['queue_profiles'] (bool): True запускать профили по очереди
               :kwargs['screen'] (str): разрешение экрана
               :kwargs['dont_change_ua'] (bool): True не заменять user agent string
               :kwargs['headless'] (bool): True запускать в --headless режиме (без окна)
               :kwargs['plugins'] (list): список плагинов, которые надо загрузить
               :kwargs['page_load_timeout'] (int): время ожидания загрузки странички
        """
        self.started = datetime.datetime.now()
        self.ip = None
        self.hostname = None
        # ------------------------------
        # Начальная позиция курсора мыши
        # ------------------------------
        self.x = 0
        self.y = 0
        self.messages = []
        self.driver_type = kwargs.get('driver_type')
        if not self.driver_type:
            self.driver_type = 'chrome' # firefox

        self.cur_dir = os.path.split(os.path.abspath(__file__))[0]
        self.locker_file = os.path.join(self.cur_dir, 'locker.txt')

        self.profile_dir = os.path.join(self.cur_dir,
                                        'profiles',
                                        self.driver_type)
        self.screen = '1920x1080'
        self.user_agent = None
        self.proxy = None
        self.headless = False

        guess_folders = [folder for folder in os.listdir(self.profile_dir) if os.path.isdir(os.path.join(self.profile_dir, folder))]
        profile_arr = kwargs.get('custom_profile_arr') or guess_folders
        ordered_profiles = sorted([x for x in profile_arr])

        if driver:
            self.driver = driver
            return

        if not os.path.exists(self.profile_dir):
            os.mkdir(self.profile_dir)

        # -----------------------------
        # Инкрементальный номер запуска
        # -----------------------------
        self.total_starts_counter = fill_starts_counter(self.cur_dir)

        # ------------------------------
        # Создание/выбор нужного профиля
        # ------------------------------
        custom_profile = kwargs.get('custom_profile')
        if custom_profile:
            profile_path = os.path.join(self.profile_dir, custom_profile)
        else:
            # ------------------------
            # Выбор случайного профиля
            # ------------------------
            if profile_arr:
                random.shuffle(profile_arr)
                profile_path = os.path.join(self.profile_dir, profile_arr[0])
            else:
                profile_path = os.path.join(self.profile_dir, 'new_profile')

        # -----------------
        # Очередной профиль
        # -----------------
        is_queue_profiles = kwargs.get('queue_profiles')
        if is_queue_profiles:
            queue_profile = simpler(self.total_starts_counter,
                                    len(profile_arr))
            profile_path = os.path.join(self.profile_dir, ordered_profiles[queue_profile])

        if not os.path.exists(profile_path):
            os.mkdir(profile_path)
        self.cur_profile = profile_path
        self.profile_name = self.cur_profile.split('/')[-1]
        logger.info('[profile]: %s' % (self.cur_profile, ))

        # -----------------
        # Поисковые запросы
        # -----------------
        self.q_arr = get_search_queries()
        # ---------------
        # Папка для логов
        # ---------------
        self.log_folder = os.path.join(self.cur_profile, 'logs')
        if not os.path.exists(self.log_folder):
            os.mkdir(self.log_folder)

        # ------------------------------
        # Попытаться использовать прокси
        # ------------------------------
        proxy = None
        proxy_candidate = kwargs.get('proxy')
        proxy_percent = kwargs.get('proxy_percent')
        if proxy_candidate and proxy_percent:
            if check_connection_over_proxy(proxy=proxy_candidate, probability=proxy_percent):
                self.proxy = proxy_candidate

        # -------------------
        # Зарядить user-agent
        # -------------------
        dont_change_ua = kwargs.get('dont_change_ua')
        if dont_change_ua:
            logger.info('[user agent]: default')
        else:
            self.user_agent = pick_user_agent(self.cur_profile)
            logger.info('[user agent]: %s' % self.user_agent)

        # --------------------------
        # Зарядить разрешение экрана
        # --------------------------
        screen = kwargs.get('screen', '').replace('x', ',').replace(' ', '')
        if not screen:
            screen = fill_screen_resolution(self.cur_profile)
        self.screen = screen

        # Успешное завершения теста
        self.success = False
        # --------
        # PLUGINS:
        # --------
        self.yandex = YandexSearch(self)
        self.skype = SkypePlugin(self)
        self.telegram = None
        plugins = kwargs.get('plugins', {})
        # ----------------
        # PLUGINS settings
        # ----------------
        if 'telegram' in plugins:
            settings = plugins['telegram']
            self.telegram = TelegramBot(
                proxies = settings.get('proxies'),
                token = settings.get('token'),
                chat_id = settings.get('chat_id')
            )
        headless = kwargs.get('headless')
        if headless:
            self.headless = True
        self.debug_performance = False

        # ------------------
        # Блокировочный файл
        # ------------------
        self.set_locker()

        # -----------------------
        # Настройка хром драйвера
        # -----------------------
        if self.driver_type == 'chrome':
            self.setup_chrome()
        # ---------------------------
        # Настройка фаерфокс драйвера
        # ---------------------------
        else:
            self.setup_firefox()
        # ---------------------------------
        # Время ожидания загрузки странички
        # ---------------------------------
        page_load_timeout = kwargs.get('page_load_timeout')
        if not page_load_timeout:
            page_load_timeout = 60
        self.driver.set_page_load_timeout(int(page_load_timeout))

        self.result = [] # Для произвольных результатов
        self.driver.instance = self

        logger.info('[STARTED]: %s' % (datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y'), ))

    def set_locker(self):
        """Ставим блокировку, которая показывает,
           какой профиль сейчас работает
        """
        if os.path.exists(self.locker_file):
            content = ''
            with open(self.locker_file, 'r', encoding='utf-8') as f:
                content = f.read()
            msg = '%s %s, locker exists %s' % (
                self.get_ip(),
                self.get_hostname(),
                content,
            )
            logger.info(msg)
            if self.telegram:
                self.telegram.send_message('%s %s' % (self.telegram.get_emoji('hot'), msg))
            return

        with open(self.locker_file, 'w+', encoding='utf-8') as f:
            f.write(self.profile_name)

    def remove_locker(self):
        """Снимаем блокировку, которая показывает,
           какой профиль сейчас работает
        """
        if not os.path.exists(self.locker_file):
            msg = '%s %s, locker NOT FOUND' % (
                self.get_ip(),
                self.get_hostname(),
            )
            logger.info(msg)
            if self.telegram:
                self.telegram.send_message('%s %s' % (self.telegram.get_emoji('hot'), msg))
            return
        os.unlink(self.locker_file)


    def setup_firefox(self):
        """Настройка firefox драйвера
           !!! Если после webdriver.Firefox()
           !!! нихуя не происходит, значит обновляться надо,
           !!! что-то с чем то не совместимо
           Мозилка думает, что она охуенно умная,
           не дает сохранять профиль, типа можно обратиться
           к driver.profile.path и там будет временная папка,
           где мы нихера не найдем :), кроме user.js настроек

           но на этом же уровне будет реальная папка rust_mozprofile...
           вот ее и надо грабить, в идеале при запуске просто зырить
           новые русты и удалять при выходе

           https://selenium-python.readthedocs.io/api.html
        """
        options = webdriver.FirefoxOptions()
        options.set_preference('browser.link.open_newwindow', 3)
        width, height = self.screen.split(',')
        options.add_argument('--width=%s' % width)
        options.add_argument('--height=%s' % height)

        profile = webdriver.FirefoxProfile(profile_directory=self.cur_profile)
        profile.update_preferences()

        self.profile = profile
        if self.headless:
            options.headless = True

        if self.user_agent:
            profile.set_preference('general.useragent.override', self.user_agent)

        capabilities = webdriver.DesiredCapabilities.FIREFOX
        if self.proxy:
            capabilities['proxy'] = {
                'proxyType': 'MANUAL',
                'httpProxy': self.proxy,
                'ftpProxy': self.proxy,
                'sslProxy': self.proxy
            }
        try:
            self.driver = webdriver.Firefox(firefox_profile=profile,
                                            options=options,
                                            capabilities=capabilities)
        except Exception as e:
            if self.telegram:
                self.telegram.send_message('%s %s' % (self.telegram.get_emoji('hot'), e))
            logger.exception('we can not start')
            exit()

    def setup_chrome(self, debug_performance: bool = False):
        """Настройка хром драйвера
           :param debug_performance: фиксировать всю активность (сеть) for entry in self.driver.get_log('performance')
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        # Использовать /tmp вместо /dev/shm
        # options.add_argument('--disable-dev-shm-usage')
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--dns-prefetch-disable')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-dev-shm-usage')

        if self.user_agent:
            options.add_argument('user-agent=%s' % self.user_agent)
        if self.proxy:
            options.add_argument('--proxy-server=%s' % self.proxy)
        options.add_argument('user-data-dir=%s' % self.cur_profile)
        options.add_argument('window-size=%s' % self.screen)

        features = ('VizDisplayCompositor',
                    'NetworkService', )
        for feature in features:
            options.add_argument('--disable-features=%s' % feature)

        caps = DesiredCapabilities.CHROME
        if debug_performance:
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}
            self.debug_performance = True
        try:
            self.driver = webdriver.Chrome(options=options, desired_capabilities=caps)
        except Exception as e:
            if self.telegram:
                self.telegram.send_message('%s %s' % (self.telegram.get_emoji('hot'), e))
            logger.exception('we can not start')
            exit()
        inform_server(self)

    def get_performance_logs(self):
        """Получаем логи (сетевая активность), например,
           for entry in driver.driver.get_log('performance'):
               log_entry = json.loads(entry['message'])
               msg = log_entry['message']['params']
        """
        if not self.debug_performance:
            logger.info('debug_performance=%s' % self.debug_performance)
            return
        return self.driver.get_log('performance')


    def save_screenshot(self, name: str = None):
        """Сохранение скриншота"""
        if not name:
            name = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
        else:
            while name.startswith('/'):
                name = name[1:]
        if not name.endswith('.png'):
            name += '.png'
        screenshots_path = os.path.join(self.cur_profile, 'screenshots')
        if not os.path.exists(screenshots_path):
            os.mkdir(screenshots_path)
        fname = os.path.join(screenshots_path, name)
        self.driver.save_screenshot(fname)
        return fname


    def log(self, msg: str = None):
        """Логирование в файл действия
           особенно нужен для регрессии"""
        now = datetime.datetime.now()
        if not msg:
            msg = '%s ip=%s\n' % (now.strftime('%H:%M'), self.get_ip())
        log_folder = os.path.join(self.log_folder,
                                  '%s' % (self.started.strftime('%Y-%m-%d'), ))
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        log_file = os.path.join(log_folder, '%s.txt' % (self.started.strftime('%H-%M')))
        with open(log_file, 'a+', encoding='utf-8') as f:
            f.write('%s\n' % (msg, ))

    def get_random_query(self):
        random.shuffle(self.q_arr)
        return self.q_arr[0]

    def get_all_attributes(self, selector):
        """Получение всех атрибутов элемента
           :param selector: селектор, например,
           document.getElementById("myId")
        """
        self.driver.execute_script("""
            var el_attributes = [];
            Array.prototype.slice.call(%s.attributes).forEach(function(item) {
              el_attributes.push([item.name, item.value]);
            });
            return el_attributes;""" % (selector, ))

    # TODO стирание
    def fill_input(self, el, text, delay: float = 0.2):
        """Отправка текста в поле для ввода по символам"""
        for letter in text:
            time.sleep(delay)
            el.send_keys(letter)

    def fill_input_by_id(self, el_id: str, text: str):
        """Поиск поля для ввода и ввод текста в него
           :param text: текст для ввода
           :param el_id: ид элемента
         """
        try:
            self.wait(EC.presence_of_element_located((By.ID, el_id)))
        except Exception:
            return
        el = self.find_element_by_id(el_id)
        self.fill_input(el, text)
        self.send_keys(el, Keys.RETURN)

    def wait(self, cond):
        """Ожидание условия, например,
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "column-left"))
        ) => driver.wait(EC.presence_of_element_located((By.ID, 'column-left')))
        или
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "show_yandex_direct"))
        )"""
        WebDriverWait(self.driver, 10).until(cond)


    def wait_for_element(self,
                         selector: str = '.SearchOrgsButton',
                         cond = By.CSS_SELECTOR):
        """Ожидание пока элемент с нужным условием
           появится на страничке
           :param selector: подходящий параметр для cond
           :param cond: условие By
        """
        try:
            self.wait(EC.presence_of_element_located((cond, selector)))
            return True
        except Exception:
            msg = 'wait_for_element: Элемент не найден %s' % selector
            self.screenshot2telegram(msg=msg)
        return False

    # -----------------
    # JavaScript методы
    # -----------------
    def obibon_link(self, css_selector, ind, to_link):
        """Подмена ссылки на свою
           :param css_selector: css селектор
           :param ind: индекс элемента с которым работаем
           :param to_link: ссылка на которую будем заменять текущую
           DEMO:
           footer = self.find_element_by_tag_name('footer')
           menus = footer.find_elements_by_css_selector('ul.menu li a')
           random_ind = random.randint(0, len(menus))
           self.obibon_link('ul.menu li a', 2, 'http://223-223.ru')
           self.scroll_to_element(menus[random_ind])
           self.move_to_element(menus[random_ind], do_click=True)
        """
        self.driver.execute_script("""
            var a = document.querySelectorAll('%s');
            var selected_a = a[%s];
            selected_a.href = '%s';
        """ % (css_selector, ind, to_link))

    def save_profile(self):
        """Сохранение профиля хитрожопого фаерфокса"""
        if not self.driver_type == 'firefox':
            return
        fname = '/profiles/firefox/%s' % self.profile_name
        if not fname in self.cur_profile:
            logger.error('Something wrong with profile folder %s' % fname)
            return
        time.sleep(3)
        tmp_folder = self.driver.profile.path
        up_folder = os.path.split(tmp_folder)[0]
        up_folder = os.path.split(up_folder)[0]
        folders = os.listdir(up_folder)
        for folder in folders:
            if folder.startswith('rust_mozprofile'):
                path = os.path.join(up_folder, folder)
                profile_file = os.path.join(path, self.profile_name)
                if os.path.exists(profile_file):
                    logger.info('... copy %s' % path)
                    shutil.rmtree(self.cur_profile)
                    shutil.copytree(path, self.cur_profile)
                    time.sleep(3)
                    shutil.rmtree(path) # сами чистим эту поиботу
                    break

    def get_el_coords(self, css_selector):
        """Получение кроссбраузерно позиции элемента
           :param css_selector: js-выражение для селектора,
           например, document.querySelectorAll('ins.adsbygoogle')[0]
        """
        return self.driver.execute_script("""
function getCoords(elem) {
  var box = elem.getBoundingClientRect();
  var body = document.body;
  var docEl = document.documentElement;
  var scrollTop = window.pageYOffset || docEl.scrollTop || body.scrollTop;
  var scrollLeft = window.pageXOffset || docEl.scrollLeft || body.scrollLeft;
  var clientTop = docEl.clientTop || body.clientTop || 0;
  var clientLeft = docEl.clientLeft || body.clientLeft || 0;
  var top = box.top + scrollTop - clientTop;
  var left = box.left + scrollLeft - clientLeft;
  return {
    top: top,
    left: left,
  };
}
return getCoords(%s);""" % css_selector)

    def get_el_size(self, css_selector):
        """Получение размера элемента
           :param css_selector: js-выражение для селектора,
           например, document.querySelectorAll('ins.adsbygoogle')[0]
        """
        return self.driver.execute_script("""
function getSize(elem) {
  return {
    height: elem.offsetHeight,
    width: elem.offsetWidth,
  };
}
return getSize(%s);""" % css_selector)

    def clear_profile(self):
        """Очистка профиля от требухи
           папки кэша скриптов и картинок занимают
           туеву хучу места, поэтому при закрытии браузера
           лучше всего очищать эту говнину
           https://yandex.com/support/metrica/general/cookie-usage.html
           яндекс пишет в куки и хранилище много чего - не надо херить
        """
        bad_folders = ('pnacl',
                       'ShaderCache',
                       'GrShaderCache',
                       'PepperFlash',
                       'BrowserMetrics',
                       'Default/Application Cache',
                       'Default/Cache', # это самая пухлая
                       'Default/Code Cache', # вторая по пухлости
                       'Default/GPUCache',
                       'Default/IndexedDB',
                       #'Default/Local Storage', # яндекс пишет в хранилище
                       'Default/Service Worker',
                      )
        for item in bad_folders:
            bad_path = os.path.join(self.cur_profile, item)
            if os.path.exists:
                try:
                    shutil.rmtree(bad_path)
                except Exception as e:
                    #logger.error('[ERROR]: drop failed %s' % bad_path)
                    pass
        hd_clear_space()
        self.remove_locker()

