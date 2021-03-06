# -*- coding: utf-8 -*-
from django.db import models

from apps.flatcontent.models import (Containers,
                                     Blocks,
                                     link_containers2block,
                                     get_link_containers, )
from apps.main_functions.models import Standard
from apps.main_functions.string_parser import translit

CURRENCY_CHOICES = (
    (1, "₽"),
    (2, "$"),
)

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
        if self.code:
            self.code = str(self.code).replace('-', '_')
        super(Products, self).save(*args, **kwargs)
        if self.id and not self.code:
            Products.objects.filter(pk=self.id).update(code=self.id)

    def link(self):
        """Ссылка на товар/услугу"""
        link = '/product/%s/' % self.id
        if self.code and self.name:
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

class Property(Standard):
    """Свойство для товара"""
    ptype_choices = (
        (1, 'Выпадающий список select'),
        (2, 'Выпадающий список с множественным выбором multiselect'),
        (3, 'Выбор из вариантов radio'),
        (4, 'Множественный выбор из вариантов checkbox'),
    )
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    ptype = models.IntegerField(choices=ptype_choices,
        blank=True, null=True, db_index=True)
    measure = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Единица измерения')
    search_facet = models.BooleanField(db_index=True, default=False,
        verbose_name='Отображать в фильтрах для поиска')

class PropertiesValues(Standard):
    """Свойства для товаров/услуг
       это точные свойства, то есть, не текст от балды,
       а именно конкретное свойство с конкретным значением
    """
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    str_value = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # По большей части для сортировки и фильтров
    digit_value = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=4, db_index=True) # 990 000 000,0000

    def save(self, *args, **kwargs):
        if self.str_value:
            try:
                self.digit_value = float(self.str_value.replace(',', '.'))
            except Exception:
                self.digit_value = None

        if self.digit_value and (self.digit_value > 999999999 or self.digit_value < -999999999):
            self.digit_value = None
        super(PropertiesValues, self).save(*args, **kwargs)

class ProductsProperties(models.Model):
    """Линковка значения свойства к товару"""
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    prop = models.ForeignKey(PropertiesValues, on_delete=models.CASCADE)

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

