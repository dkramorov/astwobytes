#-*- coding:utf-8 -*-
import logging
import datetime
import requests
from lxml import html

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.functions import object_fields
from apps.main_functions.date_time import date_plus_days, str_to_date
from apps.main_functions.string_parser import kill_html

from apps.afisha.models import (Rubrics,
                                Places,
                                RGenres,
                                REvents,
                                RSeances, )

logger = logging.getLogger(__name__)

root_url = "https://www.irk.ru"
url_places = "{}{}".format(root_url, "/guide/")
today = datetime.date.today()


def get_rubrics():
    """Получить все рубрики и жанры"""
    rubrics = []
    genres = []
    content = requests.get(url_places).text
    tree = html.fromstring(content)
    # -----
    # Жанры
    # -----
    genres_rows = tree.xpath('.//*[@class="b-content-header-menu"]/li/a')
    for item in genres_rows:
        link = item.attrib.get('href')
        if not link or not item.text:
            continue
        if not link.startswith('/afisha/'):
            continue
        if link == '/afisha/':
            continue
        name = item.text.strip()
        analogs = RGenres.objects.filter(tag=link)
        if analogs:
            analog = analogs[0]
        else:
            analog = RGenres.objects.create(tag=link)
        analog.name = name
        analog.find_genre_altname()
        analog.save()
        genres.append(analog)
    # -----
    # Места
    # -----
    places_rows = tree.xpath('.//*[@class="place-cat__item"]/a')
    for item in places_rows:
        link = item.attrib.get('href')
        name = item.text.strip()
        analogs = Rubrics.objects.filter(tag=link)
        if analogs:
            analog = analogs[0]
        else:
            analog = Rubrics.objects.create(tag=link)
        analog.name = name
        analog.save()
        rubrics.append(analog)
    return (rubrics, genres)

def get_cinema_seances(date=None):
    """Подтаскиваем все сеансы по дате"""
    if not date:
        date = datetime.date.today()
        day = date.strftime('%Y%m%d')
    else:
        day = date.strftime('%Y%m%d')

    tag = '/afisha/cinema/'
    urla_cinema = '{}{}{}/'.format(root_url, tag, day)

    logger.info('{} get_cinema_seances => {}'.format(day, urla_cinema))

    content = requests.get(urla_cinema).text
    tree = html.fromstring(content)

    containers = tree.xpath('.//*[@class="grid-inner"]/div/div/ul/li')
    for container in containers:
        # ----------------------
        # Узнаем, что за событие
        # ----------------------
        event_links = container.xpath('.//*[@class="cinema-list__title"]/a')
        if len(event_links) == 0:
            continue

        event_link = event_links[0].attrib.get("href")
        event_tag = event_link.split("/")[-2]
        event_analogs = REvents.objects.filter(tag=event_tag)
        if event_analogs:
            event = event_analogs[0]
        else:
            # ----------------------------
            # Событие отсутствует,
            # надо его срочно спиздофонить
            # ----------------------------
            imga = container.xpath('.//*[@class="cinema-list__image-link"]/img')
            if imga:
                imga = imga[0].attrib.get('src')
            else:
                imga = None
            event = get_cinema_event(event_link, imga)
        # --------------------
        # Узнаем, что за место
        # Узнаем сеансы
        # --------------------
        trs = container.xpath('.//table/tr')
        for tr in trs:
            place = tr.xpath('.//th/a')[0]
            place_link = place.attrib.get('href')
            place_tag = place_link.split('/')[-3]
            place_analogs = Places.objects.filter(tag=place_tag)
            if place_analogs:
                place = place_analogs[0]
            else:
                place = get_place(place_link, place_tag)

            seances = tr.xpath('.//td/ul/li')
            for seance in seances:
                t = seance.xpath('.//time')
                if t:
                    t = t[0].text.strip()
                    hours, minutes = t.split(':')
                    analogs = RSeances.objects.filter(event = event,
                                                      place = place,
                                                      date = date,
                                                      hours = hours,
                                                      minutes = minutes, )
                    if not analogs:
                        new_seance = RSeances.objects.create(event = event,
                                                             place = place,
                                                             date = date,
                                                             hours = hours,
                                                             minutes = minutes, )

def get_cinema_event(link, imga_link):
    """Подтаскиваем событие, если его нет"""
    url = '{}{}'.format(root_url, link)
    logger.info('get_cinema_event => {}'.format(url))
    content = requests.get(url).text
    tree = html.fromstring(content)
    container = tree.xpath('.//*[@class="grid-inner"]')[0]

    tag = link.split('/')[-2]
    analogs = REvents.objects.filter(tag=tag)
    if analogs:
        analog = analogs[0]
    else:
        analog = REvents.objects.create(tag=tag)

    # /afisha/cinema/20190125/44696/
    # Разбиваем по первой цифре года
    rgenre = RGenres.objects.get(tag=link.split('2')[0])
    analog.rgenre = rgenre
    # --------------------
    # Загрузка изображения
    # --------------------
    if imga_link:
        analog.upload_img(imga_link)

    title = container.xpath('.//h1')[0].text.strip()
    analog.name = title
    details = []
    info = container.xpath('.//*[@class="cinema-list__labels cinema-list__labels_read"]')[0]
    for item in info:
        if item.tag.lower() == 'span':
            detail = item.xpath('.//b')
            if detail:
                details.append(detail[0].text.strip())
            else:
                details.append(item.text.strip())
    if len(details) == 4:
        analog.duration = details[0]
        analog.label = details[1]
        analog.genre = details[2]
        analog.country = details[3]
    else:
        logger.error('--- INFO NOT RECOGNIZED ---')

    desc = ''
    description = container.xpath('.//*[@class="cinema-desc__item cinema-desc__item_text"]/p')
    for item in description:
        if item.text:
            desc += '<p>{}</p>'.format(kill_html(item.text.strip()))
    analog.description = desc

    trailer = container.xpath('.//*[@class="g-video"]/iframe')
    if trailer:
        src = trailer[0].attrib.get('src')
        trailer = html.tostring(trailer[0])
        if '//www.youtube.com' in src:
            analog.trailer = trailer.decode('utf-8')

    actors = container.xpath('.//*[@class="cinema-desc__item cinema-desc__item_aside"]/dl')

    if actors:
        field = None
        values = []
        for actor in actors[0]:
            if actor.tag.lower() == 'dt':
                if field and values:
                    setattr(analog, field, ', '.join(values))
                    values = []
                    field = None
                if 'Режиссер' in actor.text:
                    field = 'producer'
                else:
                    field = 'actors'
            elif actor.tag.lower() == 'dd':
                values.append(actor.text.strip())
        if field and values:
            setattr(analog, field, ', '.join(values))

    # -------------------------------
    # На удивление, тут нет картинки,
    # ее надо дергать с листинга
    # -------------------------------
    logger.info(json_pretty_print(object_fields(analog)))
    analog.save()
    return analog

def get_place(link, tag):
    """Подтаскиваем место, если его нет"""
    url = '{}{}'.format(root_url, link)
    logger.info('get_place => {}'.format(url))
    content = requests.get(url).text
    tree = html.fromstring(content)
    containers = tree.xpath('.//*[@class="grid-inner"]')
    if containers:
        container = containers[0]
    else:
        return None

    place_card = container.xpath('.//*[@class="place-card"]')[0]

    analogs = Places.objects.filter(tag=tag)
    if analogs:
        analog = analogs[0]
    else:
        analog = Places.objects.create(tag=tag)

    title = place_card.xpath('.//h1')[0].text.strip()
    analog.name = title

    imga = place_card.xpath('.//*[@class="place-card__image"]/img')
    if imga:
        imga = imga[0].attrib.get('src')
        analog.upload_img(imga)

    info = place_card.xpath('.//*[@class="place-card__info"]')[0]
    place_phones = []
    for item in info:
        class_item = item.attrib.get('class')
        if 'column_tel' in class_item:
            phones = item.xpath('.//p')
            for phone in phones:
                if phone.text:
                    place_phones.append(phone.text.strip())
        elif 'column_pl' in class_item:
            details = item.xpath('.//p')
            for detail in details:
                worktime = detail.xpath('.//b')
                address = detail.xpath('.//a')
                if worktime:
                    analog.worktime_str = worktime[0].text.strip()
                elif address:
                    analog.address_str = address[0].attrib.get('data-map-address')
        elif 'column_right' in class_item:
            details = item.xpath('.//p/a')
            for item in details:
                href = item.attrib.get('href')
                if 'mailto' in href:
                    analog.email_str = item.text.strip()
                else:
                    analog.site_str = href

    if place_phones:
        analog.phone_str = ', '.join(place_phones)

    logger.info(json_pretty_print(object_fields(analog)))
    analog.save()
    return analog

def get_seances(link, date=None):
    """Подтаскиваем все сеансы по дате"""
    if not date:
        date = datetime.date.today()
        day = date.strftime('%Y%m%d')
    else:
        day = date.strftime('%Y%m%d')

    urla = '{}{}{}/'.format(root_url, link, day)
    logger.info('get_seances => {}'.format(urla))
    content = requests.get(urla).text
    tree = html.fromstring(content)

    containers = tree.xpath('.//*[@class="grid-inner"]/div/ul/li')
    for container in containers:
        # ----------------------
        # Узнаем, что за событие
        # ----------------------
        event_link = container.xpath('.//*[@class="afisha-article__link "]') # Пробел обязательный в классе
        if event_link:
            event_link = event_link[0].attrib.get('href')
            event_tag = event_link.split('/')[-2]
            event = get_event(event_link, date)

def get_event(link, date):
    """Подтаскиваем событие
       Подтаскиваем место
       Подтаскиваем сеанс
       date передается для RSeances"""
    url = '{}{}'.format(root_url, link)
    logger.info('get_event => {}'.format(url))
    content = requests.get(url).text
    tree = html.fromstring(content)
    container = tree.xpath('.//*[@class="grid-inner"]')[0]

    tag = link.split('/')[-2]
    analogs = REvents.objects.filter(tag=tag)
    if analogs:
        analog = analogs[0]
    else:
        analog = REvents.objects.create(tag=tag)

    # /afisha/cinema/20190125/44696/
    # Разбиваем по первой цифре года
    rgenre = RGenres.objects.get(tag=link.split('2')[0])
    analog.rgenre = rgenre
    # --------------------
    # Загрузка изображения
    # --------------------
    if not analog.img:
        imgas = tree.xpath('.//link')
        for imga in imgas:
            if imga.attrib.get('rel') == 'image_src':
                href = imga.attrib.get('href')
                analog.upload_img(href)

    title = container.xpath('.//h1')[0].text.strip()
    analog.name = title

    seance = None
    place = None

    details = []
    info = container.xpath('.//*[@class="cinema-list__labels cinema-list__labels_read"]')[0]
    for item in info:
        if item.tag.lower() == 'span':
            detail = item.xpath('.//b')
            if detail:
                if detail[0].text:
                    if '+' in detail[0].text:
                        analog.label = detail[0].text.strip()
                t = detail[0].xpath('.//time')
                if t:
                    if t[0].text:
                        seance = t[0].text.strip()
            else:
                if item.text:
                    analog.genre = item.text.strip()
        # -------------------------
        # Это ссылка на место, надо
        # его найти или добавить
        # -------------------------
        elif item.tag.lower() == 'a':
            href = item.attrib.get('href')
            if not '/guide/' in href:
                continue
            tag = href.split("/")[-2]
            place_analogs = Places.objects.filter(tag=tag)
            if place_analogs:
                place = place_analogs[0]
            else:
                place = get_place(href, tag)

    if seance:
        hours, minutes = seance.split(':')
        RSeances.objects.create(place=place, event=analog, hours=hours, minutes=minutes, date=date)

    desc = ''
    description = container.xpath('.//*[@class="event-article"]/p')
    for item in description:
        if item.text:
            desc += '<p>{}</p>'.format(kill_html(item.text.strip()))
    analog.description = desc

    # -------------------------------
    # На удивление, тут нет картинки,
    # ее надо дергать с листинга
    # -------------------------------
    logger.info(json_pretty_print(object_fields(analog)))
    analog.save()

    if not seance:
        logger.error('---SEANCE NOT RECOGNIZED---')
    if not place:
        logger.error('---PLACE NOT RECOGNIZED---')

def wipe():
    """Удаление информации из базы
       Все похерить кыбеням"""
    RSeances.objects.all().delete()
    for place in Places.objects.all():
        place.delete()
    for event in REvents.objects.all():
        event.delete()
    RGenres.objects.all().delete()
    Rubrics.objects.all().delete()


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--start',
            action = 'store',
            dest = 'start',
            type = str,
            default = False,
            help = 'Set start date')
        parser.add_argument('--end',
            action = 'store',
            dest = 'end',
            type = str,
            default = False,
            help = 'Set end date')

    def handle(self, *args, **options):
        wipe()
        #exit()

        # ----------------------------------
        # Парсим всегда с завтрашнего числа,
        # чтобы увидеть все сеансы
        # ----------------------------------
        today = datetime.date.today()
        start_date = date_plus_days(today, days=1)
        end_date = date_plus_days(today, days=10)

        # ---------------------------
        # Задать дату начала парсинга
        # ---------------------------
        if options.get('start'):
            date = str_to_date(options['start'])
            if date:
                start_date = date

        # ------------------------------
        # Задать дату окончания парсинга
        # ------------------------------
        if options.get('end'):
            date = str_to_date(options['end'])
            if date:
                end_date = date

        if start_date > end_date:
            end_date = date_plus_days(start_date, days=1)

        rubrics, genres = get_rubrics()

        cur_date = start_date

        while cur_date <= end_date:
            RSeances.objects.filter(date=cur_date).delete()
            for genre in genres:
                logger.info('{} {}'.format(genre.tag, genre.name))
                if 'cinema' in genre.tag:
                    get_cinema_seances(cur_date)
                else:
                    get_seances(genre.tag, cur_date)
            cur_date = date_plus_days(cur_date, days=1)

