import os
import time
import json
import logging
import requests

from urllib import parse

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class GenericBrowser():
    """ Основные функции расширяющие Browser
    """

    def goto(self, url: str):
        """Перейти по ссылке"""
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

    def history_back(self):
        """Возвращаемся на предыдущую страничку"""
        self.driver.execute_script("window.history.go(-1)")


    def get_ip(self, api_url: str = 'http://spam.223-223.ru/my_ip/'):
        """Получить ip адрес
           :param api_url: адрес, который возвращает ip в json
        """
        r = requests.get(api_url, timeout=5)
        return r.json().get('ip')


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
            self.telegram.send_document(f, caption=msg)
        os.unlink(screenshot)

