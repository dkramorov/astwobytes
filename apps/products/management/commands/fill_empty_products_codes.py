#-*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q

from apps.products.models import Products

logger = logging.getLogger('main')

class Command(BaseCommand):
    """Заполнение пустых кодов товаров идентификаторами"""

    def handle(self, *args, **options):
        for product_id in Products.objects.filter(Q(code__isnull=True)|Q(code='')).values_list('id', flat=True):
            Products.objects.filter(pk=product_id).update(code=product_id)
