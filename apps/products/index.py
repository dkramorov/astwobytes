# -*- coding: utf-8 -*-
#from djapian import space, Indexer, CompositeIndexer
from djapian.forindex import space, NewIndexer
from apps.products.models import (
    Products,
    Property,
    PropertiesValues,
    ProductsProperties,
)

class ProductsIndexer(NewIndexer):
    """Индекс по товарам
       нужны фасеты, которые мы должны добавить в doc.add_value
    """
    fields = (
        'name',
        'altname',
        'manufacturer',
        'dj_info',
    )
    tags = [
        ('id', 'id'),
        ('code', 'code', 2),
        ('get_rubrics', 'get_rubrics'),
        ('get_props', 'get_props'),
        ('get_values', 'get_values'),
    ]

space.add_index(Products, ProductsIndexer, attach_as='indexer')


class PropertyIndexer(NewIndexer):
    """Индекс по свойствам"""
    tags = [
        ('id', 'id'),
        ('name', 'name'),
        ('code', 'code'),
        ('ptype', 'ptype'),
        ('measure', 'measure'),
        ('search_facet', 'search_facet'),
    ]

space.add_index(Property, PropertyIndexer, attach_as='indexer')


class PropertiesValuesIndexer(NewIndexer):
    """Индекс по свойствам"""
    tags = [
        ('id', 'id'),
        ('get_prop_id', 'get_prop_id'),
        ('str_value', 'str_value'),
        ('digit_value', 'digit_value'),
        ('code', 'code'),
    ]

space.add_index(PropertiesValues, PropertiesValuesIndexer, attach_as='indexer')


class ProductsPropertiesIndexer(NewIndexer):
    """Индекс по значениям свойств по товарам"""
    tags = [
        ('get_product_id', 'get_product_id'),
        ('get_prop_value_id', 'get_prop_value_id'),
        ('get_prop_value_str_value', 'get_prop_value_str_value'),
        ('get_prop_value_digit_value', 'get_prop_value_digit_value'),
        ('get_prop_value_code', 'get_prop_value_code'),

        ('get_prop_id', 'get_prop_id'),
        ('get_prop_name', 'get_prop_name'),
        ('get_prop_code', 'get_prop_code'),
        ('get_prop_ptype', 'get_prop_ptype'),
        ('get_prop_measure', 'get_prop_measure'),
        ('get_prop_search_facet', 'get_prop_search_facet'),
        ('get_prop_group_id', 'get_prop_group_id'),
        # Категории товаров, в которых представлены свойства
        ('get_rubrics', 'get_rubrics'),
    ]

space.add_index(ProductsProperties, ProductsPropertiesIndexer, attach_as='indexer')
