import os
import json
import time
import datetime
import random
import sys
import logging
import requests

import pytest

from browser import Browser
from plugins.utils import get_hd_space, driver_versions, inform_server

from envparse import env
env.read_envfile()
PROXY = env('PROXY', default=None)
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = env('TELEGRAM_CHAT_ID')
HEADLESS = env('HEADLESS', cast=bool, default=False)
DRIVER_TYPE = env('DRIVER_TYPE')
SEARCH_YANDEX_ADV_TRIES = 2
QUEUE_PROFILES = True
MULTIPLE_START = env('MULTIPLE_START', cast=bool, default=False)
LOAD_ALT_YANDEX_ADV = env('LOAD_ALT_YANDEX_ADV', cast=bool, default=False)

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

"""
0) локер на работающий профиль
   создать апи для получения ip
1) в идеале разделить мобильного пользователя и десктопного
  1.1) в ua.json добавить флаг мобильный/десктоп и считывать в browser
  1.2) подправить движения мыши и клики для мобильного пользователя
2) пересоздание профиля с сохранением credentials/ua/screen
  2.1) подумать как с сервера дать команду на перезаполнение всех профилей
"""

# ------------------------
# Usage: pytest example.py
# $ pytest example.py -s,
# чтобы stdout писался
# ------------------------

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
        #'proxy': 'http://10.10.3.1:3128',
        #'proxy': 'http://10.10.7.1:3128',
        #'proxy': 'http://10.10.2.1:3128',
        #'proxy': 'http://10.10.8.1:3128',
        #'proxy': 'http://10.10.11.1:3128',
        #'proxy_percent': 100,
        #'custom_profile': '/home/jocker/selenium/profiles/palus/palus7',

        'custom_profile': 'marolisa',
        #'custom_profile': 'ejik', # for rubrics

        #'custom_profile_arr': ['bbugoga5', 'bbugoga6', ],
        #'queue_profiles': QUEUE_PROFILES,
        #'headless': False, #HEADLESS,
        'headless': True, #HEADLESS,
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
        'debug_performance': False,
    }
    wd = Browser(**kwargs).get_driver()

    def fin():
        """Альтернативный финализер для фикстуры
           он выполнится в любом случае, после того
           как выполнится основной тест, в конце
           основного теста можно задать переменную и,
           если она здесь отсутсвуте, тогда мы знаем,
           что в основном тесте произошла ошибка"""
        print('--- Before fixture exit', wd.instance.success)
        wd.instance.save_profile() # для хитрожопого firefox
        wd.quit()
        wd.instance.clear_profile()
        print('--- Fixture succeeded', wd.instance.success)

    request.addfinalizer(fin)
    #request.addfinalizer(wd.quit)
    return wd

def parse2gis(driver):
    """Парсинг 2gis сайта мобильной версии"""
    CODE_PAGE_NOT_FOUND = 'PAGE_NOT_FOUND'
    expired_time = 24*60*60

    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.88 Mobile/15E148 Safari/604.1'
    dest_folder = '2gis'
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)

    def do_request(url):
        """Запрос на апи"""
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        json_data = r.json()
        return json_data

    def repeatable_action(func, *args, **kwargs):
        """Декоратор для функции, которую надо повторить, если завалится"""
        def wrapper(*args, **kwargs):
            for i in range(3):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print('[FAILED]: try', i, 'func', func, 'args', args, 'kwargs', kwargs)
                    print('[ERROR]:', e)
                    time.sleep(0.25)
            raise Exception('repeatable action failed')
        return wrapper

    def goto2gis():
        driver.goto('https://2gis.ru/moscow')

    def find_rubrics(search_root: bool = False):
        """Находим рубрики"""
        rubricator_selector = '.searchBar__rubricator'
        if search_root:
            rubricator_selector = '.rubricator__root'
        return driver.find_elements_by_css_selector('%s a.metarubrics__item' % rubricator_selector)

    def pick_other_rubric(search_root: bool = False):
        """Выбрать рубрику "Остальное"
        """
        rubrics = find_rubrics(search_root)
        for rubric in rubrics:
            title = driver.get_attribute(rubric, 'title')
            if title == 'Остальное':
                rubric.click()
                return True
        return False

    def pick_more_rubric(search_root: bool = True):
        """Выбрать рубрику "Ещё"
        """
        rubrics = find_rubrics(search_root)
        for rubric in rubrics:
            title = driver.get_attribute(rubric, 'title')
            if title == 'Ещё':
                rubric.click()
                return True
        return False

    def back_button(search_root: bool = False):
        """Кнопка назад"""
        css_selector = '.suggester__main .suggester__backArrow a.suggester___link'
        if search_root:
            css_selector = '.rubricator__backArrowWrapper'
        buttons = driver.find_elements_by_css_selector(css_selector)
        buttons[0].click()

    def get_requests(url_filter: str = None):
        """Смотрим запросы"""
        urls = []
        default_url = 'https://catalog.api.2gis.ru/3.0/'
        for r in driver.get_requests():
            if url_filter:
                if not r['url'].startswith(default_url + url_filter):
                    continue
            urls.append(r['url'])
        driver.clear_requests()
        return urls

    def get_add_company_button(debug_msg: str = ''):
        """Когда появляется кнопка "Добавить организацию", значит,
           скрола больше нет
        """
        add_button = driver.find_elements_by_css_selector('.addFirm__root')
        if add_button:
            if debug_msg:
                print(debug_msg)
            return True
        return False

    def scroll2bottom_listing():
        """На страничке листинга доскроллить до низу"""
        driver.driver.execute_script("""
var content_container = document.querySelector(".searchResults__content");
content_container.scrollTo(0, content_container.scrollHeight);
""")

    def expand_listing():
        """Нажать на разворачивание листинга"""
        time.sleep(0.5)
        driver.driver.execute_script("""
var content_container = document.querySelector(".searchResults__content");
content_container.click();
""")

    def wait_for_search_results():
        """Ожидаем какое-то время появление листинга"""
        for i in range(5):
            if driver.find_elements_by_css_selector('.searchResults__content'):
                return True
            time.sleep(0.5)
        return False

    def fill_rubrics_arr(result: dict):
        """Вспомогательная функция для заполнения массива рубрик
           по найденным веб-элементам
           :param result: результат аккумуляции
        """
        urls = get_requests(url_filter='rubricator/list')

        if len(urls) == 1:
            json_data = do_request(urls[0])
            rubrics = json_data['result']['items']

        for rubric in rubrics:
            if not 'id' in rubric or not 'name' in rubric:
                #print('pass', rubric)
                continue
            rid = rubric['id']
            rname = rubric['name']
            if not rid in result:
                result[rname] = {
                    'id': rid,
                    'rname': rname,
                    'subrubrics': {},
                }

    def analyze_subrubrics(result: dict):
        """Анализ подуровня рубрики"""
        for i in range(len(find_rubrics(True))):
            rubric = find_rubrics(True)[i]
            href = driver.get_attribute(rubric, 'href')
            rname = driver.get_attribute(rubric, 'title')
            # Если в адресе /rubrics/ - идем ниже
            if not '/rubrics/' in href:
                continue
            rubric.click()
            time.sleep(1)
            fill_rubrics_arr(result[rname]['subrubrics'])

            # Спускаемся еще глубже (третий уровень отличается)
            analyze_subrubrics(result[rname]['subrubrics'])

            back_button(True)
            time.sleep(1)
            driver.clear_requests()

    def analyze_rubrics():
        """Анализ рубрик
           с помощью fill_rubrics_arr
                     analyze_subrubrics
           собирается полная структура рубрик
        """
        result = {}
        goto2gis()

        pick_other_rubric() # Тут будет "Остальное"
        time.sleep(2)
        fill_rubrics_arr(result)
        analyze_subrubrics(result)
        driver.json_pretty_print(result)

        dest = os.path.join(dest_folder, 'rubrics.json')
        with open(dest, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(result))
        return result

    def load_rubrics_file():
        """Загрузить данные по рубрикам из файла"""
        rubrics_file = os.path.join(dest_folder, 'rubrics.json')
        with open(rubrics_file, 'r', encoding='utf-8') as f:
            rubrics = json.loads(f.read())
        return rubrics

    def rubrics_progress_file(result: dict = None):
        """Сохранить данные по процессу парсинга рубрика в файл
           :param result: результат для сохранения,
                          если его нет, вытаскиваем с файла
        """
        dest = os.path.join(dest_folder, 'rubrics_progress.json')
        if result:
            with open(dest, 'w+', encoding='utf-8') as f:
                f.write(json.dumps(result))
        else:
            if not os.path.exists(dest):
                return {}
            with open(dest, 'r', encoding='utf-8') as f:
                return json.loads(f.read())

    def click_by_company(company_id: str):
        """Жмак на компанию, т/к страничка перестраивается, надо в try
           Мы должны быть на списке компаний
        """
        for link in driver.find_elements_by_css_selector('.searchResults__content article .minicardPlain__header a'):
            href = driver.get_attribute(link, 'href')
            if href and href.endswith(company_id):
                driver.clear_requests()
                link.location_once_scrolled_into_view
                link.click()
                return True
        return False

    def make_search(name: str, company_id: str):
        """Поиск по названию"""
        inp = driver.find_element_by_css_selector('.suggester__input')
        inp.click()

        clear_button = driver.find_elements_by_css_selector('.suggester__clear')
        if clear_button:
            clear_button[0].click()

        driver.send_keys(inp, name + '\n')
        wait_for_search_results()
        for i in range(5):
            if get_add_company_button():
                break
            scroll2bottom_listing()
            time.sleep(0.5)

        expand_listing()
        for i in range(5):
            try:
                return click_by_company(company_id)
            except Exception as e:
                print(e)
        return False

    def search_company_by_name(pk: str, name: str,
                               to_folder: str = '',
                               pass_exists: bool = False):
        """Поиск организации по названию
           Мы должны быть на страничке поиска
        """
        company_id = pk.split('_')[0]
        companies_folder = os.path.join(to_folder, 'companies')
        dest = os.path.join(companies_folder, '%s.json' % company_id)

        if pass_exists and os.path.exists(dest):
            return

        if not make_search(name, company_id):
            print('[ERROR]: make_search failed', name, company_id)
            return
        for i in range(5):
            urls = get_requests(url_filter='items/byid')
            if urls:
                break
            time.sleep(0.5)

        if len(urls) == 1:
            json_data = do_request(urls[0])
            obj = json_data['result']['items'][0]

            companies_folder = os.path.join(to_folder, 'companies')
            if not os.path.exists(companies_folder):
                os.mkdir(companies_folder)
            dest = os.path.join(companies_folder, '%s.json' % company_id)
            with open(dest, 'w+', encoding='utf-8') as f:
                f.write(json.dumps(obj))
        else:
            print('[ERROR]: urls not equal 1', urls)

    def fetch_companies(rname, rsname, pass_exists: bool = False):
        """Получение компаний по рубрике и подрубрике"""
        goto2gis()
        time.sleep(1)
        folder = os.path.join(dest_folder, rname, rsname)
        for item in os.listdir(folder):
            path = os.path.join(folder, item)
            if path.endswith('.json'):
                with open(path, 'r', encoding='utf-8') as f:
                    companies = json.loads(f.read())
                for company in companies:
                    search_company_by_name(company['id'], company['name'], folder, pass_exists)
                    #back_button()

    # -------
    # DESKTOP
    # -------
    def wait_for_network(url_filter: str = 'items'):
        """Ожидаем пока приедет джисонина для спижжувания
           приезджает content-encoding: br,
           поэтому с декодированием не будем мучаться,
           просто возьмем ссыль и перезапросим ее
        """
        default_url = 'https://catalog.api.2gis.ru/3.0/'

        for i in range(10):
            items = driver.get_requests(url_filter=default_url + url_filter)
            if items:
                return items[0]['url']
            time.sleep(0.5)

    def desktop_find_paginator_container(rubric_id: str):
        """Найти контейнер с пагинацией
           Мы должны быть в рубрике
           :param rubric_id: идентификатор рубрики
        """
        all_links = driver.find_elements_by_tag_name('a')
        for link in all_links:
            href = driver.get_attribute(link, 'href')
            if href and '%s/page/' % rubric_id in href:
                return driver.find_parent(link)

    @repeatable_action
    def desktop_find_paginator_links(rubric_id: str):
        """Найти ссылки на постраничную навигацию
           Мы должны быть в рубрике
           :param rubric_id: идентификатор рубрики
        """
        paginator_container = desktop_find_paginator_container(rubric_id)
        paginator_links = paginator_container.find_elements_by_tag_name('a')
        pages = [
            driver.get_attribute(paginator_link, 'href')
            for paginator_link in paginator_links
        ]
        return pages

    def desktop_find_paginator_el(rubric_id: str, page: int):
        """Найти элемент-ссылку в постраничной навигации на нужную страничку
           Мы должны быть в рубрике
           :param rubric_id: идентификатор рубрики
           :param page: номер запрашиваемой странички
        """
        paginator_container = desktop_find_paginator_container(rubric_id)
        paginator_links = paginator_container.find_elements_by_tag_name('a')
        for link in paginator_links:
            href = driver.get_attribute(link, 'href')
            if page == 1 and href.endswith('rubricId/%s' % rubric_id):
                return link
            elif href and href.endswith('rubricId/%s/page/%s' % (rubric_id, page)):
                return link

    def desktop_listing_scroll2bottom(paginator_container):
        """На страничке листинга доскроллить до низу"""
        driver.driver.execute_script("""
console.log(arguments[0]);
console.log(arguments[0].scrollHeight);
arguments[0].scrollTo(0, arguments[0].scrollHeight);
""", paginator_container)

    def wait_for_listing_url(rubric_id: str, page_number: int):
        """Подождать пока url совпадет
           :param rubric_id: ид рубрики
           :param page_number: номер странички
        """
        for i in range(10):
            cur_url = driver.get_current_url()
            if page_number == 1 and 'rubricId/%s?' % rubric_id in cur_url:
                return True
            elif 'rubricId/%s/page/%s' % (rubric_id, page_number) in cur_url:
                return True
            time.sleep(0.5)
        print('[ERROR]: we wait for url and failed', rubric_id, page_number)
        return False

    def build_rubric_link(subrubric: dict):
        """Построить ссылку для рубрики
           ссылка на рубрику формируется из названия и ид
           https://2gis.ru/moscow/search/Кафе-кондитерские %2F Кофейни/rubricId/162
           :param subrubric: словарь с ид и названием рубрики
        """
        rsname = subrubric['rname']
        return 'https://2gis.ru/moscow/search/%s/rubricId/%s' % (
            rsname.replace('/', '%2F'),
            subrubric['id'],
        )

    def build_rubric_folder(parent_folder: str, subrubric: dict):
        """Построить путь к папке для рубрики
           :param parent_folder: родительская папка
           :param subrubric: словарь с ид и названием рубрики
        """
        rsname = subrubric['rname']
        rsfolder = os.path.join(parent_folder, rsname.replace('/', '_'))
        if not os.path.exists(rsfolder):
            os.mkdir(rsfolder)

        companies_folder = os.path.join(rsfolder, 'companies')
        if not os.path.exists(companies_folder):
            os.mkdir(companies_folder)

        return rsfolder

    def desktop_find_listing_main_container(subrubric_id: int, page_number: int):
        """Находим главный контейнер в котором лежат
           пагинация и все конторы для протыкивания-спижжувания
        """
        page_el = desktop_find_paginator_el(subrubric_id, page_number)
        if not page_el:
            print('[ERROR]: page not found', page_number)
            return

        paginator_parent = driver.find_parent(page_el) # div
        paginator_parent_parent = driver.find_parent(paginator_parent) # div
        preparent = driver.find_parent(paginator_parent_parent) # div
        main_container = driver.find_parent(preparent)
        return main_container

    def get_company_id_from_link(link: str):
        """Получить ид компании из ссылки
           ссылка на компанию строится так
           /moscow/firm/70000001044632446?stat=...
        """
        if not '/moscow/firm/' in link:
            return
        return link.split('/')[-1].split('?')[0]

    def parse_companies(main_container, rsfolder: str, force_update: bool = False):
        """Протыкиваем компании
           вроде не перестраивается на десктопе
           можно протыкать массово
           :param main_container: главный контейнер где все говнище лежит
           :param rsfolder: папка для компаний
           :param force_update: принудительное обновление
        """
        companies = {}
        companies_folder = os.path.join(rsfolder, 'companies')

        all_links = main_container.find_elements_by_tag_name('a')
        for link in all_links:
            href = driver.get_attribute(link, 'href')
            company_id = get_company_id_from_link(href)
            if company_id and not company_id in companies:
                companies[company_id] = link
        for company_id, company_el in companies.items():
            dest = os.path.join(companies_folder, '%s.json' % company_id)
            if os.path.exists(dest) and not force_update:
                continue

            driver.just_scroll_to(company_el)
            company_el.click()
            for i in range(10):
                urls = get_requests(url_filter='items/byid')
                if urls:
                    break
                time.sleep(0.5)

            if len(urls) == 1:
                json_data = do_request(urls[0])

                if not 'result' in json_data or not 'items' in json_data['result']:
                    print('[ERROR]: result is incorrect', json_data)
                    continue

                obj = json_data['result']['items'][0]
                with open(dest, 'w+', encoding='utf-8') as f:
                    f.write(json.dumps(obj))
            else:
                print('[ERROR]: fetch company failed', company_id)


    def desktop_parse_rubric_page(rfolder: str,
                                  subrubric: dict,
                                  page_number: int = 2):
        """На десктопе спарсиваем страничку рубрики
           :param rfolder: папка родительской рубрики
           :param subrubric: подрубрика из rubrics.json
        """
        rsname = subrubric['rname']
        href = build_rubric_link(subrubric)
        rsfolder = build_rubric_folder(rfolder, subrubric)
        subrubric_id = subrubric['id']
        pages = desktop_find_paginator_links(subrubric_id)
        if not pages:
            print('[ERROR]: paginator not found')
            return
        page_el = desktop_find_paginator_el(subrubric_id, page_number)
        if not page_el:
            print('[ERROR]: page not found', page_number)
            return CODE_PAGE_NOT_FOUND

        # Находим ибучий контейнер, там tabindex=-1,
        # чтобы подскролить вниз
        main_container = desktop_find_listing_main_container(subrubric_id, page_number)
        if not main_container:
            print('[ERROR]: main_container not found', page_number)
            return

        parse_companies(main_container, rsfolder)

        desktop_listing_scroll2bottom(main_container)
        # Ибашим на страничку и собираем запросы
        driver.clear_requests()
        page_el.click()

        url = wait_for_network()
        if not url:
            print('[ERROR]: network error fetch page', page_number)
            return
        # Перезапрашиваем данные для спижжувания
        json_data = do_request(url)
        if not 'result' in json_data or not 'items' in json_data['result']:
            print('[ERROR]: result is incorrect', json_data)
            return
        dest = os.path.join(rsfolder, '%s.json' % page_number)
        with open(dest, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(json_data['result']['items']))

    def desktop_parse_rubric(rfolder: str, subrubric: dict):
        """На десктопе спарсиваем рубрику постранично
           :param rfolder: папка родительской рубрики
           :param subrubric: подрубрика из rubrics.json
        """
        href = build_rubric_link(subrubric)
        driver.goto(href)

        # чтобы собрать данные с первой странички
        # делаем туда-суда-обратно
        desktop_parse_rubric_page(rfolder, subrubric, 2)
        desktop_parse_rubric_page(rfolder, subrubric, 1)
        for i in range(3, 500):
            code = desktop_parse_rubric_page(rfolder, subrubric, i)
            if code == CODE_PAGE_NOT_FOUND:
                break

    def is_time_to_parse(rid):
        """LOCAL Механизм задачности/прогресса,
           когда мы отдаем только 1 нераспарсенную рубрику
           ставим ей время, чтобы ее пока не трогать
           :param rid: ид рубрики
        """
        now = time.time()
        progress = rubrics_progress_file()
        expired = now - expired_time
        if rid in progress and progress[rid] > expired:
            print('[PASSING]', rid)
            return False
        progress[rid] = now
        rubrics_progress_file(progress)
        return True

    def desktop_parse_rubrics(rubrics: dict = None, rfolder: str = None, lvl: int = 0):
        """На десктопе постраничная навигация
           для сдалбливания листинга постранично
           Например, https://2gis.ru/moscow/search/%D0%90%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B9%D0%BA%D0%B8/rubricId/405
           надо сбегать на вторую страничку,
           затем на первую,
           затем на третью и дальше по порядку
           карта обязательно должна быть видна, иначе обломинго
        """
        if not rubrics:
            rubrics = load_rubrics_file()

        for rname, data in rubrics.items():
            rid = data['id']
            print('\t' * lvl, rname, rid)
            if not rfolder:
                folder = os.path.join(dest_folder, rname.replace('/', '_'))
            else:
                folder = os.path.join(rfolder, rname.replace('/', '_'))

            if not os.path.exists(folder):
                os.mkdir(folder)

            if data['subrubrics']:
                desktop_parse_rubrics(data['subrubrics'], folder, lvl + 1)
                print(folder)
            else:
                if is_time_to_parse(rid):
                    print('--- parsing ---')
                    driver.json_pretty_print(data)
                    desktop_parse_rubric(rfolder, data)

                    return

    # Формируем файл рубрик и подрубрик на мвс
    #analyze_rubrics()

    # Парсим конторы по рубрикам на десктопе
    desktop_parse_rubrics()



"""
Сверяться с 2гисной апи
https://docs.2gis.com/ru/api/search/places/reference/2.0/catalog/branch/get


На мобилке классы не обфусцированы, поэтому на мобилке собираем данные по рубрикам

А на десктопе собираем данные постранично в каталоге

Чтобы спарсить 2гисину, надо сначала собрать все рубрики и подрубрики,
затем по джисонинам идем и через поиск находим каждую компанию и пишем ее джисонину

По логотипам, например, изображение 300х300 можно получить так
https://ams2-cdn.2gis.com/previews/1049444286191370473/384a9684-f95a-445d-be34-054a45d1e02b/1/image_300x300.png?api-version=2.0

1049444286191370473
384a9684-f95a-445d-be34-054a45d1e02b
приезджают и в листинг и в карточку товара в logo/img_url

"""

# -------------------------------
# Передаем фикстуру инициализации
# https://selenium-python.readthedocs.io/locating-elements.html
# -------------------------------
def test_main(original_driver):
    driver = original_driver.instance
    parse2gis(driver)
    #driver.test_mode()
    time.sleep(3)
