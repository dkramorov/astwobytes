#!/usr/bin/env python3
#-*- coding:utf8 -*-
import MySQLdb
import os
import sys
import datetime
import time
import re
import shutil

class Backuper:
    """Резервное копирование данных"""
    started = None
    root_folder = '/home/jocker'.rstrip('/')
    host = 'localhost'
    user = 'root'
    passwd = ''

    mysql_conn = None
    mysql_dump_cmd = 'mysqldump -uroot'
    # Пропускать базы данных
    pass_db = ('mysql', 'performance_schema', 'information_schema', 'bis_223', 'bibil')
    post_backup_script = None # POST BACKUP SCRIPT

    # Старые папки можно удалить (дней назад) - WITH MINUS
    long_ago = -5

    def __init__(self,
                 root_folder: str = None,
                 host: str = None,
                 user: str = None,
                 passwd: str = None):
        self.started = datetime.datetime.now()
        if root_folder:
            self.root_folder = root_folder.rstrip('/')
        if host:
            self.host = host
        if user:
            self.user = user
        if passwd:
            self.passwd = passwd
        print('started: %s\nroot_folder: %s\nhost: %s\nuser: %s\npasswd: %s' % (
            self.started.strftime('%Y-%m-%d %H:%M:%S'),
            self.root_folder, self.host, self.user, self.passwd,
        ))
        self.post_backup_script = '%s/django/archive/backup_scripts/transport.sh' % self.root_folder

    def get_backup_path(self, to_folder: str = 'backup'):
        """Папка для сохранения бекапа"""
        backup_dest = '%s/%s/' % (self.root_folder, to_folder)
        if not os.path.exists(backup_dest):
            os.mkdir(backup_dest)

        backup_path_today = os.path.join(backup_dest, self.started.strftime('%Y-%m-%d'))
        if not os.path.exists(backup_path_today):
            os.mkdir(backup_path_today)

        backup_path_now = os.path.join(backup_path_today, str(self.started.hour))
        if not os.path.exists(backup_path_now):
            os.mkdir(backup_path_now)

        return backup_path_now

    def clean_old(self):
        # Названия папок бекапа
        rega_date = re.compile('^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})$')
        started = time.time()
        now = datetime.datetime.today()

        print('we started at', now)
        # RESET system clock PROTECTION
        dino = '01-01-2023'
        test_date = datetime.datetime.strptime(dino, '%d-%m-%Y')
        if now < test_date:
            print('[ERROR] System date lower than', dino)
            print('[INFO] Trying to run ntpdate...')
            os.system('ntpdate ntp.ubuntu.com')
            now = datetime.datetime.today()
            if now < test_date:
                print('[ERROR] ntpdate could not get correct date')
                exit()


        if not os.path.exists(backup_path):
            os.mkdir(backup_path)

        today_str = now.strftime('%Y-%m-%d')
        backup_path_today = os.path.join(backup_path, today_str)
        if not os.path.exists(backup_path_today):
            os.mkdir(backup_path_today)

        now_str = str(now.hour)
        backup_path_now = os.path.join(backup_path_today, now_str)
        if not os.path.exists(backup_path_now):
            os.mkdir(backup_path_now)

        # Garbage collector
        long_ago_delta = datetime.timedelta(days=long_ago)
        long_ago_date = now + long_ago_delta
        folders = os.listdir(backup_path)
        for item in folders:
            search_date = rega_date.match(item)
            if search_date > -1:
                folder_date = datetime.datetime.strptime(item, '%Y-%m-%d')
                if folder_date < long_ago_date:
                    shutil.rmtree(os.path.join(backup_path, item))
                    print("[WARNING]: Removing", backup_path, item)

    def get_databases(self):
        """Достаем названия баз данных"""
        mysql_conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd)
        cursor = mysql_conn.cursor()
        query = 'show databases'
        cursor.execute(query)
        rowcount = cursor.rowcount
        databases = []
        for i in range(rowcount):
            row = cursor.fetchone()
            db_name = row[0]
            if db_name in self.pass_db:
                continue
            databases.append(db_name)
        cursor.close()
        mysql_conn.close()
        return databases

    def local_db_backup(self):
        """Бекапим базы данных
        """
        db_folder = os.path.join(self.get_backup_path(), 'db')
        if not os.path.exists(db_folder):
            os.mkdir(db_folder)
        databases = self.get_databases()
        print('prepare backup databases: %s' % databases)
        for db_name in databases:
            cur_db_path = os.path.join(db_folder, db_name)
            os.system(self.mysql_dump_cmd + ' ' + db_name + '>' + cur_db_path + '.sql')
            os.system('tar -czf ' + cur_db_path + '.tar.gz ' + cur_db_path + '.sql')
            os.unlink(cur_db_path + '.sql')
            print('[DUMP]:', db_name)

    def backup_sites(self, folders: list = None):
        """TAR GZ /home/jocker/sites/django
        """
        if not folders:
            folders = ['django']
        backup_path = self.get_backup_path()
        for folder in folders:
            backup_src = os.path.join(self.root_folder, folder)
            archive_name = '%s.tar.gz' % folder
            os.system('cd ' + backup_path + '; tar -czf ' + archive_name + ' ' + backup_src)

    def post_backup(self, to_folder: str = 'backup'):
        """Постобработка бекапа,
           собираем все в один архив
        """
        backup_path = os.path.join(self.root_folder, to_folder)
        from_folder = self.get_backup_path()
        archive_name = '%s.tar.gz' % self.started.strftime('%Y-%m-%d')
        os.system('cd ' + backup_path + '; tar -czf ' + archive_name + ' ' + from_folder)
        #shutil.rmtree(from_folder)

        #final_archive = os.path.join(backup_path_today, today_str + '.tar.gz')
        #os.system(post_backup_script + ' ' + final_archive)

backuper = Backuper(root_folder='/Users/jocker/')
backuper.local_db_backup()
backuper.backup_sites(folders=['django', 'astwobytes'])
backuper.post_backup()


