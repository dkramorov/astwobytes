# -*- coding: utf-8 -*-
import os
import logging
import json
import requests
import time
import random
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count

from apps.main_functions.fortasks import search_process
from apps.main_functions.files import drop_folder
from apps.main_functions.date_time import date_plus_days
from apps.spamcha.models import SpamTable, SpamRow, EmailAccount, SpamRedirect
from apps.telegram.telegram import TelegramBot

logger = logging.getLogger(__name__)
bot = TelegramBot()

def get_accounts():
    """Достаем аккаунты для спама
       :return accounts, len_accounts, ind_accounts:
               аккаунты  длина аккаунтов индекс начала
    """
    accounts = EmailAccount.objects.filter(is_active=True)
    accounts = list(accounts)
    random.shuffle(accounts)
    return accounts, len(accounts), 0

def update_accounts():
    """Обновляем аккаунты для спама,
       если аккаунт отключен и прошло больше 24 часов,
       тогда включаем такой аккаунт"""
    accounts = EmailAccount.objects.filter(is_active=False)
    now = datetime.datetime.now()
    minus24hours = date_plus_days(now, hours=-24)
    for account in accounts:
        if account.updated < minus24hours:
            account.is_active = True
            account.save()

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Do not send email')
        parser.add_argument('--spam_id',
            action = 'store',
            dest = 'spam_id',
            type = str,
            default = False,
            help = 'Set spam id')
        parser.add_argument('--spam_delay',
            action = 'store',
            dest = 'spam_delay',
            type = str,
            default = False,
            help = 'Set spam_delay')
        parser.add_argument('--dest_email',
            action = 'store',
            dest = 'dest_email',
            type = str,
            default = False,
            help = 'Set dest_email')
        parser.add_argument('--images_with_watermarks',
            action = 'store_true',
            dest = 'images_with_watermarks',
            default = False,
            help = 'Place watermarks on images')


    def handle(self, *args, **options):
        """Задача для рассылки
           python manage.py spam_task --spam_id=3 --dest_email=dk@223-223.ru --spam_delay=3 --images_with_watermarks --fake
        """
        is_running = search_process(q = ('spam_task', 'manage.py'))
        if is_running:
            logger.info('Already running %s' % (is_running, ))
            exit()

        by = 100
        SPAM_DELAY = 120

        if options.get('spam_delay'):
            SPAM_DELAY = int(options['spam_delay'])

        dest_email = None
        if options.get('dest_email'):
            dest_email = options['dest_email']

        fake = False
        if options.get('fake'):
            fake = True

        images_with_watermarks = False
        if options.get('images_with_watermarks'):
            images_with_watermarks = True

        update_accounts()

        # Получаем на вход ид рассыли
        spam = None
        if options.get('spam_id'):
            spam_id = int(options['spam_id'])
            spam = SpamTable.objects.filter(pk=spam_id).first()
        else:
            spam = SpamTable.objects.filter(is_active=True).first()
        if not spam:
            inf = 'Spam not found'
            logger.info(inf)
            bot.send_message('%s %s' % (spam.get_emoji('hot'), inf))
            return

        inf = '--- %s. %s (%s) ---' % (spam.id, spam.name, spam.tag)
        logger.info(inf)
        bot.send_message(inf)

        original_msg = spam.msg
        # Достаем все аккаунты
        accounts, accounts_len, acc_ind = get_accounts()
        if not accounts_len:
            inf = 'ACCOUNTS ABSENTS'
            logger.info(inf)
            bot.send_message('%s %s' % (bot.get_emoji('hot'), inf))
            return
        # Вытаскиваем получателей
        query = SpamRow.objects.filter(spam_table=spam, is_active=True)
        total_records = query.aggregate(Count('id'))['id__count']
        if not total_records:
            SpamTable.objects.filter(pk=spam.id).update(is_active=False)

            inf = 'SpamTable %s done' % spam.id
            logger.info(inf)
            bot.send_message('%s %s' % (bot.get_emoji('hot'), inf))
            return

        total_pages = total_records / by + 1
        total_pages = int(total_pages)
        counter = 0
        for i in range(total_pages):
            rows = query[i*by:i*by+by]
            for row in rows:
                if acc_ind >= accounts_len - 1:
                    acc_ind = 0
                acc = accounts[acc_ind]

                acc_ind += 1
                if not fake and not dest_email:
                    SpamRow.objects.filter(pk=row.id).update(is_active=False)

                # Хак на тест по dest_email
                if dest_email:
                    row.dest = dest_email
                drop_folder('sp-images/resized')
                kwargs = {
                    'email': row.dest,
                    'client_id': row.client_id,
                    'client_name': row.client_name,
                    'images_with_watermarks': images_with_watermarks,
                    'watermark_rotate': random.randrange(0, 360),
                }
                msg = spam.get_text_msg(msg_type='html', **kwargs)

                inf = '%s, %s=>%s' % (counter, acc.email, kwargs)
                logger.info(inf)
                bot.send_message(inf)

                if not fake:
                    try:
                        acc.send_email(msg, row.dest)
                        counter += 1
                    except Exception as e:
                        logging.info(e)
                        bot.send_message('%s %s' % (bot.get_emoji('hot'), e))

                        inf = 'Blocking acc %s' % acc.email
                        logging.info(inf)
                        bot.send_message('%s %s' % (bot.get_emoji('hot'), inf))

                        acc.is_active=False
                        acc.save()
                        accounts, accounts_len, acc_ind = get_accounts()
                        if not accounts_len:
                            inf = 'ACCOUNTS ABSENTS'
                            logger.info(inf)
                            bot.send_message('%s %s' % (bot.get_emoji('hot'), inf))
                            return

                time.sleep(SPAM_DELAY)
                spam.msg = original_msg


        SpamTable.objects.filter(pk=spam.id).update(is_active=False)
        inf = 'SpamTable %s done' % spam.id
        logger.info(inf)
        bot.send_message('%s %s' % (bot.get_emoji('hot'), inf))



