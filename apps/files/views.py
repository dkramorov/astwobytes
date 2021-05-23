# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.files import check_path, full_path, file_size
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from apps.files.models import Files
from apps.files.sitemap import SitemapXML, SitemapHTML

if settings.IS_DOMAINS:
    from apps.languages.models import get_domain, get_domains

CUR_APP = 'files'
files_vars = {
    'singular_obj': 'Файл',
    'plural_obj': 'Файлы',
    'rp_singular_obj': 'файла',
    'rp_plural_obj': 'файлов',
    'template_prefix': 'files_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'files',
    'submenu': 'files',
    'show_urla': 'show_files',
    'create_urla': 'create_file',
    'edit_urla': 'edit_file',
    'model': Files,
}

def api(request, action: str = 'files'):
    """Апи-метод для получения всех данных"""
    #if action == 'files':
    #    result = ApiHelper(request, files_vars, CUR_APP)
    result = ApiHelper(request, files_vars, CUR_APP)
    return result

@login_required
def show_files(request, *args, **kwargs):
    """Вывод файлов"""
    return show_view(request,
                     model_vars = files_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_file(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование файла"""
    mh_vars = files_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    row = mh.get_row(row_id)
    context = mh.context
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))

    if request.method == 'GET':
        if action == 'create':
            mh.breadcrumbs_add({
                'link': mh.url_create,
                'name': '%s %s' % (mh.action_create, mh.rp_singular_obj),
            })
        elif action == 'edit' and row:
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
            })
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'

    elif request.method == 'POST':
        pass_fields = ('path', 'mime')
        mh.files_add('path')
        mh.post_vars(pass_fields=pass_fields)

        if action == 'create' or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
        # -------------------------------------------
        # Нужно обновить ссылку на файл, если ее нету
        # Если есть файл, нужно обновить mimetype
        # -------------------------------------------
        elif action == 'img' and request.FILES:
            mh.uploads()
            mh.row.update_mimetype()

    if mh.row:
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.get_url_edit()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def files_positions(request, *args, **kwargs):
    """Изменение позиций файлов"""
    result = {}
    mh_vars = files_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def ReturnFile(request, link):
    """Возвращаем файл"""
    if not link.startswith('/'):
        link = '/%s' % link
    # Заебал этот фавикон, думаю,
    # одна проверка на него не напряжет
    if link == '/favicon.ico':
        path = '%s/img/favicon.ico' % settings.STATIC_ROOT.rstrip('/')
        with open(path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/x-icon')
        response['Content-Length'] = file_size(path)
        response['Content-Disposition'] = 'inline; filename=%s' % (path, )
        return response
    elif link == '/sitemap.xml':
        context = {}
        sitemap = SitemapXML()
        context['managers'] = sitemap.get_menu_managers()
        template = 'sitemap_index.html'
        return render(request, template, context,
                      content_type='text/xml')
    elif link.startswith('/sitemap/'):
        context = {}
        sitemap = SitemapXML()
        context['blocks'] = sitemap.get_manager(link)
        template = 'sitemap_xml.html'
        return render(request, template, context,
                      content_type='text/xml')

    search_files = Files.objects.filter(link=link, is_active=True)
    # Если мультидомен,
    # то ищем в том числе специфический для домена файл,
    # но если нету, то возвращаем без домена
    if settings.IS_DOMAINS:
        domain = get_domain(request)
        search_file_with_domain = search_files.filter(domain=domain['pk']).values_list('id', flat=True)
        if search_file_with_domain:
            search_files = search_files.filter(domain=domain['pk'])

    search_file = search_files.first()
    if search_file:
        path = '%s%s' % (search_file.get_folder(), search_file.path)
        if not check_path(path):
            with open(full_path(path), 'rb') as f:
                response = HttpResponse(f.read(), content_type=search_file.mime)
            response['Content-Length'] = file_size(path)
            response['Content-Disposition'] = 'inline; filename=%s' % (path, )
            return response
        else: # файл не найден - лучше 404 отдать
            raise Http404
    return redirect("/")

def show_sitemap(request):
    """Страничка карты сайта HTML"""
    return SitemapHTML().show_sitemap(request)
