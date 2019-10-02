# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.models import Standard

def create_default_user():
    if User.objects.filter(username='jocker').first():
        return
    user = User.objects.create_user('jocker', 'dkramorov@mail.ru', 'cnfylfhnysq')
    user.set_password('cnfylfhnysq')
    user.last_name = 'Kramorov'
    user.is_superuser = True
    user.is_active = True
    user.is_staff = True
    user.save()

class customUser(Standard):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Номер телефона')

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = kill_quotes(self.phone, 'int')
        super(customUser, self).save(*args, **kwargs)

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
