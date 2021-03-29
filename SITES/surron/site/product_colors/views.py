# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings

from apps.main_functions.string_parser import kill_quotes
from apps.products.models import Products
from apps.site.product_colors.models import ProductColor

def get_color(request):
    """Аякс запрос по получению цвета на товар
    """
    result = {'color': '0'}
    product_id = request.GET.get('product_id')
    if not product_id.isdigit():
        return JsonResponse(result, safe=False)
    #color = request.GET.get('color')
    #if color:
    #    color = kill_quotes(color, 'int')
    product = Products.objects.filter(pk=product_id).first()
    if product:
        product_color = ProductColor.objects.filter(product=product).first()
        if product_color:
            result['color'] = product_color.color
    return JsonResponse(result, safe=False)

def set_color(request):
    """Аякс запрос по сохранению цвета на товар
    """
    result = {}
    product_id = request.GET.get('product_id')
    if not product_id.isdigit():
        return JsonResponse(result, safe=False)
    color = request.GET.get('color')
    if color:
        color = kill_quotes(color, 'int')
    if not color:
        color = 0
    product = Products.objects.filter(pk=product_id).first()
    if product:
        if request.user.has_perm('products.change_products'):
            product_color = ProductColor.objects.filter(product=product).first()
            if product_color:
                product_color.color = color
            else:
                product_color = ProductColor(product=product)
            product_color.save()
            result['success'] = 'Основной цвет сохранен'
        else:
            result['error'] = 'Недостаточно прав'
    else:
        result['error'] = 'Товар не найден'
    return JsonResponse(result, safe=False)
