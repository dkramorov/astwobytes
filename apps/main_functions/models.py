# -*- coding: utf-8 -*-
import time
import datetime
import os

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from apps.main_functions.files import (check_path,
                                       make_folder,
                                       full_path,
                                       drop_folder,
                                       drop_file,
                                       imageThumb,
                                       extension,
                                       catch_file,
                                       open_file,
                                       imagine_image,
                                       grab_image_by_url, )
from apps.main_functions.problem32folders import get_smart_folder

class Standard(models.Model):
    """Абстрактная модель
       Стандартная модель"""
    img = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    position = models.IntegerField(blank=True, null=True, db_index=True)
    is_active = models.BooleanField(db_index=True, default=True)
    state = models.IntegerField(blank=True, null=True, db_index=True)
    parents = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
      abstract = True

    def get_folder(self):
        if not self.id:
            return ''
        return '%s_%s/%s%s/' % (self._meta.app_label.lower(), self._meta.object_name.lower(), get_smart_folder(self.id), self.id)

    def drop_resized_folder(self):
        """Удаление папки с миниатюрами"""
        if not self.id:
            return
        folder = self.get_folder()
        drop_folder(os.path.join(folder, 'resized'))

    def drop_img(self):
        """Удаление изображения"""
        if not self.id:
            return
        if self.img:
            folder = self.get_folder()
            drop_file(os.path.join(folder, self.img))
            drop_folder(os.path.join(folder, 'resized'))
            self.__class__.objects.filter(pk=self.id).update(img=None)
            self.img = None

    def drop_file(self, field):
        """Удаление файла"""
        if not self.id:
            return
        if hasattr(self, field):
            path = getattr(self, field)
            if path:
                folder = self.get_folder()
                drop_file(os.path.join(folder, path))
                self.__class__.objects.filter(pk=self.id).update(**{field:None})
                setattr(self, field, None)

    def drop_media(self):
        """Удаление папки"""
        if not self.id:
            return
        drop_folder(self.get_folder())

    def upload_img(self, img):
        """Загрузка изображения"""
        new_img = None
        if self.img:
            self.drop_img()
        # ---------------------------------------------------
        # django.core.files.uploadedfile.InMemoryUploadedFile
        # ---------------------------------------------------
        if type(img) == InMemoryUploadedFile:
            ext = extension(img.name)
            if ext:
                media_folder = self.get_folder()
                if check_path(media_folder):
                    make_folder(media_folder)
                new_img = "%s%s" % (self.id, ext)
                path = os.path.join(media_folder, new_img)
                if catch_file(img, path):
                    imageThumb(path, 1920, 1280)
        # ------------------------------
        # Загрузка изображения по ссылке
        # ------------------------------
        elif type(img) == str:
            new_img = grab_image_by_url(img, self.get_folder(), str(self.id))
            if new_img:
                path = os.path.join(self.get_folder(), new_img)
                img = imageThumb(path, 1920, 1280)
                if not img:
                    self.drop_img()
                    return None
            else:
                new_img = None
        # ----------------------------------------------------
        # django.core.files.uploadedfile.TemporaryUploadedFile
        # ----------------------------------------------------
        elif type(img) == TemporaryUploadedFile:
            path = img.temporary_file_path()
            tmp_file = open(path, 'rb')
            img_content = tmp_file.read()
            tmp_file.close()
            ext = extension(img.name)
            new_img = '{}{}'.format(str(self.id), ext)
            media_folder = self.get_folder()
            if check_path(media_folder):
                make_folder(media_folder)
            dest = os.path.join(media_folder, new_img)
            img_file = open_file(dest ,'wb+')
            img_file.write(img_content)
            img_file.close()
            img = imageThumb(dest, 1920, 1280)
            if not img:
                self.drop_img()
                return None
        else:
            logger.error('Unknown img type %s' % (type(img), ))
            assert False

        self.__class__.objects.filter(pk=self.id).update(img=new_img)
        self.img = new_img
        return new_img

    def upload_file(self, fname, field):
        """Загрузка файла в нужное поле"""
        new_fname = None
        if not hasattr(self, field):
            return None
        self.drop_file(field)
        media_folder = self.get_folder()
        if check_path(media_folder):
            make_folder(media_folder)
        ext = fname.name.split(".")[-1]
        if len(ext) > 5:
            return None
        # ---------------------------------------------
        # field подставляем, чтобы не заменило картинку
        # или чтобы не совпало с другими ибучими полями
        # ---------------------------------------------
        new_fname = "%s_%s.%s" % (field, self.id, ext)
        path = os.path.join(media_folder, new_fname)
        if catch_file(fname, path):
            self.__class__.objects.filter(pk=self.id).update(**{field:new_fname})
            setattr(self, field, new_fname)
        else:
            self.__class__.objects.filter(pk=self.id).update(**{field:None})
            setattr(self, field, None)
        return new_fname

    def delete(self, *args, **kwargs):
      """Удаление объекта с подобъектами"""
      parents = self.parents
      if not parents:
          parents = ''
      children = self.__class__.objects.filter(parents='%s_%s' % (parents, self.id))
      for child in children:
          child.delete()
          child.drop_media()
      self.drop_media()
      super(Standard, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
      """Сохранение объекта"""
      if not self.position:
          maxpos = self.__class__.objects.all().aggregate(models.Max('position'))['position__max']
          if not maxpos:
              maxpos = 1
          else:
              maxpos += 1
          self.position = maxpos
      super(Standard, self).save(*args, **kwargs)

    def imagine(self):
        """Возвращаем полный путь к картинке
           Аналогично mtags => imagine,
           files => imagine_image only ПУТЬ"""

        img_path = ''
        if self.img:
            if self.img.startswith('http'):
                return self.img
            img_path = '/media/%s%s' % (self.get_folder(), self.img)
        return img_path

    def thumb(self, size:str = '150x150'):
        """Путь до миниатюры"""
        if self.img:
            if self.img.startswith('http'):
                return '%s?size=150x150' % self.img
            return imagine_image(self.img, size, self.get_folder())
        return ''

class Config(Standard):
    """Различные настройки"""
    name = models.CharField(max_length = 255,
                            blank = True, null = True,
                            db_index = True)
    attr = models.CharField(max_length = 255,
                            blank = True, null = True,
                            db_index = True)
    value = models.CharField(max_length = 255,
                             blank = True, null = True,
                             db_index = True)
    class Meta:
        verbose_name = 'Админка - Настрока'
        verbose_name_plural = 'Админка - Настройки'

class Tasks(Standard):
    """Задачи для call_command"""
    name = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    command = models.TextField()

    class Meta:
        verbose_name = 'Админка - Задача'
        verbose_name_plural = 'Админка - Задачи'

    def save(self, *args, **kwargs):
        analogs = Tasks.objects.filter(command=self.command)
        if analogs:
            analogs.update(updated = datetime.datetime.today())
        else:
            super(Tasks, self).save(*args, **kwargs)

