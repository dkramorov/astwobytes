#################################################
# Локально
#################################################
$ virtualenv -p python3 env
$ source env/bin/activate
$ python -m django --version
$ django-admin startproject test_site
$ python test_site/manage.py runserver

#################################################
# На хостинге:
#################################################
$ python3 -m pip # скажет /usr/bin/python3: No module named pip
$ wget https://bootstrap.pypa.io/get-pip.py
$ python3 get-pip.py --user # установит все в хомяка
$ python3 -m pip # скажет, что все ок - выдаст команды пипки
$ python3 -m pip install --user -r requirements.txt # все зайдет как по маслу

или просто $ python3 -m pip install --user requests



В связи с ограничениями почтовых функций Вашего аккаунта (обращение 3466206), изменения вносимые в панели управления в задачи cron не применяются, но сами задачи выполняются.
Вы можете внести изменения вручную. Для этого необходимо подключится по ssh https://timeweb.com/ru/help/pages/viewpage.action?pageId=4358354

Просмотр задач
crontab -l
Редактировать задачу
crontab -e

Подробнее про cron можно прочитать по ссылке:
https://timeweb.com/ru/help/pages/viewpage.action?pageId=4358482






# --------------
# Файл .htaccess
# --------------
Options +ExecCGI
RewriteEngine On
AddHandler wsgi-script .wsgi
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ /index\.wsgi/$1 [QSA,PT,L]

# ---------------
# Файл indes.wsgi
# ---------------
import os, sys
path = "/home/a/a223223/test_site/public_html"
# -------------------------------
# append project.path to sys.path
# -------------------------------
if not path in sys.path:
  sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = "test_site.settings"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# ---------------------------------
# Далее необходимо включить логи,
# потому что все дальнейшие препоны
# были исключены по логам, также я
# вынес проект в корень, то есть,
# manage.py должно быть там же,
# где лежит .htaccess, index.wsgi
# ---------------------------------

#################################################
# В settings.py
#################################################
import django
# -------------------
# ... и в самом конце
# -------------------
django.setup()

# ---------------------------------
# SECRET_KEY может быть чем угодно,
# можно запустить скрипт
# python3 generate_secret.py
# ---------------------------------

# -------------------------------------------
# Будет ошибка,
# Invalid HTTP_HOST header: 'test.3deda.com'.
# You may need to add 'test.3deda.com'
# to ALLOWED_HOSTS.
# В settings.py вписываем
# ALLOWED_HOSTS = ["test.3deda.com", ]
# После этого запашет индексная страничка
# -------------------------------------------

# -----------------------------------------------
# PS: Если параллельно стоит на хостинге и django
# на python2 и ставим django на python3,
# тогда следует все-таки сходить в ./local
# например, /home/a/a223223/.local/lib/python2.7/site-packages
# там будет Django, django - надо их похерить и
# положить нужную версию django в проект,
# та же логика касается и разных версий django
# -----------------------------------------------


