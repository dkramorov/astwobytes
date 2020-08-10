# -*- coding:utf-8 -*-
import os
import json

from xhtml2pdf import pisa

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.template.loader import get_template

from apps.main_functions.files import full_path


CUR_APP = 'main'

def home(request):
    """Главная страничка сайта"""
    return redirect('/auth/')

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

def test_pdf(request):
    template_path = 'web/test_pdf.html'

    page_size = request.POST.get('page_size', 'letter')
    page_orientation = request.POST.get('page_orientation', 'portrait')
    pagesize = '%s %s' % (page_size, page_orientation)

    context = {
        'pagesize': pagesize,
        'page_orientation': page_orientation,
        'page_size': page_size,
        'example_number': request.POST.get("example_number", '1'),
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="test_pdf.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    if request.POST.get('show_html', ''):
        response['Content-Type'] = 'application/text'
        response['Content-Disposition'] = 'attachment; filename="test_pdf.txt"'
        response.write(html)
    else:
        pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        if pisaStatus.err:
            return HttpResponse('We had some errors with code %s <pre>%s</pre>' % (pisaStatus.err, html))
    return response
