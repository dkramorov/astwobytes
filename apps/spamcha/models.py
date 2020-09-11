# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.main_functions.string_parser import kill_quotes

class EmailBlackList(Standard):
    """Список email'ов на которые нельзя отправлять почту
       по различным причинам"""
    email = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    reason = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Рассылка - Черный список'
        verbose_name_plural = 'Рассылка - Черный список'

class EmailAccount(Standard):
    """Наши аккаунты, с которых мы хотим осуществлять рассылку"""
    email = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    passwd = models.CharField(max_length=255, blank=True, null=True)
    smtp_server = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    smtp_port = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Рассылка - Аккаунты'
        verbose_name_plural = 'Рассылка - Аккаунты'

    def send_email(self, msg, recipient: str = 'dk@223-223.ru'):
        """Отправка email сообщения
           Сообщение =>
           from email.mime.text import MIMEText
           from email.header import Header
           msg = MIMEText(text, 'plain', 'utf-8')
           msg['Subject'] = Header(self.name, 'utf-8')
           msg['From'] = account.email
           msg['To'] = ', '.join(recipients)"""
        import smtplib
        if not self.email or not self.smtp_server or not self.smtp_port or not self.passwd:
            return
        # Дополняем заголовки сообщения
        msg['From'] = self.email
        msg['To'] = recipient
        try:
            session = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
            session.set_debuglevel(1)
            session.starttls()
            session.login(self.email, self.passwd)
            session.sendmail(msg['From'], recipient, msg.as_string())
        finally:
            session.quit()

class SpamTable(Standard):
    """Таблица для рассылки"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    msg = models.TextField(blank=True, null=True, verbose_name='Сообщение для отправки')
    html_msg = models.TextField(blank=True, null=True, verbose_name='Сообщение, созданное в конструкторе')
    # Заголовки для емайлов
    reply_to = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Адрес для ответа')

    class Meta:
        verbose_name = 'Рассылка - Таблицы рассылки'
        verbose_name_plural = 'Рассылка - Таблицы рассылки'

    def get_text_msg(self, msg_type: str = 'plain'):
       """Сформировать текстовое сообщение для отправки"""
       from email.mime.text import MIMEText
       from email.header import Header
       if not self.msg:
           return
       if not msg_type in ('plain', 'html'):
           msg_type = 'plain'
       msg = MIMEText(self.msg, msg_type, 'utf-8')
       msg['Subject'] = Header(self.name, 'utf-8')
       #msg['From'] = account.email
       #msg['To'] = ', '.join(recipients)
       if self.reply_to:
           msg.add_header('reply-to', self.reply_to)
       return msg

class SpamRow(Standard):
    """Запись в таблице для рассылки"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    dest = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Получатель')
    spam_table = models.ForeignKey(SpamTable, blank=True, null=True, on_delete=models.CASCADE)
    sender = models.ForeignKey(EmailAccount, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Рассылка - Записи в таблицах рассылок'
        verbose_name_plural = 'Рассылка - Записи в таблицах рассылок'

class SMSPhone(Standard):
    """Телефоны для смс рассылки"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Название телефона, например, Samsung Galaxy A5')
    phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер телефона, например, 89501100222')
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='ИД телефона, например, 123321')
    sent = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Кол-во отправленных смс')
    limit = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Максимальное кол-во для отправки')
    class Meta:
        verbose_name = 'Рассылка - Телефон для смс'
        verbose_name_plural = 'Рассылка - Телефоны для смс'
        #default_permissions = []

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = kill_quotes(self.phone, 'int')
        super(SMSPhone, self).save(*args, **kwargs)
