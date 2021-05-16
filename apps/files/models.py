# -*- coding: utf-8 -*-
import mimetypes
from urllib.parse import quote

from django.db import models

from apps.main_functions.models import Standard

class Files(Standard):
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Название для файла')
    link = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Пользовательская ссылка на файл')
    desc = models.TextField(blank=True, null=True,
        verbose_name='Описание')
    mime = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Mime-type')
    path = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Внутренняя ссылка на файл')
    domain = models.IntegerField(db_index=True,
        blank=True, null=True,
        verbose_name='Домен для мультиязычного сайта')

    class Meta:
        verbose_name = 'Стат.контет - Файл'
        verbose_name_plural = 'Стат.контент - Файлы'

    def save(self, *args, **kwargs):
        super(Files, self).save(*args, **kwargs)
        self.update_mimetype()

    def update_mimetype(self):
        """Обновление mimetype,
           для случаем, когда не через сохранение загружаем файл
        """
        if not self.id or not self.path:
            return
        path = '%s/%s' % (self.get_folder(), self.path)
        mime = mimetypes.MimeTypes()
        mime_type = mime.guess_type(path)
        if not mime_type:
            mime_type = 'application/force-download'
        else:
            mime_type = mime_type[0]
        Files.objects.filter(pk=self.id).update(mime=mime_type)
        self.mime = mime_type

    def content_disposition_for_cyrillic_name(self, name):
        """Если нужно скачать файл с названием в кириллице,
           по-другому, просто будет временное имя файла
           :param name: название файла в кириллице

           USAGE:
           response = HttpResponse(f.read(), content_type=self.mime)
           response['Content-Disposition'] =
               self.content_disposition_for_cyrillic_name(self.name)
        """
        return 'attachment; filename*=UTF-8\'\'{}'.format(quote(name))

