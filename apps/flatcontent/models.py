# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from apps.main_functions.models import Standard
from apps.main_functions.string_parser import translit, fix_multiple_dashes

# Если слишком много рубрик, то грузить надо lazy
FAT_HIER = 250

def get_ftype(ftype, by_id: bool = False):
    """Получение типа контейнера
       :param ftype: число или тег контейнера
       :param by_id: если ищем контейнер по числу"""
    state_choices = (
        (1, 'flatmenu'),
        (2, 'flatmain'), # Контент для всех страничек
        (3, 'flatpages'),
        (4, 'flatprices'), # Ориентирован на товар/услугу
        (5, 'flatnews'),
        (6, 'flatmobile'), # Ориентирован на мобильный контент
        (7, 'flatcat'), # Каталог
        (99, 'flattemplates'), # шаблоны специфические для сайта
        (100, 'flattemplates'), # шаблоны конструктора
    )
    if by_id:
        for item in state_choices:
            if item[0] == ftype:
                return item[1]

    for item in state_choices:
        if item[1] == ftype:
            return item[0]
    return None

def update_containers_vars(ftype, mh_vars):
    if ftype == 'flatmenu':
        mh_vars.update({
            'singular_obj': 'Меню',
            'plural_obj': 'Меню',
            'rp_singular_obj': 'меню',
            'rp_plural_obj': 'меню',
        })
    elif ftype == 'flatmain': # Контент для всех страничек
        mh_vars.update({
            'singular_obj': 'Контент для всех страничек',
            'plural_obj': 'Контент для всех страничек',
            'rp_singular_obj': 'контента для всех страничек',
            'rp_plural_obj': 'контента для всех страничек',
        })
    elif ftype == 'flatpages':
        mh_vars.update({
            'singular_obj': 'Стат. страничка',
            'plural_obj': 'Стат. странички',
            'rp_singular_obj': 'стат. странички',
            'rp_plural_obj': 'стат. страничек',
        })
    elif ftype == 'flatprices': # Ориентирован на товар/услугу
        mh_vars.update({
            'singular_obj': 'Контейнер товаров',
            'plural_obj': 'Контейнеры товаров',
            'rp_singular_obj': 'контейнера товаров',
            'rp_plural_obj': 'контейнеров товаров',
        })
    elif ftype == 'flatnews':
        mh_vars.update({
            'singular_obj': 'Новость',
            'plural_obj': 'Новости',
            'rp_singular_obj': 'новости',
            'rp_plural_obj': 'новостей',
        })
    elif ftype == 'flatmobile': # Ориентирован на мобильный контент
        mh_vars.update({
            'singular_obj': 'Моб. контент',
            'plural_obj': 'Моб. контент',
            'rp_singular_obj': 'моб. контента',
            'rp_plural_obj': 'моб. контента',
        })
    elif ftype == 'flatcat': # Каталог сайта
        mh_vars.update({
            'singular_obj': 'Каталог',
            'plural_obj': 'Каталоги',
            'rp_singular_obj': 'каталога',
            'rp_plural_obj': 'каталогов',
        })
    elif ftype == 'flattemplates': # шаблоны специфические для сайта
        mh_vars.update({
            'singular_obj': 'Шаблон',
            'plural_obj': 'Шаблоны',
            'rp_singular_obj': 'шаблона',
            'rp_plural_obj': 'шаблонов',
        })
    elif ftype == 'flattemplates': # шаблоны конструктора
        mh_vars.update({
            'singular_obj': 'Шаблон конструктора',
            'plural_obj': 'Шаблоны конструктора',
            'rp_singular_obj': 'шаблона конструктора',
            'rp_plural_obj': 'шаблонов конструктора',
        })
    template_prefix = '%s_' % (ftype, )
    mh_vars.update({
        'template_prefix': template_prefix,
        'submenu': ftype,
    })

def update_blocks_vars(ftype, mh_vars):
    if ftype == 'flatmenu':
        mh_vars.update({
            'singular_obj': 'Пункт меню',
            'plural_obj': 'Пункты меню',
            'rp_singular_obj': 'пункта меню',
            'rp_plural_obj': 'пунктов меню',
        })
    elif ftype in ('flatmain', 'flatpages',
                   'flatnews', 'flatmobile',
                   'flattemplates'):
        mh_vars.update({
            'singular_obj': 'Блок',
            'plural_obj': 'Блоки',
            'rp_singular_obj': 'блока',
            'rp_plural_obj': 'блоков',
        })
    elif ftype == 'flatprices': # Ориентирован на товар/услугу
        mh_vars.update({
            'singular_obj': 'Товар',
            'plural_obj': 'Товары',
            'rp_singular_obj': 'товара',
            'rp_plural_obj': 'товаров',
        })
    elif ftype == 'flatcat': # Каталог
        mh_vars.update({
            'singular_obj': 'Рубрика',
            'plural_obj': 'Рубрики',
            'rp_singular_obj': 'рубрики',
            'rp_plural_obj': 'рубрик',
        })
    elif ftype == '': # шаблоны специфические для сайта
        mh_vars.update({
            'singular_obj': 'Шаблон',
            'plural_obj': 'Шаблоны',
            'rp_singular_obj': 'шаблона',
            'rp_plural_obj': 'шаблонов',
        })
    mh_vars.update({
        'template_prefix': 'blocks/%s_' % (ftype, ),
        'submenu': ftype,
    })

def prepare_jstree(data,
                   menus,
                   lazy: bool = False,
                   fill_href: bool = False):
    """Вспомогательная функция для построения
       меню из queryset в формат jstree
       :param data: результат
       :param menus: иерархия менюшек
       :param lazy: если хотим получать только текущий уровень
    """
    custom_font = None
    if menus:
        container = menus[0].container
        if container.custom_font:
            custom_font = '%s %s-' % (container.custom_font[:2], container.custom_font[:2])

    for menu in menus:
        href = '#%s' % menu.id
        if fill_href:
            href = menu.link
        branch = {
            'id': menu.id,
            'text': menu.name,
            'state': {'opened': False, 'selected': False},
            'children': [] if not lazy else True,
            'a_attr': {
                'href': href,
            },
        }
        if not menu.is_active:
            branch['li_attr'] = {
                'class': 'non-active',
            }

        #if menu.icon:
        #   branch['icon'] = 'fa fa-%s' % menu.icon
        if custom_font and menu.icon:
            branch['icon'] = '%s%s' % (custom_font, menu.icon)

        data.append(branch)

        if hasattr(menu, 'sub'):
            if menu.sub:
                prepare_jstree(data[-1]['children'], menu.sub, fill_href)

class Containers(Standard):
    """Контейнер служит как меню, в него можно
       вкладывать блоки, которые могут быть как
       ссылками меню так и блоками на страничке
    """
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    template_position = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    class_name = models.CharField(max_length=128, blank=True, null=True, db_index=True, verbose_name='Класс css')
    custom_font = models.CharField(max_length=128,
        blank=True, null=True, db_index=True,
        verbose_name='Название своего шрифта (например, для иконок)')

    class Meta:
        verbose_name = 'Стат.контент - Контейнеры'
        verbose_name_plural = 'Стат.контент - Контейнеры'

    def delete(self, *args, **kwargs):
        children = self.blocks_set.all()
        for child in children:
            child.delete()
        super(Containers, self).delete(*args, **kwargs)

    def cat_link(self):
        """Получение ссылки для корня каталога"""
        if self.tag and not self.tag == settings.DEFAULT_CATALOGUE_TAG:
            return '/cat/%s/' % self.tag
        return '/cat/'

    def __str__(self):
        return 'pk=%s, %s, tag=%s, state=%s' % (self.pk, self.name, self.tag, self.state)

class Blocks(Standard):
    """Блоки - динамический контент
       картинка, текст, html, ссылка (пункт меню)
    """
    state_choices = (
        (1, "Текст"),
        (2, "Изображение"),
        (3, "HTML"),
        (4, "Каталог/Меню"),
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    html = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    container = models.ForeignKey(Containers, blank=True, null=True, on_delete=models.CASCADE)
    # для ссылок target=_blank
    blank = models.BooleanField(db_index=True, default=False)
    icon = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # title/мета-теги для меню или title/alt для картинки
    title = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    keywords = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    class_name = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Класс css')

    class Meta:
        verbose_name = 'Стат.контент - Блоки'
        verbose_name_plural = 'Стат.контент - Блоки'
        permissions = (
            ('seo_fields', 'Заполнение сео-полей меню'),
        )

    def create_menu_link(self, force: bool = False):
        """Создание ссылки для меню
           1) Только тип ссылка (state=4)
              Только без уже имеющейся ссылки
           2) Только с именем
              Только с типом контейнера меню (state=1)
           :param force: создать ссылку независимо от типа контейнера
        """
        if not self.state == 4 or not self.name:
            return

        if not force:
            if not self.container.state == 1 or self.link:
                return
        link = None
        # --------------------------------------------------
        # Если есть родительская ссылка, нужно ее подставить
        # --------------------------------------------------
        parents = None
        if self.parents:
            if '_' in self.parents:
                parent = self.parents.split('_')[-1]
                try:
                    parent = int(parent)
                except ValueError:
                    parent = None
                if parent:
                    parent_menu = Blocks.objects.filter(pk=parent).values_list('link', flat=True).first()
                    if parent_menu:
                        link = parent_menu
        if link:
            link += translit(self.name) + '/'
        else:
            link = '/' + translit(self.name) + '/'
        link = fix_multiple_dashes(link)

        # TODO: проверить повторы
        if len(link) > 254:
            link = '/' + translit(self.name) + '/'

        self.link = link

    def create_cat_link(self, force: bool = False):
        """Создание ссылки для рубрики каталога
           1) Только тип ссылка (state=4)
              Только без уже имеющейся ссылки
           2) Только с именем
              Только с типом контейнера рубрика (state=7)
        """
        if not self.state == 4 or not self.name:
            return

        if not force:
            if not self.container.state == 7 or self.link:
                return

        self.create_menu_link(force=True)
        # Для подуровней не надо /cat
        # /cat уже будет у верхнего уровня
        prefix = ''
        if not self.parents:
            prefix = '/cat'
            if self.tag and not self.container.tag == settings.DEFAULT_CATALOGUE_TAG:
                prefix = '/cat/%s' % self.container.tag
        self.link = '%s%s' % (prefix, self.link)

    def save(self, *args, **kwargs):
        """Сохранение объекта"""
        self.create_menu_link()
        self.create_cat_link()
        if not self.parents:
            self.parents = ''
        super(Blocks, self).save(*args, **kwargs)

    def __str__(self):
        return 'pk=%s, %s, state=%s' % (self.pk, self.name, self.state)

class LinkContainer(Standard):
    """Линковка пункта меню к контейнеру
       Ссылка на стр. может быть ссылкой на контейнер
    """
    block = models.ForeignKey(Blocks, on_delete=models.CASCADE)
    container = models.ForeignKey(Containers, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Стат.контент - Линковка меню к контейнерам'
        verbose_name_plural = 'Стат.контент - Линковка меню к контейнерам'

def get_link_containers(block: Blocks):
    """Получение привязанных контейнеров к блоку
       :param block: блок, к котому ищем привязки
    """
    if not block:
        return []
    result = block.linkcontainer_set.select_related('container').order_by('position')
    block.linkcontainers = [link.container for link in result]
    return block.linkcontainers

def link_containers2block(block: Blocks, ids_containers: list):
    """Привязать к блоку контейнеры
       через LinkContainer
       :param block: блок, к которому делаем привязку
       :param ids_containers: список ид контейнеров для привязки
    """
    ids_containers = [int(container_id) for container_id in ids_containers]
    clist = {container_id: None for container_id in ids_containers}
    containers = Containers.objects.filter(pk__in=ids_containers)
    for container in containers:
        clist[container.id] = container
    # ----------------
    # Старая структура
    # ----------------
    analogs = LinkContainer.objects.filter(block=block).values_list('container', flat=True)
    analogs = list(analogs)

    if not analogs and not ids_containers:
        return

    linkcontainer = [] # Новая структура
    for i, container_id in enumerate(ids_containers):
        if not container_id in clist or not clist[container_id]:
            continue
        container = clist[container_id]
        if container.id in analogs:
            LinkContainer.objects.filter(block=block, container=container).update(position=i)
        else:
            LinkContainer.objects.create(block=block, container=container, position=i)
        linkcontainer.append(container.id)
    # ----------------------
    # Удаление тех привязок,
    # которые не встретились
    # ----------------------
    fordel = []
    for analog in analogs:
        if not analog in linkcontainer:
            fordel.append(analog)
    if fordel:
        LinkContainer.objects.filter(block=block, container__in=fordel).delete()



