# -*- coding: utf-8 -*-
import mimetypes
from django.db import models

from apps.main_functions.string_parser import translit
from apps.main_functions.models import Standard

class Rubrics(Standard):
    """Каталог"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    altname = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    keywords = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Каталог - рубрика'
        verbose_name_plural = 'Каталог - рубрики'

    def save(self, *args, **kwargs):
        if not self.altname:
            self.find_altname()
        super(Rubrics, self).save(*args, **kwargs)

    def get_link(self):
        """Получить ссылку на рубрику"""
        altname = self.id
        if self.altname:
            altname = self.altname
        return '/cat/%s/' % (altname, )

    def link(self):
        """Получить ссылку на рубрику"""
        return self.get_link()

    def find_altname(self, z: int = 0):
      """Находим транслитное имя рубрики,
         которое не совпадает с другими именами"""
      if self.name:
          altname = translit(self.name)
          if z:
              altname = '%s-%s' % (altname, z)
          analog = Rubrics.objects.filter(altname=altname).exclude(pk=self.id).aggregate(models.Count('id'))['id__count']
          if not analog:
              self.altname = altname
          else:
              self.find_altname(z+1)

