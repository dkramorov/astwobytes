# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from django.conf import settings

from apps.main_functions.string_parser import GenPasswd, random_boolean

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.exclude(username='jocker').delete()
        usernames = []
        for i in range(500):
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
        User.objects.bulk_create(users)


