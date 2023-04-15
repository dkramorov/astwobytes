# -*- coding: utf-8 -*-
import time
import datetime
import os
import random

from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from apps.main_functions.files import (
    check_path,
    make_folder,
    full_path,
    drop_folder,
    drop_file,
    imageThumb,
    extension,
    catch_file,
    open_file,
    analyze_res_path,
    imagine_image,
    grab_image_by_url,
    create_captcha,
)
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
        """Папка для модели (например, для изображений)
        """
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
        """Удаление папки экземпляра модели"""
        if not self.id:
            return
        folder = self.get_folder()
        drop_folder(folder)
        parent_folder = os.path.split(folder.rstrip('/'))[0]
        if check_path(parent_folder):
            return
        pass_items = ('.DS_Store', )
        parent_folder_fp = full_path(parent_folder)
        items_in_folder = [item for item in os.listdir(parent_folder_fp) if not item in pass_items]
        if not items_in_folder:
            os.rmdir(parent_folder_fp)

    def upload_img(self, img):
        """Загрузка изображения
           :param img: изображение
                      (например, request.FILES - InMemoryUploadedFile)
        """
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
                new_img = '%s%s' % (self.id, ext)
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

    def upload_file(self, fname,
                    field: str,
                    additional_update: dict = None):
        """Загрузка файла в нужное поле
           :param fname: файл
           :param field: поле в которое загружаем файл
           :param additional_update: доп. поля, которые хотим
                                     обновить у модели,
                                     например, {'name': '123.txt'}
        """
        new_fname = None
        if not hasattr(self, field):
            return None
        if not additional_update:
            additional_update = {}
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
        params = {
            field: new_fname,
        }
        params.update(additional_update)
        if catch_file(fname, path):
            self.__class__.objects.filter(pk=self.id).update(**params)
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
           files => imagine_image only ПУТЬ
        """
        path = analyze_res_path(self.img, self.get_folder())
        if path.startswith('http') or path.startswith('/static/'):
            return path
        return '/media/%s' % path

    def thumb(self, size: str = '150x150'):
        """Путь до миниатюры
           :param size: размер фото через x, например, 123х321
        """
        path = analyze_res_path(self.img, self.get_folder())
        if path.startswith('http') or path.startswith('/static/'):
            return path # ?size=150x150
        return imagine_image(self.img, size, self.get_folder(), 'resized')

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
    user = models.ForeignKey(User,
                             blank = True, null = True,
                             on_delete = models.CASCADE)
    class Meta:
        verbose_name = 'Админка - Настройка'
        verbose_name_plural = 'Админка - Настройки'

    def __str__(self):
        return 'id=%s, name=%s, attr=%s, value=%s, user_id=%s' % (
            self.id, self.name, self.attr, self.value, self.user_id,
        )


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

class Captcha(models.Model):
    """Капча от бота
    """
    value = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Сгенерированная строка')

    def get_folder(self):
        """Путь к папке с капчами,
           капча всегда называется id.png
        """
        path_to_save = 'captcha'
        if check_path(path_to_save):
            make_folder(path_to_save)
        return path_to_save

    def get_captcha(self):
        """Возращаем путь к капче
           капча всегда называется id.png
        """
        if not self.id:
            return None
        return os.path.join(self.get_folder(), '%s.png' % self.id)

    def time(self):
        """Время, чтобы капча не кэшировалась"""
        return str(time.time()).replace('.', '_')

    def get_for_feedback(self):
        """Получение ид капчи для проверки
           на робота в форме обратной связи
        """
        enough = 30

        query = Captcha.objects.all()
        total_captchas = query.aggregate(models.Count('id'))['id__count']
        if total_captchas > enough:
            ids = query.values_list('id', flat=True)[:enough]
            ids = list(ids)
            random.shuffle(ids)
            return ids[0]
        else:
            new_captcha = Captcha().gen_captcha()
            return new_captcha.id

    def gen_captcha(self,
                    alphabet: list = None,
                    captcha_size: int = 4,
                    font: str = 'fonts/PerfoCone.ttf',
                    font_size: int = 26):
        """Генерирует капчу и возвращает (id, path_to_image)
           либо, если их скажем больше какого-то количества,
           можно сразу возвращать готовую
           :param alphabet: символы из которых будем делать капчу
           :param size: количество символов в изображении
           :param font: путь к шрифту в static
           :param font_size: размер шрифта
        """
        result = ''

        value, img = create_captcha(
            alphabet,
            captcha_size,
            font,
            font_size,
        )

        new_captcha = Captcha.objects.create(value=value)
        img_name = '%s.png' % new_captcha.id
        fname = full_path(os.path.join(new_captcha.get_folder(), img_name))
        img.save(fname, 'PNG')
        return new_captcha

    def check_captcha(self, captcha_id: str, user_value: str):
        """Верификация проверочного кода
           Например,
           В POST должен прийти id капчи
           В POST должен прийти digits,
           введенный пользователем

           :param captcha_id: ид каптчи
           :param user_value: значение, переданное пользователем
        """
        captcha_id = '%s' % captcha_id
        if not captcha_id.isdigit():
            return False
        captcha = Captchas.objects.filter(pk=captcha_id).first()
        if captcha and captcha.value == user_value:
            return True
        return False

    def delete(self, *args, **kwargs):
        """OVERRIDE DELETE METHOD"""
        path = self.get_captcha()
        if path:
            drop_file(path)
        super(Captcha, self).delete(*args, **kwargs)
