# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from django.conf import settings

from apps.main_functions.string_parser import GenPasswd, random_boolean

logger = logging.getLogger(__name__)

HOW_MUCH_NEW_USERS = 200

def create_super_user():
    """Создаем себя"""
    superuser = User()
    superuser.is_active = True
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.username = 'jocker'
    superuser.email = 'dkramorov@mail.ru'
    superuser.set_password('reabhxbr')
    superuser.save()

def create_random_users():
    """Заполняем базу пользователями от балды"""
    User.objects.exclude(username='jocker').delete()
    User.objects.all().delete()
    usernames = []
    for i in range(HOW_MUCH_NEW_USERS):
        new_username = GenPasswd()
        while new_username in usernames:
            new_username = GenPasswd()
        usernames.append(new_username)
    users = []
    for username in usernames:
        new_user = User()
        new_user.is_active = random_boolean()
        new_user.is_superuser = random_boolean()
        new_user.is_staff = random_boolean()
        new_user.username = username
        new_user.email = 'dkramorov@mail.ru'
        new_user.set_password('reabhxbr')
        users.append(new_user)
        new_user.save()

class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.exclude(username='jocker'):
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.set_password('123')
            user.save()


