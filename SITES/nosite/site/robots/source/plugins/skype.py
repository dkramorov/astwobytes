# -*- coding:utf-8 -*-
import time
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SkypePlugin:
    """Плагин для skype
       ----------------
       USAGE:
       kwargs = {
           'custom_profile': 'for_skype',
           'dont_change_ua': True,
           'plugins': ['skype', ],
       }
       wd = Browser(**kwargs).get_driver()
       ...
       driver.skype.open()
       if not driver.skype.open_chats():
           logger.error('Мы не смогли найти кнопку Чаты')
           return
       if driver.skype.find_contact('ℑ_ℂKⅇℝ'):
          driver.skype.send_msg('Привет')"""

    def __init__(self, browser):
        """Инициализация"""
        self.browser = browser

    def demo(self):
        """Начиная со второй строчки копипастить"""
        driver = self.browser
        driver.skype.open()
        if not driver.skype.open_chats():
            driver.save_screenshot()
            logger.error('Мы не смогли найти кнопку Чаты')
            return
        if driver.skype.find_contact('ℑ_ℂKⅇℝ'):
            driver.skype.send_msg('Раз-двас')

    def open(self):
        """Открывалка скайпа"""
        login = '89642233223'
        passwd = 'Cnfylfhnysq1'
        self.browser.goto('http://web.skype.com/')
        time.sleep(3)
        search_login = self.browser.find_elements_by_tag_name('input')
        for item in search_login:
            if item.is_displayed() and item.get_attribute('type') == 'email' and item.get_attribute('name') == 'loginfmt':
                item.send_keys('%s\n' % (login, ))
                break
        time.sleep(5)
        search_login = self.browser.find_elements_by_tag_name('input')
        for item in search_login:
            if item.is_displayed() and item.get_attribute('type') == 'password' and item.get_attribute('name') == 'passwd':
                item.send_keys('%s\n' % (passwd, ))
                break
        time.sleep(5)

    def open_chats(self):
        """Ищем кнопку чаты в интерфейсе и нажимаем ее"""
        buttons = self.browser.find_elements_by_tag_name('button')
        for button in buttons:
            role = self.browser.get_attribute(button, 'role')
            title = self.browser.get_attribute(button, 'title')
            if role == 'tab' and title =='Чаты':
                button.click()
                return True
        return False

    def find_contact(self, contact_name: str):
        """Поиск и выбор нужного контакта из контакт листа"""
        contact_list = None
        divs = self.browser.find_elements_by_tag_name('div')
        for div in divs:
            role = self.browser.get_attribute(div, 'role')
            aria_label = self.browser.get_attribute(div, 'aria-label')
            if role == 'group' and aria_label == 'Список бесед':
                contact_list = div
        if not contact_list:
            return None
        contacts = self.browser.find_elements_by_tag_name('div')
        for contact in contacts:
            role = self.browser.get_attribute(contact, 'role')
            aria_label = self.browser.get_attribute(contact, 'aria-label')
            if role == 'button' and aria_label:
                if aria_label.startswith(contact_name):
                    contact.click()
                    return contact
        return None

    def send_msg(self, msg: str):
        """Отправлка сообщения"""
        root_editor = self.browser.find_element_by_css_selector('.DraftEditor-root')
        editor = root_editor.find_element_by_css_selector('.public-DraftEditor-content')
        role = self.browser.get_attribute(editor, 'role')
        contenteditable = self.browser.get_attribute(editor, 'contenteditable')
        if role == 'textbox' and contenteditable == 'true':
            editor.click()
            editor.send_keys('%s\n' % (msg, ))
