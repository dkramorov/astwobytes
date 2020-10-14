import datetime

from django.test import TestCase
from django.urls import reverse

from apps.main_functions.date_time import date_plus_days
from apps.spamcha.models import SMSPhone
from apps.spamcha.sms_helper import get_sms_volume

class SmsPhonesTests(TestCase):
    """Тестирование телефонов для отправки смс"""
    def test_clear_sent(self):
        """Тестирование сброса счетчика отправленных сообщений
           если дата у нас не совпала с той, когда телефон обновлен,
           тогда сбрасываем счетчик отправленных сообщений
        """
        today = datetime.datetime.today()
        new_phone = SMSPhone.objects.create()
        phone_updated = new_phone.updated.strftime('%Y-%m-%d')
        self.assertEqual(phone_updated, today.strftime('%Y-%m-%d'))
        self.assertEqual(new_phone.sent, 0)

        yesterday = date_plus_days(today, days=-1)
        SMSPhone.objects.filter(pk=new_phone.id).update(
            updated=yesterday,
            sent=500,
        )
        phone = SMSPhone.objects.filter(pk=new_phone.id).first()
        self.assertEqual(phone.updated, yesterday)
        self.assertEqual(phone.sent, 500)
        phone.save()
        self.assertEqual(phone.sent, 0)

    def test_sms_volume(self):
        """Тестирование правильного подсчета кол-ва смсок
           по объему текста
        """
        one_sms_len = 65
        self.assertEqual(get_sms_volume('a' * one_sms_len), 1)
        self.assertEqual(get_sms_volume(None), 0)
        self.assertEqual(get_sms_volume('a' * one_sms_len * 2), 2)
        self.assertEqual(get_sms_volume('a' * one_sms_len * 3), 3)
        self.assertEqual(get_sms_volume('abc' * one_sms_len), 3)



