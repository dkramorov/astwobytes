# -*- coding:utf-8 -*-
import os
import json
import time
import logging
import random

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class YandexSearch:
    """Плагин для поиска в Яндексе"""

    def __init__(self, browser):
        """Инициализация"""
        self.browser = browser
        self.hints = [] # Подсказки по запросам от Яндекса

    def search_authorization(self):
        """Проверяет авторизацию на яндексе
           Нужно быть обязательно на главной страничке"""
        if not self.browser.get_current_url() == 'https://yandex.ru':
            self.browser.goto('https://yandex.ru')
        try:
            self.browser.wait(EC.presence_of_element_located((By.CSS_SELECTOR, '.username__first-letter')))
            logger.info('Авторизован на Яндекс')
            return True
        except Exception:
            msg = 'yandex.search_authorization: Не авторизован'
            logger.error(msg)
        return False

    def get_search_input(self):
        """Найти input яндекс поиска"""
        search_field = None
        inputs = self.browser.find_elements_by_css_selector('.input__control.input__input')
        if inputs:
            for inp in inputs:
                name = self.browser.get_attribute(inp, 'name')
                if name == 'text':
                    search_field = inp
                    break
        return search_field

    def visit_yandex(self, query: str = ''):
        """Поиск на Яндексе
           :param query: строка запроса
        """
        self.goto_desktop_version()
        if not query:
            query = self.browser.get_random_query()
        logger.info('[SEARCH QUERY]: %s' % (query, ))

        ya_url = 'https://yandex.ru'
        self.browser.goto(ya_url)
        self.browser.emulate_mouse_move()

        ya_url = self.browser.get_current_url()
        search_field = self.get_search_input()
        if search_field:
            self.browser.scroll_to_element(search_field)
            self.browser.move_to_element(search_field, do_click=True, **{'tox': 50})
            for letter in query:
                search_field.send_keys('%s' % letter)
                time.sleep(0.25)
            search_field.send_keys(Keys.RETURN)
            time.sleep(1)
            # Перенажать если url не поменялся
            if self.browser.get_current_url() == ya_url:
                logger.info('[ERROR]: Enter does not work, trying again')
                self.browser.move_to_element(search_field, do_click=True, **{'tox': 50})
                search_field.send_keys(Keys.RETURN)

    def get_yandex_hints(self, query: str = ''):
        """Получить запросы из подсказок Яндекса
           :param query: строка запроса (можно 1 букву)
        """
        cur_url = self.browser.get_current_url()
        ya_url = 'https://yandex.ru'
        if not ya_url in cur_url:
            self.browser.goto(ya_url)
        self.goto_desktop_version()
        self.browser.emulate_mouse_move()

        ya_url = self.browser.get_current_url()

        search_field = self.get_search_input()
        if search_field:
            self.browser.scroll_to_element(search_field)
            self.browser.move_to_element(search_field, do_click=True, **{'tox': 50})
            if not query:
                letters = 'абвгдежзиклмнопрстуфхцчщюя'
                ind = random.randint(0, len(letters) - 1)
                query = letters[ind]
            for letter in query:
                search_field.send_keys(letter)
                time.sleep(0.25)
            search_suggest = self.browser.find_elements_by_css_selector('ul.mini-suggest__popup-content li')
            for item in search_suggest:
                # Если там внутри говноссыль какая-то - пропускаем
                if item.find_elements_by_tag_name('a'):
                    continue
                hint = item.text.strip()
                if not hint in self.hints:
                    self.hints.append(hint)
        return search_field

    def yandex_search_results(self):
        """Вспомогательная функция к goto_search_result
           Найти результаты поиска на Яндексе
           перейти и кликнуть по найденному серпу"""
        serp_chosen = 0
        # В несколько попыток поиска
        attempts = 3
        for i in range(attempts):
            try:
                self.browser.wait(EC.presence_of_element_located((By.CSS_SELECTOR, '.serp-item')))
                break
            except Exception:
                msg = 'Не найдены .serp-item элементы, ip %s, profile %s' % (self.browser.get_ip(), self.browser.profile_name)
                logger.error(msg)
                if self.browser.telegram and i == (attempts - 1):
                    screenshot = self.browser.save_screenshot(name='serp_item_not_found.png')
                    with open(screenshot, 'rb') as f:
                        self.browser.telegram.send_document(f, caption=msg)
                    os.unlink(screenshot)
        # Надем все ссылки
        paths = self.browser.find_elements_by_css_selector('li.serp-item')
        if not paths:
            paths = self.browser.find_elements_by_css_selector('div.serp-item')
        return paths

    def goto_first_a(self, path):
        """Вспомогательная функция к goto_search_result
           Перейти по первой найденной ссылке в элементе
           :param path: элемент серпа на результатах поиска (li)
        """
        driver = self.browser
        window_handles_before = len(driver.window_handles())
        driver.scroll_to_element(path)
        driver.emulate_mouse_move()
        driver.move_to_element(path, do_click=False)
        ya_link = path.find_element_by_tag_name('a')
        if self.browser.get_tag_name(path) == 'li':
            ya_link = ya_link.find_element_by_xpath('..') # h2 выше ссылки
        for i in range(10):
            driver.move_to_element(ya_link, do_click=True)
            time.sleep(1)
            if len(driver.window_handles()) > window_handles_before:
                driver.switch_to_window(driver.window_handles()[-1])
                break
            else:
                logger.info('[ERROR]: serp link click not raise new window')
        time.sleep(1)

    def search_domain_in_serp(self, path, domains: list):
        """Поиск домена внутри серпа на результатах поиска
           :param path: serp элемент в результатах поиска
           :param domains: искомые домены
        """
        if not domains:
            return None
        path_links = path.find_elements_by_css_selector('.path a.link b')
        if not path_links:
            path_links = path.find_elements_by_css_selector('.serp-url__item a')
        for path_link in path_links:
            for domain in domains:
                if domain in path_link.text:
                    logger.info('[FOUND]: %s' % (path_link.text, ))
                    return domain

    def goto_search_result(self, search_domain: str = None, exclude_domains: list = None):
        """Перейти на конкретный результат поиска
           :param search_domain: перейти по этому домену если найден
           :param exclude_domains: не переходить по доменам
        """
        ifound = None
        paths = self.yandex_search_results()
        if search_domain:
            logger.info('[SEARCH DOMAIN]: %s' % (search_domain, ))
            for path in paths:
                if self.search_domain_in_serp(path, [search_domain]):
                    self.goto_first_a(path)
                    return True
        random.shuffle(paths)
        for path in paths:
            if self.search_domain_in_serp(path, exclude_domains):
                continue
            self.goto_first_a(path)
            break

    def is_mobile_version(self):
        """Проверка наличия mini-suggest__button,
           что будет означать, что мы на мобильной версии"""
        if not self.browser.get_current_url() == 'https://yandex.ru':
            self.browser.goto('https://yandex.ru')

        css_selector = '.switch-type'
        links = self.browser.find_elements_by_css_selector(css_selector)
        for link in links:
            if link.text == 'Мобильная версия':
                return False

        tag = 'html'
        html = self.browser.find_element_by_tag_name(tag)
        html_classes = self.browser.get_attribute(html, 'class')
        for html_class in html_classes.split(' '):
            if html_class.startswith('i-ua_browser_') and 'mobile' in html_class:
                return True
        return False

    def goto_desktop_version(self):
        """Перейти на десктоп версию"""
        if not self.is_mobile_version():
            return
        # Переходим в настройки - полная версия
        self.browser.goto('https://yandex.ru/tune/common?retpath=https%3A%2F%2Fyandex.ru%2F&nosync=1')
        time.sleep(1)
        css_selector = 'label.checkbox__label'
        try:
            self.browser.wait(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except Exception:
            return
        labels = self.browser.find_elements_by_css_selector(css_selector)
        for label in labels:
            if not label.text == 'Показывать мобильные версии сервисов':
                continue
            self.browser.scroll_to_element(label)
            self.browser.move_to_element(label, do_click=True)
            time.sleep(2)
            button_save = self.browser.find_element_by_css_selector('button.form__save')
            self.browser.scroll_to_element(button_save)
            self.browser.move_to_element(button_save, do_click=True)
            time.sleep(2)
            return

    def load_credentials(self):
        """Загрузить логин/пароль из файла"""
        login, passwd = None, None
        credentials = os.path.join(self.browser.cur_profile, 'credentials.json')
        if not os.path.exists(credentials):
            logger.info('profile credentials not found %s' % credentials)
            return None, None
        with open(credentials, 'r', encoding='utf-8') as f:
            auth = json.loads(f.read())
            login = auth.get('yandex_login') or auth.get('login')
            passwd = auth.get('yandex_passwd') or auth.get('passwd')
        return login, passwd

    def yandex_auth(self):
        """Авторизация на яндексе
           пароль храним в файле credentials.json
        """
        if self.search_authorization():
            return
        login, passwd = self.load_credentials()
        if not login or not passwd:
            logger.info('yandex credentials not found %s' % credentials)
            return

        def search_enter_another_account():
            """Поиск кнопки Войти в другой аккаунт
               нажимаем ее, если нашли
               Нужно, только если аккаунтов очень много
            """
            css_selector = 'a .passp-account-list__sign-in-button-text'
            try:
                self.browser.wait(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            except Exception:
                return
            buttons = self.browser.find_elements_by_css_selector(css_selector)
            for button in buttons:
                if not button.text == 'Войти в другой аккаунт':
                    continue
                alink = self.browser.find_parent(button)
                self.browser.scroll_to_element(alink)
                self.browser.move_to_element(alink, do_click=True)
                time.sleep(2)
                return

        passport_link = 'https://passport.yandex.ru'
        #css_selector = 'a span.button__text'
        css_selector = 'a.home-link'
        try:
            self.browser.wait(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except Exception:
            logger.error('Нет кнопок на страничке для авторизации')
            return

        buttons = self.browser.find_elements_by_css_selector(css_selector)
        for button in buttons:
            link = self.browser.get_attribute(button, 'href')
            if not link or not link.startswith(passport_link):
                continue
            window_handles = self.browser.window_handles()
            alink = self.browser.find_parent(button)
            self.browser.scroll_to_element(alink)
            self.browser.move_to_element(alink, do_click=True)
            # Авторизация открывается в новой вкладочке
            new_window_handles = self.browser.window_handles()
            if not len(window_handles) < len(new_window_handles):
                break
            time.sleep(1)
            self.browser.switch_to_window(new_window_handles[-1])
            time.sleep(1)
            # Нужно только если много аккаунтов
            #search_enter_another_account()
            self.browser.fill_input_by_id('passp-field-login', login)
            self.browser.fill_input_by_id('passp-field-passwd', passwd)
            time.sleep(3)

            try:
                link_phone = self.browser.find_elements_by_css_selector('.Button2')
                for button in link_phone:
                    if 'Не' in button.text and 'сейчас' in button.text:
                        self.browser.scroll_to_element(button)
                        self.browser.move_to_element(button, do_click=True)
                        time.sleep(3)
                        break
            except Exception as e:
                logger.info('[ERROR]: %s' % e)
            break

        screenshot = self.browser.save_screenshot(name='yandex_auth_result.png')
        msg = 'Результат авторизации на Яндекс %s' % self.browser.profile_name
        with open(screenshot, 'rb') as f:
            self.browser.telegram.send_document(f, caption=msg)

    def load_yandex_adv(self, el_id, rtb_block_id: str):
        """Подгрузить контекстную рекламу в el с rtb_block_id идентификатором
           :param el_id: ид элемента, куда будем подгружать объяву
           :param rtb_block_id: идентификатор блока
        """
        el = self.browser.find_element_by_id(el_id)
        if not el:
            logger.error('[ERROR]: load_yandex_adv - #%s not found' % el_id)
            return
        self.browser.scroll_to_element(el)
        self.browser.scroll(count=2)
        self.browser.driver.execute_script("""
(function(n) {
  window[n] = window[n] || [];
  window[n].push(function() {
    Ya.Context.AdvManager.render({
      blockId: "%s",
      renderTo: "%s",
      async: true,
    });
  });
  var t = document.getElementsByTagName("script")[0];
  var s = document.createElement("script");
  s.type = "text/javascript";
  s.src = "//an.yandex.ru/system/context.js";
  s.async = true;
  t.parentNode.insertBefore(s, t);
})("yandexContextAsyncCallbacks");
        """ % (rtb_block_id, el_id))
        time.sleep(3)

    def fuck_yandex_adv(self, rtb_blocks: list = None,
                        container_id: str = None,
                        do_click: bool = False):
        """Если контекстная реклама не отображается,
           значит подружаем альтернативный блок
           предварительно следует выполнять check_yandex_adv
           Надо ввести проверку - если есть сайдбар,
           тогда выполнять функцию внутри любой другой
           R-A-506932-1 - 3000 (не трогать - включен в сайдбаре)
           R-A-516290-1 - 2000
           R-A-577799-1 - 1000
           R-A-560520-1 - 0
           :param driver: browser
           :param rtb_blocks: список блоков, которые будем подгружать
           :param container_id: идентификатор элемента, куда грузим рекламу
           :param do_click: переход на яндекс рекламу
        """
        driver = self.browser
        window_handles_before = len(driver.window_handles())
        window_handle_before = driver.current_window_handle()
        def goto_adv(el, max_attempts: int = 5):
            """Перейти по яндекс рекламе и посуетится там"""
            if not do_click:
                return
            adv_opened = False
            for i in range(max_attempts):
                driver.move_to_element(el, do_click=do_click)
                time.sleep(2)
                if len(driver.window_handles()) > window_handles_before:
                    driver.switch_to_window(driver.window_handles()[-1])
                    adv_opened = True
                    time.sleep(2)
                    break
            if not adv_opened:
                logger.error('YANDEX ADV not opened')
                screenshot = self.browser.save_screenshot(name='yandex_adv_not_opened.png')
                msg = 'Не получилось открыть Яндекс Рекламу %s' % self.browser.profile_name
                with open(screenshot, 'rb') as f:
                    self.browser.telegram.send_document(f, caption=msg)
                return
            for i in range(random.randint(2, 3)):
                time.sleep(5)
                driver.pretend_user()
            # Вернуться на window_handle_before
            for i in range(10):
                cur_handle = driver.current_window_handle()
                if cur_handle != window_handle_before:
                    driver.close_current_window()
                    time.sleep(2)
                    driver.switch_to_window(driver.window_handles()[-1])
                    time.sleep(2)
                else:
                    break

        if not rtb_blocks:
            rtb_blocks = ('R-A-516290-1', 'R-A-577799-1', 'R-A-560520-1')
        if not container_id:
            container_id = 'pagebreak'
        for rtb_block in rtb_blocks:
            yandex_ad = driver.find_element_by_id(container_id)
            driver.scroll_to_element(yandex_ad)
            driver.scroll(count=2)
            driver.driver.execute_script("""
(function(n) {
  window[n] = window[n] || [];
  window[n].push(function() {
    Ya.Context.AdvManager.render({
      blockId: "%s",
      renderTo: "%s",
      async: true,
    });
  });
  var t = document.getElementsByTagName("script")[0];
  var s = document.createElement("script");
  s.type = "text/javascript";
  s.src = "//an.yandex.ru/system/context.js";
  s.async = true;
  t.parentNode.insertBefore(s, t);
})("yandexContextAsyncCallbacks");
            """ % (rtb_block, container_id))
            time.sleep(5)

            yandex_ad = driver.find_element_by_id(container_id)
            # Ссылок может не быть, если это фрейм, поэтому ищем ytag,
            # возможно фрейм грузится на собственную яндекс-рекламу
            # 1) ссылка может содержать картинку - такую берем
            # 2) ссылка может содержать текст - такую берем
            adv_links = yandex_ad.find_elements_by_tag_name('a')
            random.shuffle(adv_links)
            adv_tags = yandex_ad.find_elements_by_tag_name('yatag')
            if len(adv_links) > 0 or len(adv_tags) > 0:
                logger.info('+ yandex adv links found %s' % rtb_block)
                for adv_link in adv_links:
                    if not adv_link.is_displayed():
                        continue
                    href = driver.get_attribute(adv_link, 'href')
                    if not href:
                        continue
                    if 'direct.yandex.ru' in href:
                        continue
                    search_img = adv_link.find_elements_by_tag_name('img')
                    text = adv_link.text
                    if search_img and do_click:
                        img = search_img[0]
                        driver.move_to_element(img)
                        goto_adv(img)
                        break
                    elif text and not 'крыть' in text and not 'ндекс' in text:
                        driver.move_to_element(adv_link)
                        goto_adv(adv_link)
                        break
                time.sleep(5)
                return True
            logger.info('- yandex adv links NOT found %s' % rtb_block)
        return False

    def yandex_reviews(self, max_work: int = 5):
        """За отзывы даются балы,
           надо заходить и протыкивать все
           :param max_work: максимальное кол-во отзывов
        """
        cur_url = self.browser.get_current_url()
        ya_url = 'https://reviews.yandex.ru/ugcpub/cabinet'
        if not ya_url in cur_url:
            self.browser.goto(ya_url)

        def search_new_rating():
            """Поиск звездочек, то есть, того,
               что можно оценить,
               если не найдем, вернем False
               :return bool:
            """
            ratings = self.browser.find_elements_by_css_selector('.RatingEditable')
            if not ratings:
                return False
            for rating in ratings:
                is_checked = rating.find_elements_by_css_selector('.RatingEditable-Star_checked')
                if not is_checked:
                    self.browser.scroll_to_element(rating)
                    time.sleep(3)
                    not_checked = rating.find_elements_by_css_selector('.RatingEditable-Star')
                    if not_checked:
                        self.browser.move_to_element(not_checked[0], do_click=True)
                return True
            return False

        for i in range(max_work):
            if not search_new_rating():
                break
            self.browser.refresh()
            time.sleep(2)


    def yandex_make_review(self,
                           org_name: str = 'Первая справочная 223',
                           text: str = 'Отличная организация'):
        """Сделать отзыв по организации
           :param org_name: ключевики для нахождения компании
           :param text: отзыв
        """
        cur_url = self.browser.get_current_url()
        ya_url = 'https://reviews.yandex.ru/ugcpub/cabinet'
        if not ya_url in cur_url:
            self.browser.goto(ya_url)

        # Кнопка поиска организации
        selector = '.SearchOrgsButton'
        if not self.browser.wait_for_element(selector=selector):
            return
        button = self.browser.find_element_by_css_selector(selector)
        self.browser.scroll_to_element(button)
        time.sleep(1)
        self.browser.move_to_element(button, do_click=True)

        # Модалка для поиска организации
        selector = '.SearchOrgsPopup-Content'
        if not self.browser.wait_for_element(selector=selector):
            return
        modal = self.browser.find_element_by_css_selector(selector)

        # input для поиска организации
        selector = '.Textinput-Control'
        if not self.browser.wait_for_element(selector=selector):
            return
        modal_input = self.browser.find_element_by_css_selector(selector)
        self.browser.move_to_element(modal_input, do_click=True)
        self.browser.send_keys(modal_input, org_name)
        time.sleep(2)

        # компания в списке после поиска
        selector = '.SearchBlock-List .ObjectInfo'
        if not self.browser.wait_for_element(selector=selector):
            return
        orgs = self.browser.find_elements_by_css_selector(selector)
        if len(orgs) > 1:
            self.browser.screenshot2telegram(msg = 'yandex_make_review: нашлось больше одной компании по %s' % org_name)
            return
        org = orgs[0]
        self.browser.move_to_element(org, do_click=True)

        # кол-во звезд
        selector = '.Card-Content .ReviewFormContent-FormContentLastReviewLabelInfo .RatingEditable-Star'
        if not self.browser.wait_for_element(selector=selector):
            return
        review_stars = self.browser.find_elements_by_css_selector(selector)
        # звезды идут по-дурацки справо налево
        self.browser.move_to_element(review_stars[0], do_click=True)
        time.sleep(1)

        # поле для ввода отзыва
        selector = '.Card-Content textarea.Textarea-Control'
        if not self.browser.wait_for_element(selector=selector):
            return
        review_textarea = self.browser.find_element_by_css_selector(selector)
        value = self.browser.get_attribute(review_textarea, 'value')
        #if value:
        #    err = 'yandex_make_review: отзыв по %s уже оставлен: %s' % (org_name, value)
        #    self.browser.screenshot2telegram(msg = err)
        #    return
        if not value:
            for letter in text:
                review_textarea.send_keys(letter)
                time.sleep(0.3)

        # кнопка отправки отзыва, не всегда видна,
        # поэтому жмакаем яваскриптом
        selector = '.Card-Content .ReviewFormContent-FormButton'
        if not self.browser.wait_for_element(selector=selector):
            return
        #review_submit = self.browser.find_element_by_css_selector(selector)
        #self.browser.move_to_element(review_submit, do_click=True)
        self.browser.driver.execute_script("""
            document.querySelector("%s").click();
        """ % selector)
        time.sleep(2)
