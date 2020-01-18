# -*- coding: utf-8 -*-
import mimetypes
from django.db import models

from apps.main_functions.models import Standard

class Files(Standard):
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    link = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    desc = models.TextField(blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    path = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Стат.контет - Файлы'
        verbose_name_plural = 'Стат.контент - Файлы'

    def save(self, *args, **kwargs):
        super(Files, self).save(*args, **kwargs)
        path = '%s/%s' % (self.get_folder(), self.path)
        mime = mimetypes.MimeTypes()
        mime_type = mime.guess_type(path)
        if not mime_type:
            mime_type = 'application/force-download'
        else:
            mime_type = mime_type[0]
        Files.objects.filter(pk=self.id).update(mime=mime_type)

