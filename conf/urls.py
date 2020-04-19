"""ADMIN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# -----------------------------------------------------------
# re_path USAGE:
# re_path(r'^index/$', views.index, name='index'),
# re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
# re_path(r'^weblog/', include('blog.urls')),
# -----------------------------------------------------------
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
    # Сайт
    re_path(r'^', include('apps.site.main.urls')),
    # статика
    re_path(r'^', include('apps.files.urls_static'))
]

# ---------------------------------
# Подключение приложений через .env
# ---------------------------------
if 'apps.afisha' in settings.INSTALLED_APPS:
    # Афиша
    urlpatterns += [
        re_path(r'^afisha/', include('apps.afisha.urls')),
    ]
if 'apps.spamcha' in settings.INSTALLED_APPS:
    # Рассылки
    urlpatterns += [
        re_path(r'^spamcha/', include('apps.spamcha.urls')),
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
        re_path(r'^', include('apps.languages.urls')),
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
if 'apps.flattooltip' in settings.INSTALLED_APPS:
    # Подсказки для изображений
    urlpatterns += [
        re_path(r'^flattooltip/', include('apps.flattooltip.urls')),
    ]

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
