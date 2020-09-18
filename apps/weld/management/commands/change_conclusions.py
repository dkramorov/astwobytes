# -*- coding: utf-8 -*-
import logging
import re

from openpyxl import load_workbook
from io import BytesIO

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.weld.models import WeldingJoint
from apps.weld.conclusion_model import JointConclusion

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Заключения будем создавать разные на заявку
       ?блокировка редактирования у заключения на данный момент отсутствует,
       возможно, добавить проверку по ключам repair,
       и давать редактировать только последнее заключение

       1) все PDF кнопки при редактировании заключения
       перенесены под соответствующие разделы заключений

       2) В таблицах заявок на стыки выведены примечания к дефектам по РК контролю
          - TODO можно вывести примечание к другим заключениям

       3) Перенести текущее положение заключений на новую схему,
          где мы можем создавать несколько заключений на одну заявку

       4) При ремонте создается новое заключение, текущее остается
       5) В таблице заключений будут выведены заключения по ремонту,
          наряду с готовыми заключениями по той же заявке на стык

       6) В формах pdf заключений изменена нумерация заключения,
          номер стыка перемещен в начало номера, добавлен номер ремонта

       основное (первое заключение) всегда должно иметь repair=None

       Когда нажимаем отправить в ремонт, то
       1) создаем новое заключение на заявку c repair=1
          (увеличиваем согласно номеру ремонта по заявке)
       2) выводим в заявке ссылки на оба заключения
       3) в заключениях принадлежащих заявке даем возможность перейти каждое из них

       Необходимо выполнить операцию по созданию заключений на ремонты

       пока оставляем заполнение нового заключения по ремонту полностью вручную,
       то есть, пока не переносим дефекты
    """
    def handle(self, *args, **options):
        #for conclusion in JointConclusion.objects.all():
        #    conclusion.delete()

        return
        for welding_joint in WeldingJoint.objects.filter(repair__gte=1):
            repair = welding_joint.repair
            conclusions = JointConclusion.objects.filter(welding_joint=welding_joint)
            ids_conclusions = {}
            for conclusion in conclusions:
                conclusion_repair = conclusion.repair or 0
                ids_conclusions[conclusion_repair] = conclusion
            for i in range(repair + 1):
                if not i in ids_conclusions:
                    JointConclusion.objects.create(welding_joint=welding_joint, repair=i)
                    print('new conclusion repair %s for welding_joint %s' % (i, welding_joint.request_number))


