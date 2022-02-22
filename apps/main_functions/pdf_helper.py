# -*- coding:utf-8 -*-
import os
from io import BytesIO
from xhtml2pdf import pisa

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template

from apps.main_functions.files import full_path, open_file

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    if uri.startswith(settings.MEDIA_ROOT):
        path = full_path(uri)
    elif uri.startswith(settings.STATIC_ROOT):
        path = os.path.join(
            settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_ROOT, '')
        )
    else:
        return uri
    if not os.path.isfile(path):
        raise Exception('media URI not found %s' % path)
    return path

def render_pdf(request,
               template: str,
               context: dict = None,
               fname: str = None,
               download: bool = False,
               page_size: str = 'letter',
               page_orientation: str = 'portrait',
               write2file: bool = False):
    """Формирует пдф
       :param request: HttpRequest
       :param template: шаблон для pdf, например, 'web/test_pdf.html'
       :param context: словарь для шаблона
       :param fname: название файла
       :param download: скачать файла (иначе показать в браузере)
       :param page_size: размер листа
       :param page_orientation: вид листа portrait/landscape
       :param write2file: записать в файл
    """
    if not context:
        context = {}
    pagesize = '%s %s' % (page_size, page_orientation)

    font = os.path.join(settings.STATIC_ROOT, 'fonts/DejaVuSans.ttf')
    font_bold = os.path.join(settings.STATIC_ROOT, 'fonts/DejaVuSans-Bold.ttf')
    font_times = os.path.join(settings.STATIC_ROOT, 'fonts/TimesNewRomanPSMT.ttf')
    font_times_bold = os.path.join(settings.STATIC_ROOT, 'fonts/TimesNewRomanPS-BoldMT.ttf')
    default_context = {
        'pagesize': pagesize,
        'page_orientation': page_orientation,
        'page_size': page_size,
        'font': font,
        'font_bold': font_bold,
        'font_times': font_times,
        'font_times_bold': font_times_bold,
    }
    context.update(default_context)

    template = get_template(template)
    html = template.render(context)

    # Сохранение в файл
    if write2file:
        dest = open_file('%s.pdf' % fname, 'wb+')
        pisa.CreatePDF(html, dest=dest)

    # Если путь со слешами
    fname = fname.replace('/', '_')

    if not download:
        result = BytesIO()
        pisaStatus = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
        response = HttpResponse(result.getvalue(),
                                content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="%s.pdf"' % fname
    else:
        response = HttpResponse(content_type='application/pdf')
        pisaStatus = pisa.CreatePDF(html, dest=response)
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % fname

    if pisaStatus.err:
        return HttpResponse('We had errors with code %s <pre>%s</pre>' % (pisaStatus.err, html))
    return response
