# -*- coding: utf-8 -*-
import time
import logging
import smtplib
import datetime

from email.mime.text import MIMEText
from email.header import Header

from django.core.management.base import BaseCommand

from django.conf import settings

from apps.spamcha.models import EmailAccount


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--multiple',
            action = 'store_true',
            dest = 'multiple',
            default = False,
            help = 'Send to multiple accounts')
        parser.add_argument('--email',
            action = 'store',
            dest = 'email',
            type = str,
            default = False,
            help = 'Set email for send')
        parser.add_argument('--custom_account',
            action = 'store',
            dest = 'custom_account',
            type = str,
            default = False,
            help = 'Set custom account [login;passwd;smtp_server;port] for send')

    def handle(self, *args, **options):
        """Тестовая отправка почты smtplib
           Если включить пароли для приложений, то будет ошибка при аутентификации,
           если использовать основной пароль аккаунта, а не пароль для приложения
           Если слать письма без интервала - попадешь в банан
        """
        pause = 10
        accounts = EmailAccount.objects.all()
        if options.get('email'):
            accounts = accounts.filter(email=email)

        if options.get('custom_account'):
            custom_account = options['custom_account'].split(';')
            acc = EmailAccount(
                email=custom_account[0],
                passwd=custom_account[1],
                smtp_server=custom_account[2],
                smtp_port=custom_account[3],
            )
            print('custom_account', acc)
            accounts = [acc]

        if not accounts:
            logger.warning('There are no email accounts in db')
            return
        #recipients = ['dk@223-223.ru', 'dkramorov@mail.ru']
        recipients = ['dk@223-223.ru', ]
        for account in accounts:
            text = 'Привет, сейчас %s' % (datetime.datetime.today().strftime('%H:%M:%S %d-%m-%Y'))

            msg = MIMEText(text, 'plain', 'utf-8')
            msg['Subject'] = Header('Проверка', 'utf-8')
            msg['From'] = account.email
            msg['To'] = ', '.join(recipients)

            for recipient in recipients:
                logger.info('%s=>%s' % (account.email, recipient))
                account.send_email(msg, recipient)
                logger.info('sleep %s' % pause)
                time.sleep(pause)
