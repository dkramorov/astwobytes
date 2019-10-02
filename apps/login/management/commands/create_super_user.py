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

class Command(BaseCommand):
    def handle(self, *args, **options):
        """Создаем супер-пользователя"""
        if not User.objects.filter(username='jocker'):
            create_super_user()


