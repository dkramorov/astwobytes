# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

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
