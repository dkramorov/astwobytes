# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.models import Standard

def create_default_user(username: str = 'jocker',
                        email: str = 'dkramorov@mail.ru',
                        passwd: str = 'cnfylfhnysq',
                        last_name: str = 'Kramorov',
                        is_superuser: bool = True,
                        is_active: bool = True,
                        is_staff: bool = True):
    """Демо-функция для создания пользователя по умолчанию
       :param username: логин
       :param email: емайл
       :param last_name: фамилия
       :param is_superuser: суперадми
       :param is_active: включен
       :param is_staff: в штате
    """
    if User.objects.filter(username=username).first():
        return
    user = User.objects.create_user(username, email, passwd)
    user.set_password(passwd)
    user.last_name = last_name
    user.is_superuser = is_superuser
    user.is_active = is_active
    user.is_staff = is_staff
    user.save()
    return user

class customUser(Standard):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер телефона')
    function = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Должность')

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = kill_quotes(self.phone, 'int')
        super(customUser, self).save(*args, **kwargs)

    def __str__(self):
        name = self.user.username
        if self.user.last_name or self.user.first_name:
            name = ''
        if self.user.last_name:
            name += self.user.last_name + ' '
        if self.user.first_name:
            name += self.user.first_name + ' '
        return name.strip()

    @staticmethod
    def get_name(user: User) -> str:
        if user.last_name and user.first_name:
            return '%s %s (%s id=%s)' % (user.last_name, user.first_name, user.username, user.id)
        if user.last_name or user.first_name:
            return '%s (%s id=%s)' % (user.last_name or user.first_name, user.username, user.id)
        return '%s (id=%s)' % (user.username, user.id)

@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        customUser.objects.create(user=instance)

@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customuser.save()

class ExtraFields(Standard):
    """Дополнительные поля к модели пользователя
       Вспомогательная модель (использовать для personal?),
       чтобы руками не вводить, а просто заполнять
       Если прописана группа, значит выводим доп. поля только
       если пользователь принадлежит к группе
    """
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    field = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    show_in_table = models.BooleanField(db_index=True, default=False,
        verbose_name='Показывать в таблице принудительно')
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Доп. поле пользователя'
        verbose_name_plural = 'Доп. поля пользователей'
        default_permissions = []

class ExtraValues(Standard):
    """Значения к дополнительным полям модели пользователя
       Вспомогательная модель (использовать для personal?),
       чтобы руками не вводить значения, а выбирать (если есть список)
    """
    field = models.ForeignKey(ExtraFields, blank=True, null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Значение на доп. поле пользователя'
        verbose_name_plural = 'Значниея на доп. поля пользователей'
        default_permissions = []

class ExtraInfo(models.Model):
    """Поля и значения дополнительных полей для модели пользователя
       (использовать для personal?)
    """
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    field = models.ForeignKey(ExtraFields, blank=True, null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Доп. поле пользователя'
        verbose_name_plural = 'Доп. поля пользователей'
        default_permissions = []

#myuser.groups.set([group_list])
#myuser.groups.add(group, group, ...)
#myuser.groups.remove(group, group, ...)
#myuser.groups.clear()
#myuser.user_permissions.set([permission_list])
#myuser.user_permissions.add(permission, permission, ...)
#myuser.user_permissions.remove(permission, permission, ...)
#myuser.user_permissions.clear()
# default permissions
#add: user.has_perm('foo.add_bar')
#change: user.has_perm('foo.change_bar')
#delete: user.has_perm('foo.delete_bar')
#view: user.has_perm('foo.view_bar')
