#-*- coding:utf-8 -*-
import time

from django.db import connection
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        """Используется для преобразования
           или оптимизации базы данных MySQL
        """
        started = time.time()
        cursor = connection.cursor()
        query = 'show tables'
        cursor.execute(query)
        rowcount = cursor.rowcount
        if rowcount > 0:
            rows = cursor.fetchall()
            for row in rows:
                query = 'alter table %s ENGINE=INNODB' % row[0]
                print(query)
                cursor.execute(query)
        print('There are %s records in database' % rowcount)
        elapsed = time.time() - started
        print('elapsed %s (%.2f min)' % (elapsed, elapsed/60))
