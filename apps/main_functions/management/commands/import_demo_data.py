# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User, Group, Permission
from django.conf import settings

from apps.login.models import create_default_user
from apps.flatcontent.models import Containers, Blocks
from apps.files.models import Files
from apps.main_functions.models import Config
from apps.main_functions.functions import object_fields
from apps.main_functions.files import open_file, make_folder

logger = logging.getLogger(__name__)

if settings.IS_DOMAINS:
    from apps.languages.models import get_domains

robots_txt_content = """User-agent: *
Disallow: /admin/
Sitemap: https://{}/sitemap.xml
"""

def fill_flatmain(**kwargs):
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
            title='Company name', name='Название компании',
            state=3,
        )
    favicon = Blocks.objects.filter(container=container, tag='favicon').first()
    if not favicon:
        favicon = Blocks.objects.create(
            container=container, tag='favicon',
            name='Favicon',
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
    for item in ({
        'tag': 'yandex_metrika',
        'name': 'Яндекс.Метрика счетчик',
    }, {
        'tag': 'google_analytics',
        'name': 'Google.Analytics счетчик',
    }):
        counter = Blocks.objects.filter(container=container, tag=item['tag']).first()
        if not counter:
            counter = Blocks.objects.create(
                container=container, tag=item['tag'],
                name=item['name'], state=3,
                html='<script type="text/javascript"></script>',
            )

def fill_flatmenu(**kwargs):
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

def fill_settings(**kwargs):
    """Настройки"""
    feedback = Config.objects.filter(attr='flatcontent_feedback').first()
    if not feedback:
        feedback = Config.objects.create(name='Почта обратной связи',
                                         attr='flatcontent_feedback',
                                         value='dkramorov@mail.ru')

def fill_users(**kwargs):
    """Пользователи
       1) сео-пользователь
    """
    seo_perms = ('seo_fields',
                 'add_files',
                 'view_files',
                 'view_blocks',
                 'view_containers', )
    seo_group_name = 'SEO'
    username = 'SeoManager'
    group = Group.objects.filter(name=seo_group_name).first()
    if not group:
        group = Group.objects.create(name=seo_group_name)
    for perm in Permission.objects.all():
        #print(object_fields(perm))
        if perm.codename in seo_perms:
            group.permissions.add(perm)
    user = User.objects.filter(username=username).first()
    if not user:
        kwargs = {
            'username': username,
            'email': 'seo_manager@masterme.ru',
            'passwd': 'SeoManager',
            'last_name': 'SeoManager',
            'is_superuser': False,
            'is_active': True,
            'is_staff': True,
        }
        user = create_default_user(**kwargs)
    groups = [group for group in user.groups.all() if group.name == seo_group_name]
    if len(groups) < 1:
        user.groups.add(group)

def fill_files(**kwargs):
    """Файлы
       :param kwargs['force'] принудительно обновляет файл
    """
    def create_robots_txt(domain: dict = None):
        """Вспомогательная функция для создания robotx.txt файла
           :param domain: словарь с параметрами домена
        """
        if not domain:
            domain = {}
        robots_txt = Files.objects.create(link=robots_txt_link,
            name='robots.txt',
            desc='Файл для запретов индексации поисковым системам',
            domain=domain.get('pk'))
        folder = robots_txt.get_folder()
        make_folder(folder)
        dest = '%s%s' % (folder.rstrip('/'), robots_txt_link)
        with open_file(dest, mode='w+', encoding='utf-8') as f:
            domain_site = domain.get('domain')
            if not domain_site:
                domain_site = settings.MAIN_DOMAIN or 'masterme.ru'
            f.write(robots_txt_content.format(domain_site))
        robots_txt.path = robots_txt_link.lstrip('/')
        robots_txt.save()

    robots_txt_link = '/robots.txt'
    robots_txt = Files.objects.filter(link=robots_txt_link)
    if not robots_txt or kwargs.get('force'):
        for item in Files.objects.filter(link=robots_txt_link):
            item.delete()

        create_robots_txt()
        if settings.IS_DOMAINS:
            domains = get_domains()
            for domain in domains:
                create_robots_txt(domain)

class Command(BaseCommand):
    """Заливаем демонстрационными данными сайт"""
    def add_arguments(self, parser):
        parser.add_argument('--flatmain',
            action = 'store_true',
            dest = 'flatmain',
            default = False,
            help = 'Fill flatmain')
        parser.add_argument('--flatmenu',
            action = 'store_true',
            dest = 'flatmenu',
            default = False,
            help = 'Fill flatmenu')
        parser.add_argument('--flatsettings',
            action = 'store_true',
            dest = 'flatsettings',
            default = False,
            help = 'Fill settings')
        parser.add_argument('--users',
            action = 'store_true',
            dest = 'users',
            default = False,
            help = 'Fill users')
        parser.add_argument('--files',
            action = 'store_true',
            dest = 'files',
            default = False,
            help = 'Fill files')
        parser.add_argument('--force',
            action = 'store_true',
            dest = 'force',
            default = False,
            help = 'Set force update (for files)')

    def handle(self, *args, **options):
        cmd = []
        kwargs = {}
        if options.get('flatmain'):
            cmd.append(fill_flatmain)
        if options.get('flatmenu'):
            cmd.append(fill_flatmenu)
        if options.get('flatsettings'):
            cmd.append(fill_settings)
        if options.get('users'):
            cmd.append(fill_users)
        if options.get('files'):
            cmd.append(fill_files)

        if options.get('force'):
            kwargs['force'] = True

        if not cmd:
            fill_flatmain(**kwargs)
            fill_flatmenu(**kwargs)
            fill_settings(**kwargs)
            fill_users(**kwargs)
            fill_files(**kwargs)
        else:
            for item in cmd:
                item(**kwargs)




