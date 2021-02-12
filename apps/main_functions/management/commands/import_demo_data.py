# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from django.conf import settings

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.models import Config

logger = logging.getLogger(__name__)

def fill_flatmain():
    """Контент для всех страничек"""
    container = Containers.objects.filter(tag='main', state=2).first()
    if not container:
        container = Containers.objects.create(tag='main', state=2, name='Контент для всех страничек', description='Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики')
    logo = Blocks.objects.filter(container=container, tag='logo').first()
    if not logo:
        logo = Blocks.objects.create(
            container=container, tag='logo',
            description='Добро пожаловать, на наш сайт',
            name='Логотип', link='/', state=3,
        )
    phone = Blocks.objects.filter(container=container, tag='phone').first()
    if not phone:
        phone = Blocks.objects.create(
            container=container, tag='phone',
            name='Телефон', html='+7(3952) 123-321',
            link='tel:73952123321', state=3,
        )
    address = Blocks.objects.filter(container=container, tag='address').first()
    if not address:
        address = Blocks.objects.create(
            container=container, tag='address',
            name='Адрес', html='г. Иркутск ул. Советская 32а офис 5',
            state=3,
        )
    email = Blocks.objects.filter(container=container, tag='email').first()
    if not email:
        email = Blocks.objects.create(
            container=container, tag='email',
            name='Email', html='test@test.ru',
            state=3,
        )
    worktime = Blocks.objects.filter(container=container, tag='worktime').first()
    if not worktime:
        worktime = Blocks.objects.create(
            container=container, tag='worktime',
            name='Режим работы', html='пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',
            state=3,
        )
    copyright = Blocks.objects.filter(container=container, tag='copyright').first()
    if not copyright:
        copyright = Blocks.objects.create(
            container=container, tag='copyright',
            name='Copyright', html='<p>&copy; 2020 Все права защищены</p>',
            state=3,
        )
    company_name = Blocks.objects.filter(container=container, tag='company_name').first()
    if not company_name:
        company_name = Blocks.objects.create(
            container=container, tag='company_name',
            title='RGBA и COMPыта', name='Название компании',
            state=3,
        )
    social = Blocks.objects.filter(container=container, tag='social').first()
    if not social:
        social = Blocks.objects.create(
            container=container, tag='social',
            name='Сообщества', state=3,
        )
    for item in ('instagram', 'vk', 'facebook', 'twitter'):
        icon = Blocks.objects.filter(container=container, tag=item, parents='_%s' % social.id).first()
        if not icon:
            icon = Blocks.objects.create(
                container=container, tag=item,
                name=item, parents='_%s' % social.id,
                blank=True, icon=item,
                state=3,
            )

def fill_flatmenu():
    """Меню"""
    mainmenu = Containers.objects.filter(tag='mainmenu', state=1).first()
    if not mainmenu:
        mainmenu = Containers.objects.create(tag='mainmenu', state=1, name='Главное меню', description='Создано автоматически, выводит главное меню')
    bottommenu = Containers.objects.filter(tag='bottommenu', state=1).first()
    if not bottommenu:
        bottommenu = Containers.objects.create(tag='bottommenu', state=1, name='Нижнее меню', description='Создано автоматически, выводит нижнее меню')
    mainpage = Blocks.objects.filter(container=mainmenu, tag='_mainmenu_mainpage').first()
    if not mainpage:
        mainpage = Blocks.objects.create(
            container=mainmenu, state=4,
            name='Главная', link='/',
            tag='_%s_mainpage' % mainmenu.tag,
        )
    for menu in (mainmenu, bottommenu):
        catpage = Blocks.objects.filter(
            container=menu, tag='_%s_catpage' % menu.tag
        ).first()
        if not catpage:
            catpage = Blocks.objects.create(
                container=menu, state=4,
                name='Каталог', link='/cat/',
                tag='_%s_catpage' % menu.tag,
            )
        # Подпункты в меню
        for subpage in (('Популярные товары', 'popular'),
                        ('Новые товары', 'new'),
                        ('Товары со скидкой', 'discount'),
                        ('Распродажа', 'sale')):
            catitem = Blocks.objects.filter(
                container=menu, tag='_%s_catpage_%s' % (menu.tag, subpage[1]),
            ).first()
            if not catitem:
                catitem = Blocks.objects.create(
                    container=menu, state=4,
                    name=subpage[0], parents='_%s' % catpage.id,
                    tag='_%s_catpage_%s' % (menu.tag, subpage[1]),
                )
        aboutpage = Blocks.objects.filter(
            container=menu, tag='_%s_aboutpage' % menu.tag
        ).first()
        if not aboutpage:
            aboutpage = Blocks.objects.create(
                container=menu, state=4,
                name='О нас', link='/about/',
                tag='_%s_aboutpage' % menu.tag,
            )
        servicespage = Blocks.objects.filter(
            container=menu, tag='_%s_servicespage' % menu.tag
        ).first()
        if not servicespage:
            servicespage = Blocks.objects.create(
                container=menu, state=4,
                name='Услуги', link='/services/',
                tag='_%s_servicespage' % menu.tag,
            )
        feedbackpage = Blocks.objects.filter(
            container=menu, tag='_%s_feedbackpage' % menu.tag
        ).first()
        if not feedbackpage:
            feedbackpage = Blocks.objects.create(
                container=menu, state=4,
                name='Контакты', link='/feedback/',
                tag='_%s_feedbackpage' % menu.tag,
            )

def fill_settings():
    """Настройки"""
    feedback = Config.objects.filter(attr='flatcontent_feedback').first()
    if not feedback:
        feedback = Config.objects.create(name='Почта обратной связи',
                                         attr='flatcontent_feedback',
                                         value='dkramorov@mail.ru')

class Command(BaseCommand):
    """Заливаем демонстрационными данными сайт"""
    def add_arguments(self, parser):
        parser.add_argument('--flatmain',
            action = 'store_true',
            dest = 'flatmain',
            default = False,
            help = 'Fill only flatmain')
        parser.add_argument('--flatmenu',
            action = 'store_true',
            dest = 'flatmenu',
            default = False,
            help = 'Fill only flatmenu')
        parser.add_argument('--flatsettings',
            action = 'store_true',
            dest = 'flatsettings',
            default = False,
            help = 'Fill only settings')

    def handle(self, *args, **options):
        if options.get('flatmain'):
            fill_flatmain()
            return
        if options.get('flatmenu'):
            fill_flatmenu()
            return
        if options.get('flatsettings'):
            fill_settings()
            return
        fill_flatmain()
        fill_flatmenu()
        fill_settings()



