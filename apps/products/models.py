# -*- coding: utf-8 -*-
import time

from django.db import models
from django.core.cache import cache
from django.conf import settings

from apps.flatcontent.models import (Containers,
                                     Blocks,
                                     link_containers2block,
                                     get_link_containers, )
from apps.main_functions.models import Standard
from apps.main_functions.string_parser import translit
from apps.main_functions.date_time import calc_elapsed_time

# Если нужно оладить кэш
CACHE_DEBUG = False

CURRENCY_CHOICES = (
    (1, "₽"),
    (2, "$"),
)

class Cached(object):
    """Кэшированные объекты, чтобы даже в кэш не ходить за ними
       пока кэш на час, TODO: доработать до указания времени кэша
       или просто поставить минимальное, например, минутку
    """
    ONE_HOUR = 60*60
    CREATED_POSTFIX = '_created'

    @classmethod
    def set_obj(cls, key, value):
        setattr(cls, '%s%s' % (key, cls.CREATED_POSTFIX), time.time())
        setattr(cls, key, value)

    @classmethod
    def get_obj(cls, key):
        if hasattr(cls, key) and getattr(cls, '%s%s' % (key, cls.CREATED_POSTFIX)) > time.time() - cls.ONE_HOUR:
            return getattr(cls, key)

class Products(Standard):
    """Товары/услуги"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    altname = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    measure = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    currency = models.IntegerField(choices=CURRENCY_CHOICES, blank=True, null=True, db_index=True)
    old_price = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, db_index=True) # 99 000 000 000,00
    price = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, db_index=True) # 99 000 000 000,00
    dj_info = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    mini_info = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    count = models.IntegerField(blank=True, null=True, db_index=True)
    stock_info = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Текстовая информация об остатках')
    # min/max price храним преимущественно для сортировки,
    # согда у нас есть несколько типов цен на товар
    min_price = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, db_index=True) # 99 000 000 000,00
    max_price = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, db_index=True) # 99 000 000 000,00
    min_count = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Минимальное кол-во для заказа')
    multiplicity = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Кратность товара, по сколько будет добавляться +/-')

    class Meta:
        verbose_name = 'Товары - товар/услуга'
        verbose_name_plural = 'Товары - товары/услуги'

    def analyze_prices(self):
        """Дополнительная обработка цен"""
        self.min_price = self.price if self.price else None
        self.max_price = self.price if self.price else None
        if self.id:
            min_price = Costs.objects.filter(product=self).aggregate(models.Min('cost'))['cost__min']
            if not self.price or (min_price and self.price > min_price):
                self.min_price = min_price
            max_price = Costs.objects.filter(product=self).aggregate(models.Max('cost'))['cost__max']
            if not self.price or (max_price and self.price < max_price):
                self.max_price = max_price

        if self.old_price and self.old_price > 99999999999:
            self.old_price = None
        if self.price and self.price > 99999999999:
            self.price = None

    def save(self, *args, **kwargs):
        self.analyze_prices()
        # Замена для того, чтобы ЧПУ ссылку распознать
        #if self.code:
        #    self.code = str(self.code).replace('-', '_')
        super(Products, self).save(*args, **kwargs)
        if self.id and not self.code:
            Products.objects.filter(pk=self.id).update(code=self.id)

    def link(self):
        """Ссылка на товар/услугу"""
        link = '/product/%s/' % self.id
        if self.code and self.name and not '-' in self.code:
            link = '/product/%s-%s/' % (translit(self.name), self.code)
        elif self.name:
            link = '/product/%s-%s/' % (translit(self.name), self.id)
        return link

    def fill_seo(self, **kwargs):
        """Заполнение сео-полей/статей для товара,
           заполнение привязок к статьям (привязваем контейнеры)
           просто создаем ссылку с сео-полями по ссылке товара,
        """
        if not self.id:
            return
        seo_fields = ('seo_title', 'seo_description', 'seo_keywords')
        linkcontainer = kwargs.get('linkcontainer', [])

        seo_block = None
        seo_tag = 'seo_for_products'
        product_tag = 'product_%s' % self.id
        link = self.link()
        seo_container = Containers.objects.filter(state=4, tag=seo_tag).first()
        if not seo_container:
            seo_container = Containers.objects.create(
                state=4,
                tag=seo_tag,
                name='Сео-тексты для товаров/услуг'
            )
        seo_blocks = seo_container.blocks_set.filter(models.Q(tag=product_tag)|models.Q(link=link))
        # Если по id не найден блок,
        # тогда пробуем найти по ссылке
        if not seo_blocks:
            seo_block = Blocks(
                state=4,
                container=seo_container,
                tag=product_tag,
                link=link,
            )
        else:
            for block in seo_blocks:
                if block.tag == product_tag:
                    seo_block = block
                    break
            if not seo_block:
                seo_block = seo_blocks[0]
        seo_block.link = link
        seo_block.name = self.name
        for key in seo_fields:
            field = key.replace('seo_', '')
            setattr(seo_block, field, kwargs.get(key))
        seo_block.save()
        link_containers2block(seo_block, linkcontainer)

    def get_seo(self):
        """Получить сео для товара"""
        if not self.id:
            return
        seo_tag = 'seo_for_products'
        product_tag = 'product_%s' % self.id
        seo_block = None
        link = self.link()
        seo_container = Containers.objects.filter(state=4, tag=seo_tag).first()
        if not seo_container:
            return
        seo_block = None
        seo_blocks = seo_container.blocks_set.filter(models.Q(tag=product_tag)|models.Q(link=link))
        # Если по id не найден блок,
        # тогда пробуем найти по ссылке
        for block in seo_blocks:
            if block.tag == product_tag:
                seo_block = block
                break
        if not seo_block and seo_blocks:
            seo_block = seo_blocks[0]

        get_link_containers(seo_block)
        return seo_block

    def get_all_rubrics(self,
                        cache_time: int = 60*60,
                        force_new: bool = False):
        """Получение всех рубрик всех товаров
           и кэширования их для индексации
        """
        cache_var = 'get_all_rubrics_%s' % settings.PROJECT_NAME
        if not force_new:
            inCache = cache.get(cache_var)
            if inCache:
                return inCache
        result = {}
        by = 5000
        query = ProductsCats.objects.all()
        count = query.aggregate(models.Count('id'))['id__count']
        pages = int(count / by) + 1
        for i in range(pages):
            rows = query[i*by: i*by+by].values('product', 'cat', 'cat__parents')
            if i % 50 == 0:
                print('get_all_rubrics: fetching progress %s/%s' % (i, pages))
            for row in rows:
                product_id = row['product']
                if product_id not in result:
                    result[product_id] = []

                # находим все родительские рубрики по категориям
                cat_id = row['cat']
                result[product_id].append(cat_id)
                parents = row['cat__parents'] or ''
                for parent in parents.split('_'):
                    if not parent:
                        continue
                    result[product_id].append(parent)

        cache.set(cache_var, result, cache_time)
        if CACHE_DEBUG:
            test_cache_size = cache.get(cache_var)
            if not test_cache_size:
                print('Inrease cache size -I 32M')
        return result

    #@calc_elapsed_time
    def get_rubrics(self,
                    cache_time: int = 60*60,
                    force_new: bool = False):
        """Находим рубрики товара
           Пишем рубрики в которых находится товар (с родительскими)
        """
        key = 'all_rubrics'
        cached = Cached.get_obj(key)
        if cached:
            return cached.get(self.id)
        all_rubrics = self.get_all_rubrics(cache_time=cache_time,
                                           force_new=force_new)
        Cached.set_obj(key, all_rubrics)
        return all_rubrics.get(self.id)

    def get_all_props(self,
                      prop_key: str = 'prop__prop__id',
                      cache_time: int = 60*60,
                      force_new: bool = False):
        """Получение всех свойств всех товаров
           и кэширования их для индексации
           :param prop_key: prop__prop__id для Property
                            prop__id для PropertiesValues
        """
        cache_var = 'get_all_products_%s_%s' % (prop_key, settings.PROJECT_NAME)
        if not force_new:
            inCache = cache.get(cache_var)
            if inCache:
                return inCache
        result = {}
        by = 5000
        query = ProductsProperties.objects.all()
        count = query.aggregate(models.Count('id'))['id__count']
        pages = int(count / by) + 1
        for i in range(pages):
            rows = query[i*by: i*by+by].values('product', prop_key)
            if i % 50 == 0:
                print('get_all_props: fetching %s progress %s/%s' % (prop_key, i, pages))
            for row in rows:
                product_id = row['product']
                if product_id not in result:
                    result[product_id] = []
                result[product_id].append(row[prop_key])
        cache.set(cache_var, result, cache_time)
        if CACHE_DEBUG:
            test_cache_size = cache.get(cache_var)
            if not test_cache_size:
                print('Inrease cache size -I 32M')
        return result

    #@calc_elapsed_time
    def get_props(self,
                  cache_time: int = 60*60,
                  force_new: bool = False):
        """Находим свойства товара (идентификаторы)
           нужно для индекса, для фильтрации
        """
        key = 'all_props'
        cached = Cached.get_obj(key)
        if cached:
            return cached.get(self.id)
        all_props = self.get_all_props(prop_key='prop__prop__id',
                                       cache_time=cache_time,
                                       force_new=force_new)
        Cached.set_obj(key, all_props)
        return all_props.get(self.id)

    #@calc_elapsed_time
    def get_values(self,
                   cache_time: int = 60*60,
                   force_new: bool = False):
        """Находим значения свойств товара
           нужно для индекса, для фильтрации
        """
        key = 'all_values'
        cached = Cached.get_obj(key)
        if cached:
            return cached.get(self.id)
        all_values = self.get_all_props(prop_key='prop__id',
                                       cache_time=cache_time,
                                       force_new=force_new)
        Cached.set_obj(key, all_values)
        return all_values.get(self.id)

class PropertyGroup(Standard):
    """Группа свойств"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

class Property(Standard):
    """Свойство для товара"""
    ptype_choices = (
        (1, 'Выпадающий список select'),
        (2, 'Выпадающий список с множественным выбором multiselect'),
        (3, 'Выбор из вариантов radio'),
        (4, 'Множественный выбор из вариантов checkbox'),
        (5, 'Текст (используем как select), для совместимости'),
    )
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    ptype = models.IntegerField(choices=ptype_choices,
        blank=True, null=True, db_index=True)
    measure = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Единица измерения')
    search_facet = models.BooleanField(db_index=True, default=False,
        verbose_name='Отображать в фильтрах для поиска')
    group = models.ForeignKey(PropertyGroup, blank=True, null=True,
        verbose_name='Группа свойств', on_delete=models.SET_NULL)
    cat = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        super(Property, self).save(*args, **kwargs)
        if 'djapian' in settings.INSTALLED_APPS:
            from djapian.forindex import work_for_djapian
            query = ProductsProperties.objects.filter(prop__prop__id=self.id)
            count = query.aggregate(models.Count('id'))['id__count']
            if count < 5000:
                ids_products_properties = ProductsProperties.objects.filter(prop__prop__id=self.id).values_list('id', flat=True)
                work_for_djapian(ProductsProperties, list(ids_products_properties))
            else:
                print('[ERROR]: too many rows for work_for_djapian %s property, %s products properties' % (self.id, count))

class PropertiesValues(Standard):
    """Свойства для товаров/услуг
       это точные свойства, то есть, не текст от балды,
       а именно конкретное свойство с конкретным значением
    """
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    str_value = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # По большей части для сортировки и фильтров
    digit_value = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=4, db_index=True) # 990 000 000,0000
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):
        if self.str_value:
            try:
                self.digit_value = float(self.str_value.replace(',', '.'))
            except Exception:
                self.digit_value = None

        if self.digit_value and (self.digit_value > 999999999 or self.digit_value < -999999999):
            self.digit_value = None
        super(PropertiesValues, self).save(*args, **kwargs)

    def get_prop_id(self):
       """Возвращает ид свойства"""
       return self.prop_id

class ProductsProperties(models.Model):
    """Линковка значения свойства к товару"""
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    prop = models.ForeignKey(PropertiesValues, on_delete=models.CASCADE)

    def get_product_id(self):
        """Возвращает product_id"""
        return self.product_id

    def get_prop_value_id(self):
       """Возвращает ид значения свойства"""
       return self.prop_id

    def get_prop(self, cache_time: int = 600):
        """Заполняем и получаем свойство используя кэш"""
        prop_value = self.get_prop_value()
        property_id = prop_value.get('prop_id')
        if not property_id:
            return {}
        cache_var = 'get_prop_%s_%s' % (property_id, settings.PROJECT_NAME)
        inCache = cache.get(cache_var)
        if inCache:
            return inCache
        prop = Property.objects.filter(pk=property_id).first()
        if prop:
            result = {
                'id': prop.id,
                'name': prop.name,
                'code': prop.code,
                'ptype': prop.ptype,
                'measure': prop.measure,
                'search_facet': prop.search_facet,
                'group_id': prop.group_id,
            }
            cache.set(cache_var, result, cache_time)
            return result
        return {}

    def get_prop_value(self, cache_time: int = 600):
        """Заполняем и получаем значение свойства используя кэш"""
        cache_var = 'get_prop_value_%s_%s' % (self.prop_id, settings.PROJECT_NAME)
        inCache = cache.get(cache_var)
        if inCache:
            return inCache
        prop_value = PropertiesValues.objects.filter(pk=self.prop_id).first()
        if prop_value:
            result = {
                'id': prop_value.id,
                'str_value': prop_value.str_value,
                'digit_value': prop_value.digit_value,
                'code': prop_value.code,
                'prop_id': prop_value.prop_id,
            }
            cache.set(cache_var, result, cache_time)
            return result
        return {}

    def get_prop_value_str_value(self):
        """Возвращает строковое значение из значения свойства"""
        return self.get_prop_value().get('str_value')

    def get_prop_value_digit_value(self):
        """Возвращает числовое значение из значения свойства"""
        return self.get_prop_value().get('digit_value')

    def get_prop_value_digit_value(self):
        """Возвращает строковое значение из значения свойства"""
        return self.get_prop_value().get('digit_value')

    def get_prop_value_code(self):
        """Возвращает код из значения свойства"""
        return self.get_prop_value().get('code')

    def get_prop_id(self):
        """Возвращает ид свойства"""
        return self.get_prop().get('id')

    def get_prop_name(self):
        """Возвращает код свойства"""
        return self.get_prop().get('name')

    def get_prop_code(self):
        """Возвращает код свойства"""
        return self.get_prop().get('code')

    def get_prop_ptype(self):
        """Возвращает код свойства"""
        return self.get_prop().get('ptype')

    def get_prop_measure(self):
        """Возвращает код свойства"""
        return self.get_prop().get('measure')

    def get_prop_search_facet(self):
        """Возвращает код свойства"""
        return self.get_prop().get('search_facet')

    def get_prop_group_id(self):
        """Возвращает код свойства"""
        return self.get_prop().get('group_id')

    def get_rubrics(self):
        """Категории товаров в которых представлены товары с таким свойством
           товар знаем, у товара есть рубрики, их возьмем
        """
        # Берем кэш переменную из товара по ид товара
        cache_var = 'get_rubrics_%s_%s' % (self.product_id, settings.PROJECT_NAME)
        inCache = cache.get(cache_var)
        if inCache:
            return inCache
        product = Products.objects.filter(pk=self.product_id).first()
        if product:
            rubrics = product.get_rubrics()
            return rubrics

class ProductsCats(models.Model):
    """Рубрики товаров"""
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    container = models.ForeignKey(Containers, blank=True, null=True, on_delete=models.CASCADE)
    cat = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.CASCADE)

class ProductsPhotos(Standard):
    """Галереи для товаров"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class CostsTypes(Standard):
    """Разные типы цен для товаров"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    currency = models.IntegerField(choices=CURRENCY_CHOICES,
        blank=True, null=True, db_index=True)

class Costs(models.Model):
    """Цены для товара/услуги
       Если у товара/услуги несколько цен (опт, розн)
    """
    measure_choices = (
      (1, 'шт'),
      (2, 'л'),
    )
    cost_type = models.ForeignKey(CostsTypes, blank=True, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, blank=True, null=True, on_delete=models.CASCADE)
    measure = models.IntegerField(choices=measure_choices, blank=True, null=True, db_index=True)
    cost = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, db_index=True) # 99 000 000 000,00

