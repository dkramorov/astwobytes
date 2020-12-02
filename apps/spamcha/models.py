# -*- coding: utf-8 -*-
import os
from django.db import models
from django.core.mail import send_mail, EmailMessage, get_connection

from apps.main_functions.models import Standard
from apps.main_functions.files import full_path
from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.catcher import REGA_IMG

class EmailBlackList(Standard):
    """Список email'ов на которые нельзя отправлять почту
       по различным причинам"""
    email = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    reason = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Рассылка - Черный список'
        verbose_name_plural = 'Рассылка - Черный список'
        #default_permissions = []

class EmailAccount(Standard):
    """Наши аккаунты, с которых мы хотим осуществлять рассылку"""
    email = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    passwd = models.CharField(max_length=255, blank=True, null=True)
    smtp_server = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    smtp_port = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Рассылка - Аккаунты'
        verbose_name_plural = 'Рассылка - Аккаунты'
        #default_permissions = []

    def send_email(self, msg, recipient: str = 'dk@223-223.ru'):
        """Отправка email сообщения
           Сообщение =>
           from email.mime.text import MIMEText
           from email.header import Header
           msg = MIMEText(text, 'plain', 'utf-8')
           msg['Subject'] = Header(self.name, 'utf-8')
           msg['From'] = account.email
           msg['To'] = ', '.join(recipients)"""
        if not self.email or not self.smtp_server or not self.smtp_port or not self.passwd:
            return
        msg['From'] = self.email
        msg['To'] = recipient
        # ---------------------------
        # Создаем бэкэнд для рассылки
        # ---------------------------
        conn = get_connection(host=self.smtp_server,
                              port=self.smtp_port,
                              username=self.email,
                              password=self.passwd,
                              use_tls=True, )
        mail = EmailMessage(msg['Subject'], None, msg['From'], [msg['To'], ], connection=conn)
        mail.encoding = 'utf8'
        mail.attach(msg) # Attach the raw MIMEBase descendant
        mail.send()

        """
        import smtplib
        # Дополняем заголовки сообщения
        try:
            session = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
            session.set_debuglevel(1)
            session.starttls()
            session.login(self.email, self.passwd)
            session.sendmail(msg['From'], msg['To'], msg.as_string())
        finally:
            session.quit()
        """

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
        #default_permissions = []

    def get_text_msg(self, msg_type: str = 'plain'):
        """Сформировать текстовое сообщение для отправки"""
        from email.mime.text import MIMEText
        from email.header import Header
        from email.mime.image import MIMEImage
        from email.mime.multipart import MIMEMultipart
        if not self.msg:
            return
        if not msg_type in ('plain', 'html'):
            msg_type = 'plain'

        if msg_type == 'html':
            html_part = MIMEMultipart(_subtype='related')
            search_images = REGA_IMG.findall(self.msg)
            images = []
            for i, img in enumerate(search_images):
                cid = 'inline_imga_%s' % i
                self.msg = self.msg.replace(img, 'cid:%s' % cid)
                img_path = full_path(img)
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                html_img = MIMEImage(img_data)
                # angle brackets are important
                html_img.add_header('Content-Id', '<%s>' % cid)
                html_img.add_header('Content-Disposition', 'inline')
                images.append(html_img)
                #html_part.attach(html_img)

            html_text = MIMEText(self.msg, msg_type, 'utf-8')
            html_part.attach(html_text)
            for image in images:
                html_part.attach(image)
            msg = html_part
        else:
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
        #default_permissions = []

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
        """Сохранение"""
        if self.phone:
            self.phone = kill_quotes(self.phone, 'int')
        super(SMSPhone, self).save(*args, **kwargs)
