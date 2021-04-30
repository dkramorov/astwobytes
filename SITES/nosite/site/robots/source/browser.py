# -*- coding:utf-8 -*-
# VERSION 0.2 alpha
import os
import json
import pickle
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
from plugins.ua import (generate_user_agent,
                        fill_screen_resolution)
from plugins.utils import (hd_clear_space,
                           fill_starts_counter,
                           simpler,
                           check_connection_over_proxy,
                           get_ip)

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
        logger.info('[profile folder]: %s' % (self.profile_dir, ))

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
        self.q_arr = get_search_queries(self.cur_dir, self.cur_profile)
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

        # -----------------------------
        # Инкрементальный номер запуска
        # -----------------------------
        self.profile_starts_counter = 0
        # -------------------
        # Зарядить user-agent
        # -------------------
        user_agent = None
        dont_change_ua = kwargs.get('dont_change_ua')
        if dont_change_ua:
            logger.info('[user agent]: default')
        else:
            ua_file = os.path.join(self.cur_profile, 'ua.json')
            if os.path.exists(ua_file):
                with open(ua_file, 'r', encoding='utf-8') as f:
                    ua_settings = json.loads(f.read())
                    user_agent = ua_settings['ua']
                    self.profile_starts_counter = ua_settings.get('starts_counter', 0)
            else:
                user_agent = generate_user_agent()
            with open(ua_file, 'w+', encoding='utf-8') as f:
                f.write(json.dumps({
                    'ua': user_agent,
                    'starts_counter': self.profile_starts_counter + 1,
                }))
            logger.info('\n[user agent]: %s\n[starts_count]: %s' % (user_agent, self.profile_starts_counter))
        self.user_agent = user_agent
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
        logger.info('[HEADLESS]: %s' % self.headless)
        debug_performance = kwargs.get('debug_performance')
        self.debug_performance = False # в _setup зададим
        # -----------------------
        # Настройка хром драйвера
        # -----------------------
        if self.driver_type == 'chrome':
            self.setup_chrome(debug_performance = debug_performance)
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
            msg = '%s ip=%s\n' % (now.strftime('%H:%M'), get_ip())
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

    def get_driver(self):
        return self.driver

    def get_attribute(self, el, attr):
        """Получение атрибута элемента"""
        return el.get_attribute(attr)

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

    def get_tag_name(self, el):
        """Возвращает тег элемента в нижнем регистре"""
        return el.tag_name.lower()

    def is_element_visible(self, el):
        """Проверка, что элемент видимый
        """
        return el.is_displayed()

    def send_keys(self, el, text):
        """Отправка текста в элемент
           Keys.RETURN для ENTER
           :param el: элемент DOM
           :param text: посылаемый текст
        """
        el.send_keys(text)

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

    def move_to_element(self, el, do_click=False, **kwargs):
        """Передвинуть мышь к элементу
           startx, endx, starty, endy - ограничивает область наведения
           например, когда на элементе другие элементы - чтобы
           не клацнуть на них мать-перемать"""
        self.track_mouse()
        time.sleep(1) # т/к до него scroll_to_element может спутать карты

        fromx = kwargs.get('fromx', 1)
        tox = kwargs.get('tox', 1)
        fromy = kwargs.get('fromy', 1)
        toy = kwargs.get('toy', 1)

        # -------------------------------------------
        # Рассчитываем случайное смещение на элементе
        # -------------------------------------------
        el_props = self.get_element_props(el)
        el_size = el_props['size']
        if el_size['width'] <= 1 or el_size['height'] <= 1:
            logger.info('[ERROR]: el is too small')
            return
        diffx = random.randint(fromx, el_size['width'] - tox)
        diffy = random.randint(fromy, el_size['height'] - toy)
        el_coords = el_props['location']


        actions = ActionChains(self.driver)
        coords = self.get_mouse_coords()
        dest_x = el_props['location']['x'] + diffx + random.randint(-30, 30)
        dest_y = el_props['location']['y'] + diffy + random.randint(-30, 30)
        path = self.accumulate_path(coords['x'], coords['y'], dest_x, dest_y)
        for point in path:
            actions.move_by_offset(point[0], point[1])
        try:
            actions.perform()
        except Exception as e:
            logger.error('%s: coords: %s %s, to %s, scroll %s, offset %s %s' % (e, coords['x'], coords['y'], el_props['location'], self.get_scrolly(), point[0], point[1]))

        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(el, diffx, diffy)
        if do_click:
            logger.info('Click from %s to %s' % (self.get_current_url(), self.get_attribute(el, 'href')))
            actions.click()
        try:
            actions.perform()
        except Exception as e:
            logger.error(e)
            logger.info('[ELEMENT]: %s props %s' % (el, el_props))
            logger.info('[MOVE TO OFFSET]: %s, %s' % (diffx, diffy))
            logger.info('[ATTRIBUTES]: %s' % (self.get_attribute(el, 'href'), ))
        time.sleep(1)

    def move_by_offset(self, xoffset, yoffset, right_away: bool = True):
        """Передвинуть мышь на xoffset, yoffset от текущей позиции мыши"""
        self.track_mouse()
        coords = self.get_mouse_coords()
        doc_size = self.get_document_size()
        scrolly = self.get_scrolly()

        if coords['y'] + yoffset >= scrolly + doc_size['h']:
            yoffset = 0
        elif coords['y'] + yoffset <= scrolly:
            yoffset = 0
        if coords['x'] + xoffset >= doc_size['w']:
            xoffset = 0
        elif coords['x'] + xoffset <= 0:
            xoffset = 0

        logger.info('horiz %s/%s, vert %s/%s, scroll %s, offset %s %s' % (coords['x'], doc_size['w'], coords['y'], doc_size['h'], scrolly, xoffset, yoffset))

        try:
            ActionChains(self.driver).move_by_offset(xoffset, yoffset).perform()
        except Exception as e:
            logger.error(e)
            return None
        return (xoffset, yoffset)

    def get_element_props(self, el):
        """Узнать позицию и размер элемента
           :param el: dom-элемент
        """
        return {
            'location': el.location,
            'size': {
                'width': int(el.size['width']),
                'height': int(el.size['height']),
            }
        }

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

    def find_parent(self, el):
        """Найти parent элемента"""
        return el.find_element_by_xpath('..')

    def generate_coords(self, startx: int = 1, endx: int = None,
                              starty: int = 1, endy: int = None) -> dict:
        """Возращаем случайную координату в заданной области"""
        viewport_size = self.get_viewport_size()
        if not endx:
            endx = viewport_size['w'] - 1
        if not endy:
            endy = viewport_size['h'] - 1 + self.get_scrolly()
        x = random.randint(startx, endx)
        y = random.randint(starty, endy)
        return {'x': x, 'y': y}

    def accumulate_path(self, startx, starty, endx, endy):
        """Собрать n-ое количество точек для движеня к заданной точке"""
        result = []
        viewport_size = self.get_viewport_size()
        scrolly = self.get_scrolly()
        diff = 12 # Порог до которого прыгаем
        while (startx > (endx + diff) or startx < (endx - diff)) or (starty > (endy + diff) or starty < (endy - diff)):
            xoffset = 0

            # Дополнительно будем добавлять от 1/4 до 1/2 от оставшегося расстояния
            if startx > endx:
                xoffset -= random.randint(diff/4, diff)
                speedy = startx + xoffset - endx
                xoffset -= int(speedy/4)
            elif startx < endx:
                xoffset += random.randint(diff/4, diff)
                speedy = endx - startx + xoffset
                xoffset += int(speedy/4)
            startx += xoffset

            yoffset = 0
            if starty > endy:
                yoffset -= random.randint(diff/4, diff)
                speedy = starty + yoffset - endy
                yoffset -= int(speedy/4)
            elif starty < endy:
                yoffset += random.randint(diff/4, diff)
                speedy = endy - starty + yoffset
                yoffset += int(speedy/4)
            starty += yoffset

            #if self.x + xoffset > doc_size['w'] or self.x + xoffset < 0:
            #    xoffset = 0
            #if self.y + yoffset > doc_size['h'] or self.y + yoffset < 0:
            #    yoffset = 0
            #self.x += xoffset
            #self.y += yoffset

            if xoffset == 0 and yoffset == 0:
                break
            result.append((xoffset, yoffset))
        return result

    def scroll_to_element(self, el):
        """"Движение до элемента прокруткой экрана"""
        self.track_mouse()
        window_size = self.get_window_size()
        scrolly = self.get_scrolly()
        el_props = self.get_element_props(el)
        old_scrolly = scrolly

        while el_props['location']['y'] > scrolly + window_size['height']/2:
            self.scroll(count=2)
            scrolly = self.get_scrolly()
            time.sleep(0.1)
            if scrolly == old_scrolly:
                break
            old_scrolly = scrolly

        while el_props['location']['y'] < scrolly + window_size['height']/2:
            self.scroll(direction='up', count=2)
            scrolly = self.get_scrolly()
            time.sleep(0.1)
            if scrolly == old_scrolly:
                break
            old_scrolly = scrolly
        time.sleep(1)

    # -----------------
    # JavaScript методы
    # -----------------
    def track_mouse(self):
        """На каждой страничке надо вешать слушалку движения мыши,
           чтобы знать координаты мыши"""
        tracked = self.driver.execute_script("""
if(window.mouse_pointer !== undefined){
    return true;
}
var cursor_img = document.createElement("img");
cursor_img.setAttribute('src', 'data:image/png;base64,'
    + 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAQAAACGG/bgAAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAA'
    + 'HsYAAB7GAZEt8iwAAAAHdElNRQfgAwgMIwdxU/i7AAABZklEQVQ4y43TsU4UURSH8W+XmYwkS2I0'
    + '9CRKpKGhsvIJjG9giQmliHFZlkUIGnEF7KTiCagpsYHWhoTQaiUUxLixYZb5KAAZZhbunu7O/PKf'
    + 'e+fcA+/pqwb4DuximEqXhT4iI8dMpBWEsWsuGYdpZFttiLSSgTvhZ1W/SvfO1CvYdV1kPghV68a3'
    + '0zzUWZH5pBqEui7dnqlFmLoq0gxC1XfGZdoLal2kea8ahLoqKXNAJQBT2yJzwUTVt0bS6ANqy1ga'
    + 'VCEq/oVTtjji4hQVhhnlYBH4WIJV9vlkXLm+10R8oJb79Jl1j9UdazJRGpkrmNkSF9SOz2T71s7M'
    + 'SIfD2lmmfjGSRz3hK8l4w1P+bah/HJLN0sys2JSMZQB+jKo6KSc8vLlLn5ikzF4268Wg2+pPOWW6'
    + 'ONcpr3PrXy9VfS473M/D7H+TLmrqsXtOGctvxvMv2oVNP+Av0uHbzbxyJaywyUjx8TlnPY2YxqkD'
    + 'dAAAAABJRU5ErkJggg==');
cursor_img.setAttribute('id', 'my_mouse_cursor');
cursor_img.setAttribute('style', 'position: absolute; z-index: 99999999999; pointer-events: none;');
document.body.appendChild(cursor_img);
window.mouse_pointer = document.getElementById('my_mouse_cursor');
document.onmousemove = function(event){
    window.mouse_pointer.style.left = event.pageX + 'px';
    window.browser_x = event.pageX;
    window.mouse_pointer.style.top = event.pageY + 'px';
    window.browser_y = event.pageY;
};
return false;
        """)
        ActionChains(self.driver).move_by_offset(0, 0).perform()
        if not tracked:
            rand = self.generate_coords()
            try:
                ActionChains(self.driver).move_by_offset(rand['x'], rand['y']).perform()
            except Exception as e:
                logger.error(e)

    def get_mouse_coords(self):
        """Получить координаты мыши,
           которые мы должны были отследить из track_mouse"""
        mouse_coords = self.driver.execute_script("""
            return {'x': window.browser_x, 'y': window.browser_y};
        """)
        if mouse_coords['x'] is None or mouse_coords['y'] is None:
            logger.error('--- mouse coords is None %s ---' % mouse_coords)
            if mouse_coords['x'] is None:
                mouse_coords['x'] = 0
            if mouse_coords['y'] is None:
                mouse_coords['y'] = 0
        return mouse_coords

    def get_document_size(self):
        """Получить размер документа"""
        return self.driver.execute_script("""
var body = document.body;
var html = document.documentElement;
var h = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
return {'w': window.innerWidth, 'h': h};""")

    def get_viewport_size(self):
        """Получить размер окна документа"""
        return self.driver.execute_script("return {'w': window.innerWidth, 'h': window.innerHeight}")

    def get_scrolly(self):
        """Получаем скролл по y"""
        return self.driver.execute_script('return window.scrollY;')

    def scroll(self, direction:str = 'down', count:int = 1):
        """Подскролить страничку в direction направлении count раз"""
        directions = (
            ('up', Keys.UP),
            ('down', Keys.DOWN),
            ('left', Keys.LEFT),
            ('right', Keys.RIGHT),
            ('top', Keys.CONTROL + Keys.HOME),
            ('bottom', Keys.CONTROL + Keys.END),
        )
        scrolly = self.get_scrolly()
        for item in directions:
            if item[0] == direction:
                for i in range(count):
                    scroll_height = random.randint(20, 50)
                    if direction == 'up':
                        scrolly -= scroll_height
                    elif direction == 'down':
                        scrolly += scroll_height
                    self.driver.execute_script('window.scrollTo(0, %s)' % (scrolly, ))
                break

    def pretend_user_helper(self, do_click=False, **kwargs):
        """Вспомогательная функция,
           чтобы притвориться пользователем
           :param do_click: выполнять нажатия
        """
        current_url = self.get_current_url()
        scheme = '%s://' % (current_url.split('://')[0], )
        domain = '%s%s' % (scheme, current_url.replace(scheme, '').split('/')[0])

        clicked = False
        links = self.find_elements_by_tag_name('a')
        random.shuffle(links)
        for link in links:
            href = self.get_attribute(link, 'href')
            target = self.get_attribute(link, 'target')

            el_size = self.get_element_props(link)['size']
            if href and el_size['width'] > 10 and el_size['height'] > 5:
                # Всякие скриптованные ссылки нахер не нужны
                if '#' in href or 'tel:' in href or 'mailto:' in href:
                    continue
                # Переход по статике пропускаем
                # если расширение в конце - иди они науй!
                if href[-4] == "." or href[-5] == ".":
                    continue
                if target == '_blank':
                    continue
                if href.startswith('javascript:void(0)'):
                    continue

                # Если надо жмакнуть, но домен левый - не ведемся
                if do_click and not href.startswith(domain):
                    continue
                self.scroll_to_element(link)
                self.emulate_mouse_move()
                if self.is_element_visible(link):
                    clicked = True
                    self.move_to_element(link, do_click=do_click)
                    break
        if do_click and not clicked:
            self.refresh()
            time.sleep(5)

    def emulate_mouse_move(self, count: int = None):
        """Эмулировать движение мыши
           :param count: количество перепрыгиваний
                         на случайные координаты
        """
        self.track_mouse()
        if not count:
            count = random.randint(1, 5)
        for i in range(count):
            actions = ActionChains(self.driver)
            rand = self.generate_coords()
            coords = self.get_mouse_coords()
            path = self.accumulate_path(coords['x'], coords['y'], rand['x'], rand['y'])
            for point in path:
                actions.move_by_offset(point[0], point[1])
            try:
                actions.perform()
            except Exception as e:
                logger.error('%s: coords: %s %s, to %s %s, scroll %s, offset %s %s' % (e, coords['x'], coords['y'], rand['x'], rand['y'], self.get_scrolly(), point[0], point[1]))
                break

    def pretend_user(self):
        """Притвориться пользователем на ТЕКУЩЕМ сайте
           и кликнуть на случайную ссыль
        """
        time.sleep(1)
        self.pretend_user_helper(do_click=True)
        time.sleep(1)
        self.pretend_user_helper(do_click=False)
        time.sleep(1)

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
           яндекс пишет в куки и хранилище много чего - на надо херить
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

