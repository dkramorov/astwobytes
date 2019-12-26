# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from apps.main_functions.models import Standard
from apps.main_functions.string_parser import translit

def get_ftype(ftype):
    state_choices = (
        (1, 'flatmenu'),
        (2, 'flatmain'), # Контент для всех страничек
        (3, 'flatpages'),
        (4, 'flatprices'), # Ориентирован на товар/услугу
        (5, 'flatnews'),
        (6, 'flatmobile'), # Ориентирован на мобильный контент
        (7, 'flatcat'), # Ориентирован на контейнеры, привязанные к рубрикам
        (99, 'flattemplates'), # шаблоны специфические для сайта
        (100, 'flattemplates'), # шаблоны конструктора
    )
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
    elif ftype == 'flatcat': # Ориентирован на контейнеры, привязанные к рубрикам
        mh_vars.update({
            'singular_obj': 'Контент рубрики',
            'plural_obj': 'Контент рубрик',
            'rp_singular_obj': 'контента рубрики',
            'rp_plural_obj': 'контента рубрик',
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
    mh_vars.update({
        'template_prefix': '%s_' % (ftype, ),
        'submenu': ftype,
    })

def update_blocks_vars(ftype, mh_vars):
    if ftype == 'flatmenu':
        mh_vars.update({
            'singular_obj': 'Пункт меню',
            'plural_obj': 'Пункты меню',
            'rp_singular_obj': 'Пункта меню',
            'rp_plural_obj': 'Пунктов меню',
        })
    mh_vars.update({
        'template_prefix': 'blocks/%s_' % (ftype, ),
        'submenu': ftype,
    })

class Containers(Standard):
    """Контейнер служит как меню, в него можно
       вкладывать блоки, которые могут быть как
       ссылками меню так и блоками на страничке"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    template_position = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Стат.контент - Контейнеры'
        verbose_name_plural = 'Стат.контент - Контейнеры'

    def delete(self, *args, **kwargs):
        children = self.blocks_set.all()
        for child in children:
            child.delete()
        super(Containers, self).delete(*args, **kwargs)

class Blocks(Standard):
    """Блоки - динамический контент
       картинка, текст, html, ссылка (пункт меню)"""
    state_choices = (
        (1, "Текст"),
        (2, "Изображение"),
        (3, "HTML"),
        (4, "Ссылка/Меню"),
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    container = models.ForeignKey(Containers, blank=True, null=True, on_delete=models.CASCADE)
    # для ссылок target=_blank
    blank = models.BooleanField(blank=True, null=True, default=True, db_index=True)
    icon = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # title/мета-теги для меню или title/alt для картинки
    title = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    keywords = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Стат.контент - Блоки'
        verbose_name_plural = 'Стат.контент - Блоки'

    def save(self, *args, **kwargs):
        if self.state == 4 and not self.link and self.name:
            link = None
            # --------------------------------------------------
            # Если есть родительская ссылка, нужно ее подставить
            # --------------------------------------------------
            parents = None
            if self.parents:
                if "_" in self.parents:
                    parent = self.parents.split("_")[-1]
                    try:
                        parent = int(parent)
                    except ValueError:
                        parent = None
                    if parent:
                        parent_menu = Blocks.objects.get(pk=parent)
                        if parent_menu:
                            link = parent_menu.link
            if link:
              link += translit(self.name) + "/"
            else:
              link = "/" + translit(self.name) + "/"
            self.link = link
        super(Blocks, self).save(*args, **kwargs)

    # ----------------------------------------
    # По блоку хотим достать товары/услуги
    # Они крепятся к блоку через LinkContainer
    # К меню у нас привязаны контейнеры
    # Через функцию удобно доставать в шаблоне
    # ----------------------------------------
    def get_products(self, request=None):
        all_containers = [] # Для перевода
        # ---------------------------------------------
        # Возможно, есть контейнеры с товарами/услугами
        # ---------------------------------------------
        have_prices = []
        ids_containers = {}

        if "price" in settings.INSTALLED_APPS:

          from price.models import PriceContainer, Disconts, CostsTypes, Costs
          from price.utils import search_disconts_for_prices, get_costs_types

          # --------------------------------------------
          # Вычисляем есть ли привязка меню к контейнеру
          # --------------------------------------------
          containers = LinkContainer.objects.select_related("container").filter(block=self)
          if containers:
            for container in containers:
              all_containers.append(container.container) # Для перевода
              ids_containers[container.container.id] = {"container":container.container, "tags":{}, "prices":[], "position":container.position}
        # ----------------------------
        # Вытаскиваем только контейнер
        # и привязку к товарам,
        # вложенные блоки не тащим
        # ----------------------------
        if ids_containers:
          # -------------------------------------
          # Обрабатываем нестандартные контейнеры
          # -------------------------------------
          prices = PriceContainer.objects.select_related("price").filter(container__in=ids_containers.keys()).order_by("position")
          ids_prices = {x.price.id:x.price for x in prices}
          # -------------------------------
          # Находим скидки для всех товаров
          # -------------------------------
          shopper = None
          if request:
            shopper = request.session.get("shopper", None)
          search_disconts_for_prices(ids_prices, shopper)
          # ---------------
          # Разные типы цен
          # ---------------
          get_costs_types(ids_prices)
          # ----------------------
          # Рейтинги товаров/услуг
          # ----------------------
          if "reviews" in settings.INSTALLED_APPS:
            from reviews.models import get_objects_ratings
            get_objects_ratings(ids_prices, "price.Products")
          # -------
          # Перевод
          # -------
          if request:
            if hasattr(settings, "DOMAINS") and "languages" in settings.INSTALLED_APPS:
              from django.contrib.contenttypes.models import ContentType
              from languages.models import Translate
              from languages.views import get_translations, translate_rows
              # -----------------------
              # Переводим товары/услуги
              # -----------------------
              ct_prices = ContentType.objects.get_for_model(Products)
              get_translations(ids_prices.values(), ct_prices)
              translate_rows(ids_prices.values(), request)
              # --------------------
              # Переводим контейнеры
              # --------------------
              ct_containers = ContentType.objects.get_for_model(Containers)
              get_translations(all_containers, ct_containers)
              translate_rows(all_containers, request)

          # ----------------------------------------
          # Для сохранения сортировки идем по prices
          # ----------------------------------------
          for item in prices:
            price = ids_prices[item.price.id]
            ids_containers[item.container_id]['prices'].append(price)
            have_prices.append(item.container_id)
          # ------------------------------------
          # Ищем скидки/акции по товарам/услугам
          # ------------------------------------
          if have_prices:
            disconts = Disconts.objects.filter(container__in=have_prices)
            for discont in disconts:
              # ----------------------------------
              # Добавлять надо к самому контейнеру
              # ----------------------------------
              for key, value in ids_containers.items():
                container_id = value['container'].id
                if discont.container_id == container_id:
                  value['container'].discont = discont
                  break
        return sorted(ids_containers.values(), key=lambda x: x['position'])

class LinkContainer(Standard):
    """Линковка пункта меню к контейнеру
       Ссылка на стр. может быть ссылкой на контейнер"""
    block = models.ForeignKey(Blocks, on_delete=models.CASCADE)
    container = models.ForeignKey(Containers, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Стат.контент - Линковка меню к контейнерам'
        verbose_name_plural = 'Стат.контент - Линковка меню к контейнерам'

#class SiteMap(models.Model):
#    """Карта сайта
#     Выбираем нужные меню по поиску и по ним
#     делаем sitemapindex в которых уже urlset
#     TODO для ссылок добавить lastmod,
#     changefreq и priority"""
#    container = models.ForeignKey(Containers, blank=True, null=True, on_delete=models.CASCADE)
#    block = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.CASCADE)
#    #link = models.CharField(max_length=255, blank=True, null=True)
