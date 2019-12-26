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
    # Афиша
    re_path(r'^afisha/', include('apps.afisha.urls')),
    # Стат. странички
    re_path(r'^flatcontent/', include('apps.flatcontent.urls')),
    # Файлы
    re_path(r'^files/', include('apps.files.urls')),
    # Рассылки
    re_path(r'^spamcha/', include('apps.spamcha.urls')),
    # binary.com
    re_path(r'^binary_com/', include('apps.binary_com.urls')),
    # websocket
    re_path(r'^ws/', include('apps.ws.urls')),
    # статика
    re_path(r'^', include('apps.files.urls_static'))
]

# Обработка статических файлов под DEBUG=True
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

