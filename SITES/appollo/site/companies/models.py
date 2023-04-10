# -*- coding: utf-8 -*-
import os

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.models import Standard
from apps.addresses.models import Address
from apps.flatcontent.models import Blocks

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
    imagine_image,
    grab_image_by_url,
)


class MainCompany(Standard):
    """Сущность для группы компаний
    """
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    resume = models.TextField(blank=True, null=True)
    img_view = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Изображение для компании')

    def drop_img_view(self):
        """Удаление изображения"""
        if not self.id:
            return
        if self.img_view:
            print("__")
            folder = self.get_folder()
            drop_file(os.path.join(folder, self.img_view))
            drop_folder(os.path.join(folder, 'resized'))
            self.__class__.objects.filter(pk=self.id).update(img_view=None)
            self.img_view = None

    def upload_img_view(self, img):
        """Загрузка изображения
           :param img: изображение
                      (например, request.FILES - InMemoryUploadedFile)
        """
        new_img = None
        if self.img_view:
            self.drop_img_view()
        # ---------------------------------------------------
        # django.core.files.uploadedfile.InMemoryUploadedFile
        # ---------------------------------------------------
        if type(img) == InMemoryUploadedFile:
            ext = extension(img.name)
            if ext:
                media_folder = self.get_folder()
                if check_path(media_folder):
                    make_folder(media_folder)
                new_img = 'view_%s%s' % (self.id, ext)
                path = os.path.join(media_folder, new_img)
                if catch_file(img, path):
                    imageThumb(path, 1920, 1280)
        # ------------------------------
        # Загрузка изображения по ссылке
        # ------------------------------
        elif type(img) == str:
            ext = extension(img)
            view = 'view_%s%s' % (self.id, ext)
            new_img = grab_image_by_url(img, self.get_folder(), name=view)
            if new_img:
                path = os.path.join(self.get_folder(), new_img)
                img = imageThumb(path, 1920, 1280)
                if not img:
                    self.drop_img_view()
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
            new_img = 'view_{}{}'.format(str(self.id), ext)
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

        self.__class__.objects.filter(pk=self.id).update(img_view=new_img)
        self.img_view = new_img
        return new_img

    def imagine_view(self):
        """Возвращаем полный путь к картинке
           Аналогично mtags => imagine,
           files => imagine_image only ПУТЬ"""

        img_path = ''
        if self.img_view:
            if self.img_view.startswith('http'):
                return self.img_view
            img_path = '/media/%s%s' % (self.get_folder(), self.img_view)
        return img_path

    def thumb_view(self, size: str = '150x150'):
        """Путь до миниатюры
           :param size: размер фото через x, например, 123х321
        """
        if self.img_view:
            if self.img_view.startswith('http'):
                return '%s?size=150x150' % self.img_view
            return imagine_image(self.img_view, size, self.get_folder())
        # можно в settings положить путь к пустой картинке
        return '/static/img/ups.png'

class MainCompany2Category(models.Model):
    """Связка группы компаний с категориями"""
    main_company = models.ForeignKey(MainCompany, blank=True, null=True, on_delete=models.CASCADE)
    cat = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.CASCADE)

class Company(Standard):
    """Компания, по сути это филиал компании
       может быть головной офис
    """
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    site = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    email = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    twitter = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    facebook = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    instagram = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    phone = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    main_company = models.ForeignKey(MainCompany, blank=True, null=True,
        verbose_name='Родительская компания группы филиалов', on_delete=models.SET_NULL)
    address = models.ForeignKey(Address, blank=True, null=True,
        verbose_name='Адрес', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Компании - филиал'
        verbose_name_plural = 'Компании - филиалы'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = kill_quotes(self.phone, 'int')
        super(Company, self).save(*args, **kwargs)

class Company2Category(models.Model):
    """Связка филиалов с категориями"""
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
    cat = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.CASCADE)

class Contact(Standard):
    """Контакты компаний, пока только телефоны"""
    ctype_choices = (
        (1, 'phone'),
        (2, 'site'),
        (3, 'email'),
        (4, 'twitter'),
        (5, 'facebook'),
        (6, 'instagram'),
    )
    state_choices = (
        (10, 'company_owner'),
    )
    main_company = models.ForeignKey(MainCompany,
        blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company,
        blank=True, null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Значение в человеческом виде')
    indexed_value = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Значение для индексации')
    ctype = models.IntegerField(choices=ctype_choices,
        blank=True, null=True, db_index=True)
    comment = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Комментарий к телефону')

    def save(self, *args, **kwargs):
        if self.ctype == 1 and self.value:
            self.indexed_value = kill_quotes(self.value, 'int')
        else:
            self.indexed_value = self.value
        super(Contact, self).save(*args, **kwargs)
