# -*- coding: utf-8 -*-
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
        parser.add_argument('--single',
            action = 'store_true',
            dest = 'single',
            default = False,
            help = 'Send to single account')
    def handle(self, *args, **options):
        """Тестовая отправка почты smtplib"""
        accounts = EmailAccount.objects.all()
        account = accounts.first()
        if not account:
            logger.warning('There are no email accounts in db')
            return
        #recipients = ['dk@223-223.ru', 'dkramorov@mail.ru']
        recipients = ['dk@223-223.ru', ]
        text = 'Привет, сейчас %s' % (datetime.datetime.today().strftime('%H:%M:%S %d-%m-%Y'))

        msg = MIMEText(text, 'plain', 'utf-8')
        msg['Subject'] = Header('Проверка', 'utf-8')
        msg['From'] = account.email
        msg['To'] = ', '.join(recipients)
        msg.add_header('reply-to', 'zergo01@yandex.ru')

        # Отправка сразу на несколько аккаунтов
        if options.get('multiple'):
            try:
                session = smtplib.SMTP(account.smtp_server, account.smtp_port, timeout=10)
                session.set_debuglevel(1)
                session.starttls()
                session.login(account.email, account.passwd)
                session.sendmail(msg['From'], recipients, msg.as_string())
            finally:
                #logger.info(msg)
                session.quit()
        if options.get('single'):
            # Если не закрывая сессию делать отправку,
            # тогда попадаем под спам-фильтр
            for recipient in recipients:
                try:
                    session = smtplib.SMTP(account.smtp_server, account.smtp_port, timeout=10)
                    session.set_debuglevel(1)
                    session.starttls()
                    session.login(account.email, account.passwd)

                    text = 'Сейчас %s' % (datetime.datetime.today().strftime('%H:%M:%S %d-%m-%Y'))
                    msg = MIMEText(text, 'plain', 'utf-8')
                    msg['Subject'] = Header('Проверка 2', 'utf-8')
                    msg['From'] = account.email
                    msg['To'] = recipient
                    msg.add_header('reply-to', 'zergo01@yandex.ru')
                    session.sendmail(msg['From'], recipient, msg.as_string())
                finally:
                    #logger.info(msg)
                    session.quit()

