"""
Django settings for project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# -----------------------
# Проверить все настройки
# -----------------------
# $ python manage.py diffsettings --all

import os
from envparse import env

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

env.read_envfile()

# ------------------
# Мультиязычный сайт
# ------------------
IS_DOMAINS = False
MAIN_DOMAIN = env('MAIN_DOMAIN')
DOMAINS = [] # Можно из базы дополнить
# В env можно положить список поддоменов через запятую,
# например, SUBDOMAINS = "rus:Русская версия,eng:Английская версия"
SUBDOMAINS = env('SUBDOMAINS', default='')
if MAIN_DOMAIN and SUBDOMAINS:
    DOMAINS = [
        {'pk': None, 'domain': MAIN_DOMAIN, 'name': 'Основной сайт'},
        {'pk': None, 'domain': 'rus.%s' % (MAIN_DOMAIN, ), 'name': 'Основной сайт'},
    ]
    sub_domains = []
    for i, item in enumerate(SUBDOMAINS.split(',')):
        sub_domain, name = item.split(':')
        sub_domains.append({
            'pk': i,
            'domain': '%s.%s' % (sub_domain.strip(), MAIN_DOMAIN),
            'name': name.strip(),
        })
    DOMAINS += sub_domains
    #print('[DOMAINS]: %s' % (DOMAINS, ))
    IS_DOMAINS = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=3+k48o8@y*j1@sd(@_se4-@o7%l1id-=r7-iv#nbi!h2ho+^8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', cast=bool, default=True)
TEMPLATE_DEBUG = env('TEMPLATE_DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = [
    '*',
    #'.example.com',  # Allow domain and subdomains
    #'.example.com.',  # Also allow FQDN and subdomains
]

# main_functions.tasks create_new_app
# CUSTOM_APPS_START
CUSTOM_APPS = [
]
# CUSTOM_APPS_END

# Сайт
if env('SITE_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.site')

if env('AFISHA_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.afisha')
if env('SPAMCHA_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.spamcha')
if env('WS_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.ws')
if env('BINARY_COM_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.binary_com')
if env('LANGUAGES_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.languages')
if env('FREESWITCH_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.freeswitch')
if env('DEMONOLOGY_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.demonology')
if env('PRODUCTS_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.products')
if env('FLATTOOLTIP_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.flattooltip')
if env('PROMOTION_APP', cast=bool, default=False):
    CUSTOM_APPS.append('apps.promotion')

CUSTOM_APPS += [
    'apps.upload_tasks',
]
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000
# Email settings
EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')

# Application definition
INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.messages',
    #'django.contrib.staticfiles', # => STATICFILES_DIRS
    'apps.main_functions',
    'apps.login',
    'apps.telegram',
    'apps.files',
    'apps.flatcontent',
] + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# mysql с autoreload.py вызывает иногда embedded null byte error
# mysqlclient==1.4... вызывал проблему
# mysqlclient==1.3.13 решил проблему
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'conf', 'my.cnf'),
            'sql_mode': 'traditional',
        },
        #'NAME': 'astwobytes',
        #'USER': 'root',
        #'PASSWORD': '',
        #'HOST': 'localhost',
        #'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = env('TIME_ZONE', default='Asia/Irkutsk')
USE_TZ = env('USE_TZ', cast=bool, default=False)

USE_I18N = False
USE_L10N = False

LOGIN_REDIRECT_URL = '/admin/login/welcome/'
LOGIN_URL = '/admin/login/'

AUTHENTICATION_BACKENDS = (
    'apps.login.backend.MyBackend',
    #'django.contrib.auth.backends.ModelBackend',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [
    STATIC_ROOT,
]

LOG_LEVEL = env('LOG_LEVEL', default='INFO')

def skip_static_requests(record):
    """Фильтр для запросов на статику"""
    if record.args[0].startswith('GET /static/') or record.args[0].startswith('GET /media/'):
        return False
    return True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': env('DISABLE_EXISTING_LOGGERS', cast=bool, default=True),
    'filters': {
        'skip_static_requests': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_static_requests,
        }
    },
    'formatters': {
        'simple': {
            'format': '\t'.join((
                '%(asctime)s',
                '%(levelname)s',
                #'%(pathname)s:%(lineno)s',
                '%(message)s',
            )),
        },
    },
    'handlers': {
        'debug_console': {
            'level': LOG_LEVEL,
            'filters': ['skip_static_requests'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console'],
    },
    'loggers': {
        'django.server': {
            'level': LOG_LEVEL,
            'handlers': ['debug_console'],
            'propagate': False,
        },
        'main': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'requests': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# -----------------------
# Настройки телеграм-бота
# -----------------------
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN', default='')
TELEGRAM_PROXY = env('TELEGRAM_PROXY', default='')
TELEGRAM_CHAT_ID = env('TELEGRAM_CHAT_ID', default=0)
TELEGRAM_ENABLED = env('TELEGRAM_ENABLED', cast=bool, default=False)

# --------------
# Websocket chat
# --------------
WS_CHAT = env('WS_CHAT', cast=bool, default=True)
WS_SERVER = env('WS_SERVER', default='ws://127.0.0.1:8888/')
WS_SECRET = env('WS_SECRET', default='bugogashenki')

# -------------------
# Freeswitch settings
# -------------------
FREESWITCH_DOMAIN = env('FREESWITCH_DOMAIN', default='')
FREESWITCH_URI = env('FREESWITCH_URI', default='')
FREESWITCH_WSS = env('FREESWITCH_WSS', default='')

# ------
# CRM DB
# ------
CRM_HOST = env('CRM_HOST', default='')

SENTRY_DSN = env('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# ----------------------------
# Внешнее хранилище для файлов
# ----------------------------
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', default='')
AWS_ACL_POLICY = "public-read"
BOTO_S3_BUCKET = env.str('BOTO_S3_BUCKET', default='my_bucket')
BOTO_S3_HOST = env.str('BOTO_S3_HOST', default='hb.bizmrg.com')
AWS_S3_FORCE_HTTP_URL = False
# с этим не все пашет
#BOTO_BUCKET_LOCATION = env.str('BOTO_BUCKET_LOCATION', default='RU')
