# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings

from apps.main_functions.files import full_path, open_file
from apps.main_functions.pdf_helper import render_pdf
from apps.main_functions.string_parser import digit_to_str, analyze_digit
from apps.main_functions.models import Standard
from apps.shop.models import Orders

from apps.site.passport.models import Passport

DATE_FORMATTER = '%d.%m.%Y'

def pdf_order(order_id,
              template_vars: dict = None,
              write2file: bool = False):
    """Формируем файл с полюсом
       :param order_id: ид заказа
       :param template_vars: переменные в шаблоне
       :param write2file: запись в файл
    """
    context = {}
    order = Orders.objects.select_related('polis', 'shopper').filter(pk=order_id).first()
    polis = Polis()
    if hasattr(order, 'polis') and order.polis:
        polis = order.polis
    shopper = order.shopper
    passport = Passport.objects.filter(shopper=shopper).last()
    main_name, main_birthday = order.shopper.name, polis.birthday
    if passport.birthday: # polis.birthday deprecated
        main_birthday = passport.birthday

    name_parts = main_name.split(' ')
    main_surname, main_first_name, main_middle_name = None, None, None
    for item in name_parts:
        if not item:
            continue
        if item and not main_surname:
            main_surname = item
            continue
        if item and not main_first_name:
            main_first_name = item
            continue
        if item and not main_middle_name:
            main_middle_name = item
            continue
    members = polis.polismember_set.select_related('passport').all()
    kop = int(str(order.total).split('.')[-1])
    context.update({
        'logo': full_path('misc/soglasie_logo.png'),
        'stamp': full_path('misc/soglasie_stamp.png'),
        'order': order,
        'polis': polis,
        'main_name': main_name,
        'main_first_name': main_first_name,
        'main_surname': main_surname,
        'main_middle_name': main_middle_name,
        'main_birthday': main_birthday,
        'shopper': shopper,
        'passport': passport,
        'number7': polis.get_number7(),
        'summa': digit_to_str(order.total),
        'ends': analyze_digit(order.total, end=('рубль', 'рублей', 'рубля')),
        'kop': '%s %s' % (digit_to_str(kop), analyze_digit(kop, end=('копейка', 'копеек', 'копейки'))),
        'members': members,
    })
    ptype = settings.FULL_SETTINGS_SET.get('REPORT_TYPE') or 'hockey'
    if ptype == 'hockey':
        context['logo'] = full_path('misc/soglasie_logo.png')
        context['stamp'] = full_path('misc/soglasie_stamp.png')
    elif ptype == 2:
        context['logo'] = full_path('misc/soglasie_logo_en.jpg')
        context['stamp'] = full_path('misc/soglasie_stamp_en.png')
        context['members'] = list(polis.polismember_set.all())
        try:
            created = datetime.date(polis.created.year, polis.created.month, polis.created.day)
            context['sdate_days'] = (polis.from_date - created).days
        except Exception as e:
            print(e)
            context['sdate'] = 1
    context['purchases'] = order.purchases_set.all()
    for purchase in context['purchases']:
        purchase.product_name = purchase.product_name.split('(')[0]
    for purchase in context['purchases']:
        if purchase.product_code and 'G' in purchase.product_code:
            context['g1'] = True
    template = 'web/order/pdf/order_%s.html' % ptype

    return render_pdf(
        template = template,
        context = context,
        download = False,
        fname = 'insurance_%s' % (
            order.id,
        ),
        write2file = write2file,
    )

class Polis(Standard):
    """Оформленный полис
    """
    polis_choices = (
        (1, 'Хоккей'),
        (2, 'Круиз'),
    )
    order = models.OneToOneField(Orders,
        blank=True, null=True, db_index=True,
        on_delete=models.SET_NULL,
        verbose_name='Ссылка на заказ')
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер полюса/заказа')
    # depricated (TODO: use shopper instead)
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='ФИО')
    # depricated (TODO: use passport instead)
    birthday = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата рождения')
    insurance_sum = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Общая страховая сумма')
    insurance_program = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Страховая программа')
    from_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Период страхования с')
    to_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Период страхования до')
    already_safe = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Уже застрахован')
    ptype = models.IntegerField(choices=polis_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Тип полюса (для формы)'
    )
    days = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Количество дней')
    class Meta:
        verbose_name = 'Страховка - Полис'
        verbose_name_plural = 'Страховка - Полисы'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Polis, self).save(*args, **kwargs)

    def send_email(self, email: str):
        """Отправка полюса по почте
           :param email: адрес куда отправляем полюс
           :return: Exception or None
        """
        if not self.id:
            return
        msg = 'Онлайн оплата прошла успешно. В приложении ваш полис.'
        host = request.META['HTTP_HOST'].encode('idna').decode('idna')
        mail = EmailMessage('%s полис' % host, msg, settings.EMAIL_HOST_USER, [email])
        mail.content_subtype = 'html'

        pdf_order(self.id,
                  write2file=True)
        fname = 'insurance_%s.pdf' % self.id
        with open_file(fname, 'rb') as f:
            mail.attach('polis%s.pdf' % self.id, f.read(), 'application/pdf')
        try:
            mail.send()
        except Exception as e:
            return e

    def get_number7(self):
        """Номер полюса по маске"""
        if not self.number:
            return ''
        if settings.FULL_SETTINGS_SET.get('REPORT_TYPE') == 'hockey':
            return self.number
        prefix = '0002114' # был, надо сменить
        if self.created and self.created > datetime.datetime(2022, 8, 31):
            prefix = '0002102'
        zfill7 = 7 - len('%s' % self.number)
        number = '%s-%s%s/22МП' % (prefix, '0' * zfill7, self.number)
        return number

class PolisMember(Standard):
    """Застрахованные к полису"""
    polis = models.ForeignKey(Polis, blank=True, null=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Имя застрахованного')
    # depricated (TODO: use passport instead)
    birthday = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата рождения застрахованного')
    # new logic for polis memeber
    passport = models.OneToOneField(Passport,
        blank=True, null=True, db_index=True,
        on_delete=models.SET_NULL,
        verbose_name='Паспорт страхуемого')
