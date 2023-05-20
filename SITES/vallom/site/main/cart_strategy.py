from django.db import connections

from apps.main_functions.db_helper import DBAbstract
from apps.shop.cart import calc_cart, get_shopper
from apps.shop.models import Purchases
from apps.products.models import Products


class CRMProducts(DBAbstract):
    table = 'products'
    fields = (
        'id', 'name', 'quantity', 'price_total',
    )

def check_cart(request):
    """Проверка корзинки на наличие товаров"""
    CRM_DB = 'vallomcrm'
    shopper = get_shopper(request)
    cart = calc_cart(shopper, min_info=False)
    ids_product = []
    for purchase in cart.get('purchases', {}):
        ids_product.append(purchase.product_id)

    if not ids_product:
        return {}

    crm_products = CRMProducts()
    with connections[CRM_DB].cursor() as cursor:
        where = 'id IN (%s)' % ','.join(['"%s"' % product_id for product_id in ids_product])
        query = crm_products.get_query(table=crm_products.table, fields=crm_products.fields, where=where, limit=999)
        cursor.execute(query)
        rows = cursor.fetchall()
        products = crm_products.rows2dict(fields=crm_products.fields, rows=rows)
    fordel = []
    modify = []
    for purchase in cart.get('purchases', {}):
        if purchase.product_id in products:
            if products[purchase.product_id]['quantity'] <= 0:
                fordel.append(purchase)
                # Удаляем из корзинки
                Purchases.objects.filter(pk=purchase.id).delete()

            elif products[purchase.product_id]['quantity'] < purchase.count:
                modify.append(purchase)
                # Меняем кол-во
                Purchases.objects.filter(pk=purchase.id).update(count=products[purchase.product_id]['quantity'])

    if fordel:
        Products.objects.filter(pk__in=[item.product_id for item in fordel]).update(count=0)
    return {'fordel': fordel, 'modify': modify}


