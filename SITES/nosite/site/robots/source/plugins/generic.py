import os
import time
import json
import logging
import random

from urllib import parse

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from plugins.utils import get_ip, get_hostname

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class GenericBrowser():
    """Основные функции расширяющие Browser
       Скриптизер для Browser
    """
    # Запоминаем результаты выполнения run_script
    run_script_results = {}
    run_script_result = None

    def get_driver(self):
        return self.driver

    def get_attribute(self, el, attr):
        """Получение атрибута элемента
           :param el: элемент DOM
           :param attr: название атрибута
        """
        if isinstance(el, str):
            el = self.get_run_script_result(el)
        return el.get_attribute(attr)

    def run_script(self, script):
        """Выполнение функций скрипта
           например, scripts = (
               ('goto', 'http://ya.ru'), # script
               ('screenshot2telegram', ''),
               ('yandex.yandex_auth', None),
           )
           :param script: алгоритм с командами,
               в скрипт каждая запись это список с 2-3 элементами,
               первый элемент - название функции
               второй элемент - параметры функции
               третий элемент - название переменной для хранения результата
        """
        if not self.check_script(script):
            exit()
        for item in script:
            cmd, params, result_var = item[0], item[1], None
            if len(item) > 2:
                result_var = item[2]

            func = self.find_cmd(cmd)
            if isinstance(params, (str, int, float)):
                result = func(params)
            elif isinstance(params, (list, tuple)):
                result = func(*params)
            elif isinstance(params, dict):
                result = func(**params)
            else:
                result = func()
            # Запоминаем результат выполнения
            self.run_script_result = result
            if result_var:
                self.run_script_results[result_var] = result

            self.debug_run_script('%s(%s)' % (cmd, params))

    def debug_run_script(self, func_name: str = None):
        """Вывод результатов после выполнения run_script"""
        print('---\n%s=>\n%s' % (func_name, self.run_script_result))

    def get_run_script_result(self, result_var: str = None):
        """Получаем переменную
           с результатом выполнения предыдущих действий
           через run_script
           :param result_var: название переменной
        """
        if result_var:
            return self.run_script_results.get(result_var)
        return self.run_script_result

    def check_script(self, script):
        """Проверка всех функций скрипта,
           например, script = (
               ('goto', 'http://ya.ru'),
               ('screenshot2telegram', ''),
               ('yandex.yandex_auth', None),
           )
           :param script: алгоритм с командами
        """
        for item in script:
            cmd = self.find_cmd(item[0])
            if not cmd:
                logger.info('[ERROR]: driver method %s not found' % item[0])
                return False
        return True

    def find_cmd(self, cmd):
        """Находим метод,
           Если в команде есть точка,
           значит, обращение к свойству (плагину)
           :param func: команда
        """
        if '.' in cmd:
            cur_func = self
            cmd_arr = cmd.split('.')
            for item in cmd_arr:
                if hasattr(cur_func, item):
                    cur_func = getattr(cur_func, item)
                else:
                    return None
            return cur_func
        return getattr(self, cmd) if hasattr(self, cmd) else None

    def shuffle_list(self, arr: list =  None):
        """Перемешивание списка,
           :param arr: список, который надо перемешать
        """
        if not arr or isinstance(arr, str):
            arr = self.get_run_script_result(arr)
        if isinstance(arr, list):
            random.shuffle(arr)
            return arr

    def pick_from_list(self, arr: list = None, ind: int = 0):
        """Взять ind элемент из списка
           :param arr: список c элементами
           :param ind: индекс из списка
        """
        if not arr or isinstance(arr, str):
            arr = self.get_run_script_result(arr)
        if isinstance(arr, list) and len(arr) > ind:
            return arr[ind]

    def scroll_to_element(self, el = None):
        """Движение до элемента прокруткой экрана
           :param el: dom - элемент
        """
        if not el or isinstance(el, str):
            el = self.get_run_script_result(el)

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
        return el

    def scroll(self, direction:str = 'down', count: int = 1):
        """Подскролить страничку в direction направлении count раз
           :param direction: направление
           :param count: кол-во раз
        """
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

    def idna(self, domain):
        """Преобразовать в idna байты, затем в строку,
           Например, https://8800из-за-бугра.рф =>
           b'xn--https://8800---7tlbq0b9dbs7prc.xn--p1ai' =>
           xn--https://8800---7tlbq0b9dbs7prc.xn--p1ai
           :param domain: адрес сайта
        """
        if not domain:
            return domain
        return domain.encode('idna').decode('utf-8')

    def goto(self, url: str):
        """Перейти по ссылке
           :param url: ссылка
        """
        self.driver.get(url)

    def refresh(self):
        """Обновить страничку"""
        self.driver.refresh()

    def window_handles(self):
        """Возвращет список открытых вкладок"""
        return self.driver.window_handles

    def current_window_handle(self):
        """Возвращает активную вкладку"""
        return self.driver.current_window_handle

    def close_current_window(self):
        """Закрыть активную вкладку,
           возможно, вызывает
           selenium.common.exceptions.InvalidSessionIdException:
             Message: invalid session id
        """
        time.sleep(2)
        self.driver.close()
        time.sleep(2)

    def switch_to_window(self, window_handle):
        """Переключает на окно/вкладку
           :param window_handle: handler из window_handles()
        """
        time.sleep(0.5)
        self.driver.switch_to.window(window_handle)
        time.sleep(0.5)

    def close_other_tabs(self):
        """Закрыть все вкладки, кроме активной"""
        cur_tab = self.current_window_handle()
        for tab in self.window_handles():
            if tab != cur_tab:
                self.switch_to_window(tab)
                self.close_current_window()
        self.switch_to_window(cur_tab)

    def get_capabilities(self) -> dict:
        """Возвращает capabilities,
           использованные для создания экземпляра
        """
        return self.driver.capabilities

    def maximize_window(self):
        """Сделать максимальный размер окна"""
        self.driver.maximize_window()

    def get_current_url(self, unquote: bool = False):
        """Получить текущий url браузера
           :param unquote: вывести кириллицу нормально
        """
        url = self.driver.current_url
        if unquote:
            url = parse.unquote(url)
        return url

    def get_window_size(self):
        """Получить размер окна"""
        return self.driver.get_window_size()

    # --------------
    # Поиск элемента
    # --------------
    # Другие варианты поиска элемента:
    # find_element_by_partial_link_text
    # find_element_by_class_name

    def find_element_by_id(self, id_selector: str):
        """Поиск элемента по ид
           :param id_selector: ид элемента
        """
        return self.driver.find_element_by_id(id_selector)

    def find_element_by_name(self, name: str):
        """Поиск элемента по имени
           :param name: name элемента
        """
        return self.driver.find_element_by_name(name)

    def find_element_by_xpath(self, xpath: str):
        """Поиск элемента по xpath
           :param xpath: xpath элемента
        """
        return self.driver.find_element_by_xpath(xpath)

    def find_element_by_tag_name(self, tag: str):
        """Поиск элемента по тегу
           :param tag: тег элемента
        """
        return self.driver.find_element_by_tag_name(tag)

    def find_element_by_css_selector(self, selector: str):
        """Поиск элемента по css селектору
           например,
           find_element_by_css_selector('.megamenu-pattern')
           :param selector: селектор элемента
        """
        return self.driver.find_element_by_css_selector(selector)

    def find_element_by_link_text(self, link_text: str):
        """Поиск элемента по тексту ссылки
           :param link_text: текст ссылки элемента
        """
        return self.driver.find_element_by_link_text(link_text)

    # ---------------
    # Поиск элементов
    # ---------------
    # Другие варианты поиска элементОВ:
    # find_elements_by_link_text
    # find_elements_by_partial_link_text
    # find_elements_by_class_name

    def find_elements_by_name(self, name: str):
        """Поиск элементов по имени
           :param name: name элемента
        """
        return self.driver.find_elements_by_name(name)

    def find_elements_by_tag_name(self, tag: str):
        """Поиск элементов по тегу
           :param tag: тег элемента
        """
        return self.driver.find_elements_by_tag_name(tag)

    def find_elements_by_xpath(self, xpath: str):
        """Поиск элементов по xpath
           :param xpath: xpath элемента
        """
        return self.driver.find_elements_by_xpath(xpath)

    def find_elements_by_css_selector(self, selector: str):
        """Поиск элементов по css селектору,
           например,
           find_element_by_css_selector('.megamenu-pattern')
           :param selector: селектор элемента
        """
        return self.driver.find_elements_by_css_selector(selector)

    def find_parent(self, el):
        """Найти parent элемента
           :param el: DOM-элемент
        """
        return el.find_element_by_xpath('..')

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

    def is_element_visible(self, el):
        """Проверка, что элемент видимый
           :param el: DOM-элемент
        """
        return el.is_displayed()

    def get_tag_name(self, el):
        """Тег элемента в нижнем регистре
           :param el: DOM-элемент
        """
        return el.tag_name.lower()

    def history_back(self):
        """Возвращаемся на предыдущую страничку"""
        self.driver.execute_script("window.history.go(-1)")

    def get_hostname(self):
        """Получить название сервера"""
        if hasattr(self, 'hostname') and self.hostname:
            return self.hostname
        self.hostname = get_hostname()
        return self.hostname

    def get_ip(self):
        """Получить ip адрес"""
        if hasattr(self, 'ip') and self.ip:
            return self.ip
        self.ip = get_ip()
        return self.ip


    def screenshot2telegram(self, msg: str = 'Вы запросили скриншот'):
        """Отправить скриншот в телегу"""
        if not hasattr(self, 'telegram') or not self.telegram:
            logger.info('[ERROR]: instance telegram not found')
            return
        screenshot = self.save_screenshot()
        if not os.path.exists(screenshot):
            logger.info('[ERROR]: screenshot not found')
            return
        with open(screenshot, 'rb') as f:
            msg = '%s %s %s\n%s' % (
                self.get_ip(),
                self.get_hostname(),
                self.profile_name,
                msg)
            self.telegram.send_document(f, caption=msg)
        os.unlink(screenshot)

    def generate_coords(self, startx: int = 1, endx: int = None,
                              starty: int = 1, endy: int = None) -> dict:
        """Возращаем случайную координату в заданной области
           :param startx: x1
           :param endx: x2
           :param starty: y1
           :param endy: y2
        """
        viewport_size = self.get_viewport_size()
        if not endx:
            endx = viewport_size['w'] - 1
        if not endy:
            endy = viewport_size['h'] - 1 + self.get_scrolly()
        x = random.randint(startx, endx)
        y = random.randint(starty, endy)
        return {'x': x, 'y': y}


    def accumulate_path(self, startx, starty, endx, endy):
        """Собрать n-ое количество точек для движения к заданной точке
           :param startx: x1
           :param starty: y1
           :param endx: x2
           :param endy: y2
        """
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


    def send_keys(self, el, text):
        """Отправка текста в элемент
           Keys.RETURN для ENTER
           :param el: элемент DOM
           :param text: посылаемый текст
           :param with_enter: добавлять ENTER в конце
        """
        el.send_keys(text)

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


    def get_mouse_coords(self):
        """Получить координаты мыши,
           которые мы должны были отследить из track_mouse
        """
        mouse_coords = self.driver.execute_script("""
            return {'x': window.browser_x, 'y': window.browser_y};
        """)
        if mouse_coords['x'] is None or mouse_coords['y'] is None:
            if mouse_coords['x'] is None:
                mouse_coords['x'] = 0
            if mouse_coords['y'] is None:
                mouse_coords['y'] = 0
        return mouse_coords


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
        # TODO: получать координаты мыши из javascript
        ActionChains(self.driver).move_by_offset(0, 0).perform()
        if not tracked:
            rand = self.generate_coords()
            try:
                ActionChains(self.driver).move_by_offset(rand['x'], rand['y']).perform()
            except Exception as e:
                logger.error(e)


    def move_by_offset(self, xoffset, yoffset):
        """Передвинуть мышь на xoffset, yoffset от текущей позиции мыши
           :param xoffset: смещение x
           :param yoffset: смещение y
        """
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


    def move_to_element(self, el, do_click=False, **kwargs):
        """Передвинуть мышь к элементу
           startx, endx, starty, endy - ограничивает область наведения
           например, когда на элементе другие элементы
           :param el: DOM-элемент
           :param do_click: нажатие
        """
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

    def pretend_user(self):
        """Притвориться пользователем на ТЕКУЩЕМ сайте и кликнуть на случайную ссыль"""
        time.sleep(1)
        self.pretend_user_helper(do_click=True)
        time.sleep(1)
        self.pretend_user_helper(do_click=False)
        time.sleep(1)


    def test_mode(self, mc_servers: list = ['localhost:11211'],
                  cmd_key: str = 'selenium_test_command'):
        """Тестовый режим с приемом команд из кэша

           Демонстрационный сценарий для test_mode
           mc = memcache.Client(['localhost:11211'])
           cmd = [('goto', 'https://3dnews'), ('screenshot2telegram')]
           mc.set('selenium_test_command', json.dumps(cmd))

           :param mc_servers: memcached адреса серверов
           :param cmd_key: ключ в кэше, который мониторим на команды
        """
        import json
        import memcache
        mc = memcache.Client(mc_servers)
        while True:
            try:
                command = mc.get(cmd_key)
                if command:
                    print(command)
                    try:
                        mc.delete(cmd_key)
                        self.run_script(json.loads(command))
                    except Exception as e:
                        print(e)
                time.sleep(1)
            except KeyboardInterrupt:
                break
