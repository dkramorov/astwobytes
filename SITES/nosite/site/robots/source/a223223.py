# -*- coding:utf-8 -*-
import os
import json
import time
import datetime
import random
import sys
import logging
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from browser import Browser
from plugins.utils import search_process, get_hd_space, get_ip
from plugins.yandex_adv_info import get_yandex_adv_clicks

from envparse import env
env.read_envfile()
PROXY = env('PROXY')
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = env('TELEGRAM_CHAT_ID')
HEADLESS = env('HEADLESS', cast=bool, default=False)
DRIVER_TYPE = env('DRIVER_TYPE')
SEARCH_YANDEX_ADV_TRIES = 2
QUEUE_PROFILES = env('QUEUE_PROFILES', cast=bool, default=True)
MULTIPLE_START = env('MULTIPLE_START', cast=bool, default=False)
VISIT_223_SITES = env('VISIT_223_SITES', cast=bool, default=False)
LOAD_ALT_YANDEX_ADV = env('LOAD_ALT_YANDEX_ADV', cast=bool, default=False)
DEBUG_PERFORMANCE = env('DEBUG_PERFORMANCE', cast=bool, default=False)

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
browser = None
# ------------------------
# Usage: pytest example.py
# $ pytest example.py -s,
# чтобы stdout писался
# ------------------------

process = '%s.py' % __name__
if not MULTIPLE_START:
    analog = search_process(['pytest', process])
    if analog:
        logger.error('already running %s' % analog)
        exit()

# -------------------------------------
# Каждый тест использует фикстуру,
# которая создаст состояние для теста,
# тут запускается и разрушается браузер
# -------------------------------------

@pytest.fixture
def original_driver(request):
    kwargs = {
        'driver_type': DRIVER_TYPE,
        #'screen': '1280x800',
        #'proxy_percent': 25,
        #'custom_profile': 'kimadav',
        #'custom_profile_arr': ['bbugoga5', 'bbugoga6', ],
        'queue_profiles': QUEUE_PROFILES,
        'headless': HEADLESS,
        'debug_performance': DEBUG_PERFORMANCE,
        'plugins': {
            'skype': {},
            'telegram': {
                'proxies': {
                    'http': PROXY,
                    'https': PROXY,
                } if PROXY else {},
                'token': TELEGRAM_TOKEN,
                'chat_id': TELEGRAM_CHAT_ID,
            },
        },
    }
    wd = Browser(**kwargs).get_driver()

    def fin():
        """Альтернативный финализер для фикстуры
           он выполнится в любом случае, после того
           как выполнится основной тест, в конце
           основного теста можно задать переменную и,
           если она здесь отсутсвуте, тогда мы знаем,
           что в основном тесте произошла ошибка"""
        wd.instance.save_profile() # для хитрожопого firefox
        wd.quit()
        # ---------------------------------------------------
        # Оповещаем в телегу, что была ошибка, в этом случае,
        # можно просто удалить нах файл с количеством кликов
        # ---------------------------------------------------
        if wd.instance.telegram:
            wd.instance.telegram.send_message('\n'.join(wd.instance.messages), disable_web_page_preview = True)
        wd.instance.clear_profile()

    request.addfinalizer(fin)
    #request.addfinalizer(wd.quit)
    return wd

def goto_target_my_com_adv(driver):
    """Загрузка ибучей рекламы майла
       Поиск контекстной рекламы и жмак на нее
    """
    driver.log('def %s\n' % (goto_target_my_com_adv.__name__, ))

    if not '223-223.ru' in driver.get_current_url():
        driver.goto('https://223-223.ru/q/%s/' % driver.get_random_query())
        time.sleep(3)

    container_id = "pagebreak"
    driver.driver.execute_script("""
        $.getScript('https://ad.mail.ru/static/ads-async.js', function( data, textStatus, jqxhr ) {
            $('#%s').append($('<div class="container"><div class="row"><div id="target_my_com_ad" class="text-center"><ins class="mrg-tag" style="display:inline-block;width:320px;height:50px" data-ad-client="ad-861873" data-ad-slot="861873"></ins></div></div></div>'));
            (MRGtag = window.MRGtag || []).push({});
        });""" % (container_id, ))

    window_handles_before = len(driver.window_handles())

    remove_fucking_noisy_popup(driver)
    target_my_com_ad = driver.find_element_by_id('target_my_com_ad')

    for i in range(3):
        driver.scroll_to_element(target_my_com_ad)
        driver.move_to_element(target_my_com_ad, do_click=True)

        if len(driver.window_handles()) > window_handles_before:
            time.sleep(1)
            driver.switch_to_window(driver.window_handles()[-1])
            msg = '+ TARGET ADV'
            if not msg in driver.messages:
                driver.messages.append(msg)
            time.sleep(1)
            break

    for i in range(random.randint(2, 3)):
        time.sleep(5)
        driver.pretend_user()

def alt_yandex_adv(driver):
    """Загрузка альтернативной яндекс-рекламы"""
    if not LOAD_ALT_YANDEX_ADV:
        return
    remove_fucking_noisy_popup(driver)
    result = driver.yandex.fuck_yandex_adv(rtb_blocks=['R-A-516290-1', 'R-A-577799-1'], do_click=True)
    msg = '- ALT YANDEX ADV LINKS'
    if result:
        msg = '+ ALT YANDEX ADV LINKS'
        if not msg in driver.messages:
            driver.messages.append(msg)
    logger.info(msg)

def remove_fucking_noisy_popup(driver):
    """Закрыть ибучие окна всплывашки"""
    driver.log('def %s\n' % (remove_fucking_noisy_popup.__name__, ))
    try:
        driver.wait(EC.presence_of_element_located((By.CSS_SELECTOR, '.b24-widget-button-shadow')))
        driver.driver.execute_script("""
var b24 = document.querySelector('.b24-widget-button-shadow');
b24.parentNode.parentNode.removeChild(b24.parentNode);
        """)
        driver.wait(EC.presence_of_element_located((By.CSS_SELECTOR, '.white-saas-generator')))
        driver.driver.execute_script("""
var blya = document.querySelector('.white-saas-generator');
blya.parentNode.removeChild(blya);
var blya_bg = document.querySelector('.cbk-window-bgr');
blya_bg.parentNode.removeChild(blya_bg);
        """)
    except Exception as e:
        pass

def visit_yandex(driver):
    """Поиск на Яндексе, переход на сайт, по возможности на наш домен"""
    our_domain = '223-223.ru'

    if not driver.yandex.search_authorization():
        msg = 'Не авторизован на Yandex'
        logger.info(msg)
        if not msg in driver.messages:
            driver.messages.append(msg)

    driver.yandex.visit_yandex()
    is_our_domain = driver.yandex.goto_search_result(search_domain=our_domain)
    if not is_our_domain:
        for i in range(random.randint(1, 3)):
            driver.pretend_user()
    time.sleep(2)

def a223_goto_search_page(driver, page: str = None):
    """Переход в раздел каталог/товары/работу/афишу"""
    driver.log('def %s, page %s\n' % (a223_goto_search_page.__name__, page))

    links_classes = ['all', 'cat', 'prices', 'work', 'afisha']
    search_form = driver.find_element_by_id('search_mini_form')
    driver.scroll_to_element(search_form)
    search_links = search_form.find_elements_by_tag_name('a')
    random.shuffle(search_links)
    for search_link in search_links:
        link_class = driver.get_attribute(search_link, 'class')
        if not link_class:
            continue
        link_class = link_class.split(' ')[0]
        if not link_class in links_classes:
            continue

        if driver.is_element_visible(search_link):
            if not page or page == link_class:
                driver.move_to_element(search_link, do_click=True)
                break
    time.sleep(3)
    alt_yandex_adv(driver)
    driver.emulate_mouse_move()

def find_companies(driver):
    """Находим контейнеры с компаниями на страничке"""
    driver.log('def %s\n' % (find_companies.__name__, ))
    return driver.find_elements_by_css_selector('.product-layout')

def find_random_company(driver):
    """Находим случайную компанию на страничке"""
    driver.log('def %s\n' % (find_random_company.__name__, ))

    containers = find_companies(driver)
    if containers:
        random.shuffle(containers)
        container = containers[0]
        return container
    return None

def a223_do_search(driver):
    """Выполнить поиск на страничке"""
    driver.log('def %s\n' % (a223_do_search.__name__, ))

    search_field = driver.find_element_by_id('autocomplete_search')
    driver.scroll_to_element(search_field)
    driver.emulate_mouse_move()
    driver.move_to_element(search_field, do_click=True, **{'fromx': 60, 'tox': 100})
    query = driver.get_attribute(search_field, 'value')
    if query:
        clear_input = driver.find_element_by_id('search_form_input_clear')
        driver.move_to_element(clear_input, do_click=True)
        time.sleep(2)

    query = driver.get_random_query()
    for letter in query:
        driver.find_element_by_id('autocomplete_search').send_keys('%s' % letter)
        time.sleep(0.25)

    driver.find_element_by_id('autocomplete_search').send_keys(Keys.RETURN)
    time.sleep(3)
    alt_yandex_adv(driver)

def company_bustling_on_listing(driver):
    """Суета в компании после поиска"""
    driver.log('def %s\n' % (company_bustling_on_listing.__name__, ))

    companies = find_companies(driver)
    if companies:
        company = find_random_company(driver)
        if not company:
            return

        pk = driver.get_attribute(company, 'data-org-pk')
        ask_buttons = company.find_elements_by_css_selector('.ask_question')
        if not ask_buttons:
            return
        ask_button = ask_buttons[0]
        driver.scroll_to_element(ask_button)
        driver.emulate_mouse_move()
        driver.move_to_element(ask_button, do_click=True)
        time.sleep(0.5)

        # Сейчас только зареганные могут писать,
        # имя уже заполнено, телефон тоже должен быть
        # но у ботяр пустой он, поэтому заполняем
        #inp_name = company.find_element_by_id('input-name-%s' % (pk, ))
        #driver.scroll_to_element(inp_name)
        #driver.move_to_element(inp_name, do_click=True)
        #for letter in driver.get_random_query():
        #    inp_name.send_keys(letter)
        #    time.sleep(0.30)

        inp_phone = company.find_element_by_id('input-phone-%s' % (pk, ))
        driver.scroll_to_element(inp_phone)
        driver.move_to_element(inp_phone, do_click=True)
        for i in range(10):
            inp_phone.send_keys(random.randint(0, 9))
            time.sleep(0.25)

        inp_msg = company.find_element_by_id('input-msg-%s' % (pk, ))
        driver.scroll_to_element(inp_msg)
        driver.move_to_element(inp_msg, do_click=True)
        for letter in driver.get_random_query():
            inp_msg.send_keys(letter)
            time.sleep(0.30)
        inp_msg.send_keys(' ')
        for letter in driver.get_random_query():
            inp_msg.send_keys(letter)
            time.sleep(0.30)

def check_yandex_adv(driver):
    """Проверка, что контекстная реклама отображается"""
    driver.log('def %s\n' % (check_yandex_adv.__name__, ))
    try:
        driver.wait(EC.presence_of_element_located((By.ID, 'show_yandex_direct')))
        show_yandex_direct = driver.find_element_by_id('show_yandex_direct')
    except:
        show_yandex_direct = None
    if show_yandex_direct:
        driver.scroll_to_element(show_yandex_direct)
        driver.move_to_element(show_yandex_direct, do_click=True)
        time.sleep(1)
        driver.refresh()
        time.sleep(2)
    try:
        driver.wait(EC.presence_of_element_located((By.ID, 'hide_yandex_direct')))
        hide_yandex_direct = driver.find_element_by_id('hide_yandex_direct')
    except:
        hide_yandex_direct = None
    if hide_yandex_direct:
        driver.scroll_to_element(hide_yandex_direct)
        driver.move_to_element(hide_yandex_direct)
    else:
        msg = '[BAD]: hide_yandex_direct not found %s' % (driver.profile_name, )
        logger.info(msg)
        driver.messages.append(msg)
        return False
    try:
        driver.wait(EC.presence_of_element_located((By.ID, 'yandex_ad')))
        yandex_ad = driver.find_element_by_id("yandex_ad")
    except Exception as e:
        msg = '[BAD]: yandex_ad not found %s' % (driver.profile_name, )
        logger.info(msg)
        driver.messages.append(msg)
        time.sleep(20)
        return False
    driver.scroll_to_element(yandex_ad)
    adv_links = yandex_ad.find_elements_by_tag_name("a")
    if len(adv_links) < 1:
        msg = '- YANDEX ADV LINKS'
        logger.info(msg)
        #driver.messages.append(msg)
        driver.pretend_user()
        return False
    else:
        msg = '+ YANDEX ADV LINKS, %s' % driver.get_current_url(unquote=True)
        logger.info(msg)
        driver.messages.append(msg)

    time.sleep(2)
    driver.emulate_mouse_move()
    return True

def goto_yandex_adv(driver):
    """Поиск контекстной рекламы и жмак на нее"""
    driver.log('def %s\n' % (goto_yandex_adv.__name__, ))

    window_handles_before = len(driver.window_handles())

    remove_fucking_noisy_popup(driver)
    is_yandex_adv = check_yandex_adv(driver)
    if not is_yandex_adv:
        return False

    yandex_ad = driver.find_element_by_id('yandex_ad')

    driver.scroll_to_element(yandex_ad)
    driver.move_to_element(yandex_ad)
    adv_links = yandex_ad.find_elements_by_tag_name('a')
    random.shuffle(adv_links)
    for adv_link in adv_links:
        driver.scroll_to_element(adv_link)
        driver.move_to_element(adv_link)
        if adv_link.is_displayed():
            href = driver.get_attribute(adv_link, 'href')
            if 'direct.yandex.ru' in href:
                continue
            # ------------------
            # Кликаем по паренту
            # ------------------
            ya_link = adv_link.find_element_by_xpath('..')#.find_element_by_xpath('..')
            driver.scroll_to_element(ya_link)
            driver.emulate_mouse_move()
            driver.move_to_element(ya_link, do_click=True)
            break
    if len(driver.window_handles()) > window_handles_before:
        time.sleep(1)
        driver.switch_to_window(driver.window_handles()[-1])
        time.sleep(1)

        # Пока закомментируем если уже посещение было
        #already_visited = check_visited_adv(driver)
        #if already_visited:
            #time.sleep(3)
            #return True

        for i in range(random.randint(2, 3)):
            time.sleep(5)
            driver.pretend_user()
        return True
    else:
        msg = 'Не удалось открыть яндекс-рекламу'
        logger.error(msg)
        driver.messages.append(msg)
        #goto_google_adv(driver)
    return False

def goto_google_adv(driver):
    """Поиск контекстной рекламы и жмак на нее"""
    driver.log('def %s\n' % (goto_google_adv.__name__, ))

    time.sleep(1)
    yandex_ad = driver.find_element_by_id('yandex_ad')
    driver.scroll_to_element(yandex_ad)

    window_handles_before = len(driver.window_handles())
    css_selector = 'ins.adsbygoogle[data-ad-slot=\'5726774098\']'

    google_ad = driver.find_element_by_css_selector(css_selector)
    adv_props = driver.get_element_props(google_ad)
    driver.scroll_to_element(google_ad)
    remove_fucking_noisy_popup(driver)
    driver.move_to_element(google_ad, do_click=True)

    if len(driver.window_handles()) > window_handles_before:
        time.sleep(1)
        driver.switch_to_window(driver.window_handles()[-1])
        time.sleep(1)

        msg = '+ GOOGLE ADV LINKS %s' % (driver.profile_name, )
        logger.info(msg)
        driver.messages.append(msg)

        for i in range(random.randint(2, 3)):
            time.sleep(5)
            driver.pretend_user()
    else:
        msg = '- GOOGLE ADV LINKS %s' % (driver.profile_name, )
        logger.info(msg)
        driver.messages.append(msg)

def check_visited_adv(driver):
    """Записываем запрос в файл,
       если уже посещали такой домен, то вернем False,
       чтобы по другой ссылке сходить"""
    visited_adv = []
    visited_adv_fname = 'visited_adv.txt'
    visited_adv_path = os.path.join(driver.cur_profile, visited_adv_fname)
    if os.path.exists(visited_adv_path):
        with open(visited_adv_path, 'r', encoding='utf-8') as f:
            visited_adv = json.loads(f.read())
    domain_parts = driver.get_current_url().split('://')[1]
    domain_parts = domain_parts.split('#')[0]
    domain_parts = domain_parts.split('?')[0]
    domain = domain_parts.split('/')[0]

    # TODO: если мы уже посещали такую страничку,
    # то посидеть на ней 15 сек и вернуться на 223-223,
    # там должна появиться новая рекламка
    if domain in visited_adv:
        return True

    visited_adv.append(domain)
    with open(visited_adv_path, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(visited_adv))
    return False


def a223_goto_main_menu(driver):
    """Переход по главному меню"""
    #mobile_menu = driver.find_element_by_id('show-megamenu')
    #driver.scroll_to_element(mobile_menu)
    #is_mobile_menu = driver.find_element_by_id('remove-megamenu')
    #if driver.is_element_visible(mobile_menu) and not driver.is_element_visible(is_mobile_menu):
    #    driver.move_to_element(mobile_menu, do_click=True)
    #    time.sleep(1)
    driver.log('def %s\n' % (a223_goto_main_menu.__name__, ))
    remove_fucking_noisy_popup(driver)
    dest = None
    mega_menus = driver.find_elements_by_css_selector('#header .navbar-default .container>ul>li')
    random.shuffle(mega_menus)
    #mega_menus = mega_menus[1:2]
    for menu in mega_menus:
        driver.scroll_to_element(menu)
        menu_class = driver.get_attribute(menu, 'class')
        if menu_class and 'with-sub-menu' in menu_class:
            a_menu = menu.find_element_by_tag_name('a')
            driver.scroll_to_element(a_menu)
            driver.move_to_element(a_menu)
            submenus = menu.find_elements_by_css_selector('ul li a')
            random.shuffle(submenus)
            for submenu in submenus:
                if driver.is_element_visible(submenu):
                    dest = submenu
                    break
        else:
            if driver.is_element_visible(menu):
                dest = menu
        if dest:
            break
    if dest:
        #driver.emulate_mouse_move()
        driver.move_to_element(dest, do_click=True)
        time.sleep(2)
        alt_yandex_adv(driver)

def a223_goto_bottom_menu(driver):
    """Переход по нижнему меню"""
    driver.log('def %s\n' % (a223_goto_bottom_menu.__name__, ))

    menus = driver.find_elements_by_css_selector('footer .box-information ul li a')
    random.shuffle(menus)
    for menu in menus:
        driver.scroll_to_element(menu)
        if driver.is_element_visible(menu):
            href = driver.get_attribute(menu, 'href')
            # Пустая страничка
            if '/free-call/' in href:
                continue
            driver.emulate_mouse_move()
            driver.move_to_element(menu, do_click=True)
            time.sleep(2)
            alt_yandex_adv(driver)
            break

def a223_goto_catalogue(driver):
    """Переход по каталогу слева"""
    driver.log('def %s\n' % (a223_goto_catalogue.__name__, ))

    menus = driver.find_elements_by_css_selector('#column-left ul li a')
    random.shuffle(menus)
    for menu in menus:
        driver.scroll_to_element(menu)
        if driver.is_element_visible(menu):
            driver.emulate_mouse_move()
            driver.move_to_element(menu, do_click=True)
            break

def a223_goto_random_company(driver):
    """Переход в случайную компанию"""
    driver.log('def %s\n' % (a223_goto_random_company.__name__, ))

    company = find_random_company(driver)
    if not company:
        return
    company_title = company.find_element_by_css_selector('.right-block .caption h4 a')
    driver.scroll_to_element(company_title)
    if driver.is_element_visible(company_title):
        driver.emulate_mouse_move()
        driver.move_to_element(company_title, do_click=True)
        time.sleep(2)
        alt_yandex_adv(driver)

def a223_goto_cat_or_prices(driver):
    """Переход в раздел каталог/товары"""
    driver.log('def %s\n' % (a223_goto_cat_or_prices.__name__, ))

    links_classes = ['all', 'cat', 'prices']
    random.shuffle(links_classes)
    a223_goto_search_page(driver, links_classes[0])

def goto223(driver):
    """Переход на 223 если мы еще не там"""
    if not '223-223.ru' in driver.get_current_url():
        driver.goto('https://223-223.ru/')
        driver.emulate_mouse_move()
    alt_yandex_adv(driver)

def auth223(driver):
    """Авторизация на сайте 223-223.ru"""
    signin = driver.find_elements_by_css_selector('li.signin a')
    if signin:
        signin = signin[0]
        href = driver.get_attribute(signin, 'href')
        if '/profile/' in href:
            return

        driver.move_to_element(signin, do_click=True)
        time.sleep(3)
        alt_yandex_adv(driver)

        driver.wait(EC.presence_of_element_located((By.ID, 'input-email')))
        driver.emulate_mouse_move()
        email_input = driver.find_element_by_id('input-email')
        driver.move_to_element(email_input, do_click=True)

        # Логин и пароль должны быть одинаковыми
        login = driver.profile_name
        driver.fill_input(email_input, '%s@223-223.ru' % (login, ))
        passwd_input = driver.find_element_by_id('input-password')
        driver.fill_input(passwd_input, login)
        passwd_input.send_keys(Keys.RETURN)
        time.sleep(3)

def gotosite_from223(driver, by: int = 3):
    """Сценарий перехода на сайты компаний
       :param by: количество сайтов для посещения
    """
    sites = requests.get('https://223-223.ru/media/client_sites.txt').json()
    # Не тасуем - идем по driver.total_starts_counter по порядку
    ###random.shuffle(sites)

    point = driver.total_starts_counter*by
    i = driver.simpler(point, len(sites))

    pks = sites[i:i+by]

    for i, pk in enumerate(pks):
        driver.goto('https://223-223.ru/company/%s/' % (pk, ))
        driver.emulate_mouse_move()
        links = driver.find_elements_by_css_selector('.gotosite')
        for link in links:
            org_pk = driver.get_attribute(link, 'data-org-pk')
            if org_pk:
                driver.scroll_to_element(link)
                driver.move_to_element(link, do_click=True)
                href = driver.get_attribute(link, 'href')
                time.sleep(2)
                driver.switch_to_window(driver.window_handles()[-1])
                time.sleep(2)
                driver.pretend_user()
                time.sleep(2)
                driver.pretend_user()
                # Пишем результат
                driver.result.append(pk)

                driver.messages.append('%s - %s' % (href, org_pk))
                driver.close_current_window()
                time.sleep(2)
                driver.switch_to_window(driver.window_handles()[-1])
                time.sleep(2)
                break
    time.sleep(2)

    # Обновление статистики в файле
    stata_folder = os.path.split(driver.profile_dir)[0]
    stata_folder = os.path.split(stata_folder)[0]
    stata_folder = os.path.join(stata_folder, 'stata')
    logger.info('stata folder %s' % (stata_folder, ))
    if not os.path.exists(stata_folder):
        os.mkdir(stata_folder)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    fname = '%s.json' % os.path.join(stata_folder, today)
    result = []
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            result = json.loads(f.read())
    result.append({driver.profile_name: driver.result})
    with open(fname, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(result))

    return

def get_new_scenario(driver):
    """Выбрать сценарий для работы
       для потрахивания яндекс рекламы
    """
    scenarios = [
        (visit_yandex, goto223, auth223, a223_goto_search_page, a223_do_search, goto_yandex_adv),
        (visit_yandex, goto223, auth223, a223_goto_main_menu, a223_goto_cat_or_prices, a223_do_search, goto_yandex_adv),
        (visit_yandex, goto223, auth223, a223_goto_bottom_menu, a223_goto_cat_or_prices, a223_do_search, goto_yandex_adv),
        (visit_yandex, goto223, auth223, a223_goto_cat_or_prices, a223_do_search, a223_goto_random_company, goto_yandex_adv),
        (visit_yandex, goto223, auth223, a223_goto_cat_or_prices, a223_do_search, company_bustling_on_listing, goto_yandex_adv),
    ]
    random.shuffle(scenarios)
    scenario = scenarios[0]
    driver.log('scenario %s' % ([action.__name__ for action in scenarios[0]], ))
    return scenario

# -------------------------------
# Передаем фикстуру инициализации
# https://selenium-python.readthedocs.io/locating-elements.html
# -------------------------------
def test_main(original_driver):
    logger.info('[STARTED]: %s' % (datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y'), ))
    driver = original_driver.instance

    # Проверка перехода со ссылки википедии
    #driver.goto('https://ru.wikipedia.org/wiki/Монтажная_пена')
    #driver.emulate_mouse_move()
    #selector = '#mw-content-text a'
    #links = driver.find_elements_by_css_selector(selector)
    #ind = random.randint(0, len(links))
    #driver.obibon_link(selector, ind, 'https://223-223.ru/q/монтажная пена/')
    #driver.emulate_mouse_move()
    #driver.scroll_to_element(links[ind])
    #driver.move_to_element(links[ind], do_click=True)
    #time.sleep(30)
    #return

    proxies = {}
    if PROXY:
        proxies = {
            'http'  : PROXY,
            'https' : PROXY,
        }

    balance = get_yandex_adv_clicks(proxies=proxies)
    fbalance = list(filter(lambda x:x.get('partner_wo_nds', ''), balance))
    if fbalance:
        balance = fbalance[0]['partner_wo_nds']
    ip = get_ip()
    driver.messages.append('%s - %s - %s' % (balance, driver.profile_name, ip))
    driver.messages.append('hd: %s' % get_hd_space()['percent'])
    # ---------------------------
    # Сценарий переход по рекламе
    # ---------------------------
    #driver.goto('https://223-223.ru/prices/')
    #goto_yandex_adv(driver)

    # ------------------------
    # Сценарий переход по меню
    # ------------------------
    #driver.goto('https://223-223.ru/')
    #a223_goto_search_page(driver, 'work')

    # ---------------
    # Сценарий поиска
    # ---------------
    #driver.goto('https://223-223.ru/')
    #a223_do_search(driver)

    # ----------------------------------
    # Сценарий перехода по главному меню
    # ----------------------------------
    #driver.goto('https://223-223.ru/')
    #a223_goto_main_menu(driver)

    # ---------------------------------
    # Сценарий перехода по нижнему меню
    # ---------------------------------
    #driver.goto('https://223-223.ru/')
    #a223_goto_bottom_menu(driver)

    # -------------------------------------
    # Сценарий перехода по каталогу (слева)
    # -------------------------------------
    #driver.goto('https://223-223.ru/cat/')
    #a223_goto_catalogue(driver)

    # -----------------------------------
    # Сценарий перехода в случайную фирму
    # -----------------------------------
    #driver.goto('https://223-223.ru/cat/')
    #a223_goto_random_company(driver)

    # ----------------------------------
    # Сценарий перехода на сайт компании
    # ----------------------------------
    #gotosite_from223(driver)
    #return

    # -------------------------------------
    # Сценарий перехода на по гугль рекламе
    # -------------------------------------
    #driver.goto('https://223-223.ru/')
    #a223_do_search(driver)
    #goto_google_adv(driver)
    #return

    # ----------------------------------
    # Сценарий авторизации на 223-223.ru
    # ----------------------------------
    #driver.goto('https://223-223.ru')
    #auth223(driver)
    #return

    adv_visited = False
    for i in range(SEARCH_YANDEX_ADV_TRIES):
        if adv_visited:
            break
        scenario = get_new_scenario(driver)
        #scenario = (goto223, a223_do_search, goto_yandex_adv)
        for action in scenario:
            try:
                result = action(driver)
            except Exception as e:
                err = 'err: %s on action %s' % (e, action)
                logger.error(err)
                driver.messages.append(err)
                break
            if action == goto_yandex_adv and result:
                adv_visited = True
    try:
        driver.window_handles()
    except Exception as e:
        err = '[ERROR]: %s, setup driver again' % e
        logger.error(err)
        driver.messages.append(err)
        driver.setup_chrome()
        goto223(driver)
        time.sleep(15)

    if VISIT_223_SITES:
        try:
            gotosite_from223(driver)
        except Exception as e:
            err = 'err: %s on gotosite' % e
            logger.error(err)
            driver.messages.append(err)
    time.sleep(5)
    driver.success = True # Завершение без ошибок
