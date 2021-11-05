#-*- coding:utf-8 -*-
import os
import time
import logging
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.files import make_folder, drop_folder, open_file
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file, ListDir, check_path, copy_file
from apps.main_functions.functions import object_fields
from apps.addresses.models import Address

from djapian.forindex import hershin

from apps.site.companies.models import (
    Company,
    MainCompany,
    Contact,
    Company2Category,
    MainCompany2Category,
)

logger = logging.getLogger(__name__)

default_folder = settings.MEDIA_ROOT
MAX_VARCHAR = 250
by = 250

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--demo_mode',
            action = 'store_true',
            dest = 'demo_mode',
            default = False,
            help = 'Set demo mode')
        parser.add_argument('--cat_id',
            action = 'store',
            dest = 'cat_id',
            type = str,
            default = False,
            help = 'Set cat tag for update')

    def handle(self, *args, **options):
        started = time.time()
        app_json_folder = 'app_json'

        version = 1
        version_file = os.path.join(app_json_folder, 'version.json')
        if not check_path(version_file):
            with open_file(version_file, 'r', encoding='utf-8') as f:
                version = int(json.loads(f.read())['version'])

        drop_folder(app_json_folder)
        make_folder(app_json_folder)

        json_file = os.path.join(app_json_folder, 'companies_db_helper.json')

        json_obj = {}
        fill_catalogue(json_obj)
        fill_addresses(json_obj)
        fill_orgs(json_obj)
        fill_branches(json_obj)
        fill_contacts(json_obj)

        with open_file(json_file, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(json_obj))
        with open_file(version_file, 'w+', encoding='utf-8') as f:
            f.write(json.dumps({
                'version': version + 1
            }))

        #fp = full_path(app_folder)
        #tar = search_binary('tar')
        #os.system('%s -czf %s/app4.tar.gz -C %s .' % (tar, settings.MEDIA_ROOT, fp))

def fill_contacts(json_obj: dict):
    """Заполнение контактов
       :param json_obj: результирующая джисонина
    """
    json_obj['phones'] = []
    query = Contact.objects.select_related('company').filter(ctype=1)
    total_records = query.aggregate(Count('id'))['id__count']
    total_pages = int(total_records / by) + 1

    for i in range(total_pages):
        rows = query[i*by:i*by+by]
        for phone in rows:
            search_terms = []
            hershin(phone.value, search_terms)
            hershin(phone.indexed_value, search_terms)
            search_terms = ' '.join(search_terms)

            obj = {
                'id': phone.id,
                'client': phone.company.main_company_id,
                'branch': phone.company.id,
                'prefix': '',
                'number': phone.value,
                'digits': phone.indexed_value,
                'whata': '',
                'comment': phone.comment,
                'position': phone.position,
                'search_terms': search_terms,
            }
            #print(obj)
            json_obj['phones'].append(obj)


def fill_branches(json_obj: dict):
    """Заполнение филиалов
       :param json_obj: результирующая джисонина
    """
    json_obj['branches'] = []
    query = Company.objects.all()
    total_records = query.aggregate(Count('id'))['id__count']
    total_pages = int(total_records / by) + 1

    for i in range(total_pages):
        rows = query[i*by:i*by+by]
        for branch in rows:
            search_terms = []
            hershin(branch.name, search_terms)
            search_terms = ' '.join(search_terms)

            obj = {
                'id': branch.id,
                'client': branch.main_company_id,
                'name': branch.name,
                'address': branch.address_id,
                'site': branch.site,
                'email': branch.email,
                'wtime': '',
                'position': branch.position,
                'search_terms': search_terms,
            }
            json_obj['branches'].append(obj)

def fill_orgs(json_obj: dict):
    """Заполнение компаний
       :param json_obj: результирующая джисонина
    """
    json_obj['orgs'] = []
    json_obj['cats'] = []
    json_obj['cat_contpos'] = []
    query = MainCompany.objects.all()
    total_records = query.aggregate(Count('id'))['id__count']
    total_pages = int(total_records / by) + 1

    for i in range(total_pages):
        rows = query[i*by:i*by+by]
        ids_orgs = [org.id for org in rows]
        orgs_branches = Company.objects.filter(main_company__in=ids_orgs).values('main_company').annotate(pcount=Count('main_company'))
        branches_count = {org['main_company']: org['pcount'] for org in orgs_branches}

        orgs_phones = Contact.objects.filter(
            company__main_company__in=ids_orgs,
            ctype=1,
        ).values('company__main_company').annotate(pcount=Count('company__main_company'))
        phones_count = {org['company__main_company']:org['pcount'] for org in orgs_phones}

        for org in rows:
            if not org.id in branches_count and not org.id in phones_count:
                logger.info("[INFO]: NO BRANCHES, NO PHONES, org %s" % org.id)
                continue
            search_terms = []
            hershin(org.id, search_terms)
            hershin(org.name, search_terms)
            search_terms = ' '.join(search_terms)

            logo = None
            if org.img and not org.img.startswith('http'):
                logo = os.path.join(org.get_folder(), org.img)

            obj = {
                'id': org.id,
                'name': org.name,
                'logo': logo,
                'resume': org.resume,
                'branches': branches_count.get(org.id),
                'phones': phones_count.get(org.id),
                'search_terms': search_terms,
            }
            json_obj['orgs'].append(obj)

            links = MainCompany2Category.objects.filter(main_company=org)
            for link in links:
                json_obj['cats'].append({
                    'id': link.id,
                    'cat_id': link.cat_id,
                    'client_id': link.main_company_id,
                })


def fill_addresses(json_obj: dict):
    """Заполнение адресов
       :param json_obj: результирующая джисонина
    """
    json_obj['addresses'] = []
    query = Address.objects.all()
    total_records = query.aggregate(Count('id'))['id__count']
    total_pages = int(total_records / by) + 1

    for i in range(total_pages):
        rows = query[i*by:i*by+by]

        ids_addresses = [adr.id for adr in rows]
        addresses_branches = Company.objects.filter(address__in=ids_addresses).values('address').annotate(pcount=Count('address'))
        addresses_count = {adr['address']: adr['pcount'] for adr in addresses_branches}

        for address in rows:
            if not address.id in addresses_count:
                logger.info('[INFO]: empty address %s' % address.id)
                continue
            search_terms = []
            hershin(address.postalCode, search_terms)
            hershin(address.country, search_terms)
            hershin(address.state, search_terms)
            hershin(address.county, search_terms)
            hershin(address.city, search_terms)
            hershin(address.district, search_terms)
            hershin(address.subdistrict, search_terms)
            hershin(address.street, search_terms)
            hershin(address.houseNumber, search_terms)
            hershin(address.addressLines, search_terms)
            hershin(address.additionalData, search_terms)
            hershin(address.place, search_terms)
            search_terms = ' '.join(search_terms)

            obj = {
                'id': address.id,
                'postalCode': address.postalCode,
                'country': address.country,
                'state': address.state,
                'county': address.county,
                'city': address.city,
                'district': address.district,
                'subdistrict': address.subdistrict,
                'street': address.street,
                'houseNumber': address.houseNumber,
                'addressLines': address.addressLines,
                'additionalData': address.additionalData,
                'latitude': '%s' % address.latitude,
                'longitude': '%s' % address.longitude,
                'place': address.place,
                'branches_count': addresses_count[address.id],
                'search_terms': search_terms,
            }
            json_obj['addresses'].append(obj)


def fill_catalogue(json_obj: dict):
    """Заполнение каталога
       :param json_obj: результирующая джисонина
    """
    json_obj['catalogue'] = []
    catalogue = Containers.objects.filter(state=7, tag='catalogue').first()
    if not catalogue:
        logger.info('[ERROR]: catalogue not found')
        return
    query = catalogue.blocks_set.all()
    total_records = query.aggregate(Count('id'))['id__count']
    total_pages = int(total_records / by) + 1
    for i in range(total_pages):
        rows = query[i*by:i*by+by]

        ids_cats = [cat.id for cat in rows]
        orgs_cats = Company2Category.objects.filter(cat__in=ids_cats).values('cat').annotate(pcount=Count('company'))
        orgs_count = {cat['cat']: cat['pcount'] for cat in orgs_cats}
        for cat in rows:
            if not cat.id in orgs_count:
                #logger.info('[INFO]: empty cat %s' % cat.id)
                continue

            search_terms = []
            hershin(cat.name, search_terms)

            search_terms = ' '.join(search_terms)
            obj = {
                'id': cat.id,
                'name': cat.name,
                'count': orgs_count[cat.id],
                'search_terms': search_terms,
            }
            #print(json_pretty_print(obj))
            json_obj['catalogue'].append(obj)
