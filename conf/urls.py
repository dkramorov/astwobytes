from django.conf import settings
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.conf.urls import url


urlpatterns = [
    re_path(r'^admin/', include('apps.login.urls')),
    path('auth/', lambda request: redirect('/admin/', permanent=False)),
    # Стат. странички
    re_path(r'^flatcontent/', include('apps.flatcontent.urls')),
    # Файлы
    re_path(r'^files/', include('apps.files.urls')),
    # main_functions
    re_path(r'^', include('apps.main_functions.urls')),
    # статика
    re_path(r'^', include('apps.files.urls_static'))
]

# ---------------------------------
# Подключение приложений через .env
# ---------------------------------
if 'apps.site' in settings.INSTALLED_APPS:
    # Сайт
    urlpatterns.insert(1, re_path(r'^', include('apps.site.main.urls')))
# ---------------------------
# Подключаем custom site apps
# ---------------------------
for app in settings.INSTALLED_APPS:
    if app.startswith('apps.site.'):
        prefix = app.split('.')[-1]
        urlpatterns.insert(1, re_path(r'^%s/' % prefix, include('%s.urls' % app)))

if 'apps.afisha' in settings.INSTALLED_APPS:
    # Афиша
    urlpatterns += [
        re_path(r'^afisha/', include('apps.afisha.urls')),
    ]
if 'apps.spamcha' in settings.INSTALLED_APPS:
    from apps.spamcha.views import srdr_goto
    # Рассылки
    urlpatterns += [
        re_path(r'^spamcha/', include('apps.spamcha.urls')),
        # -----------------------------
        # /srdr/goto/.../ Переадресация
        # -----------------------------
        url('^srdr/goto/(?P<our_link>.+)/$', srdr_goto, name='srdr_goto'),
    ]
if 'apps.ws' in settings.INSTALLED_APPS:
    # websocket (chat)
    urlpatterns += [
        re_path(r'^ws/', include('apps.ws.urls')),
    ]
if 'apps.binary_com' in settings.INSTALLED_APPS:
    # binary.com
    urlpatterns += [
        re_path(r'^binary_com/', include('apps.binary_com.urls')),
    ]
if 'apps.languages' in settings.INSTALLED_APPS:
    # Переводы
    urlpatterns += [
        re_path(r'^languages/', include('apps.languages.urls')),
    ]
if 'apps.freeswitch' in settings.INSTALLED_APPS:
    # FREESWITCH
    urlpatterns += [
        re_path(r'^freeswitch/', include('apps.freeswitch.urls')),
    ]
if 'apps.demonology' in settings.INSTALLED_APPS:
    # Создание демонов
    urlpatterns += [
        re_path(r'^demonology/', include('apps.demonology.urls')),
    ]
if 'apps.products' in settings.INSTALLED_APPS:
    # Товары/услуги
    urlpatterns += [
        re_path(r'^products/', include('apps.products.urls')),
    ]
if 'apps.promotion' in settings.INSTALLED_APPS:
    # Продвижение и сео
    urlpatterns += [
        re_path(r'^promotion/', include('apps.promotion.urls')),
    ]
if 'apps.personal' in settings.INSTALLED_APPS:
    # Пользователи сайта
    urlpatterns += [
        re_path(r'^personal/', include('apps.personal.urls')),
    ]
if 'apps.yandex' in settings.INSTALLED_APPS:
    # Яндекс сервисы
    urlpatterns += [
        re_path(r'^yandex/', include('apps.yandex.urls')),
    ]
if 'apps.shop' in settings.INSTALLED_APPS:
    # Магазин
    urlpatterns += [
        re_path(r'^shop/', include('apps.shop.urls')),
    ]
if 'apps.weld' in settings.INSTALLED_APPS:
    # Модуль сварки стыков
    urlpatterns += [
        re_path(r'^weld/', include('apps.weld.urls')),
    ]
if 'apps.addresses' in settings.INSTALLED_APPS:
    # Адреса объектов
    urlpatterns += [
        re_path(r'^addresses/', include('apps.addresses.urls')),
    ]
if 'apps.contractors' in settings.INSTALLED_APPS:
    # Контрагенты
    urlpatterns += [
        re_path(r'^contractors/', include('apps.contractors.urls')),
    ]
if 'apps.jabber' in settings.INSTALLED_APPS:
    # Jabber XMPP
    urlpatterns += [
        re_path(r'^jabber/', include('apps.jabber.urls')),
    ]
if 'djapian' in settings.INSTALLED_APPS:
    # DJAPIAN SEARCH
    from djapian.utils import load_indexes
    load_indexes()

# -------------------------------------------
# Обработка статических файлов под DEBUG=True
# -------------------------------------------
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# --------------
# Стат странички
# --------------
urlpatterns += [
    re_path(r'^', include('apps.flatcontent.urls_static')),
]
