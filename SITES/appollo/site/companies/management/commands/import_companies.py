#-*- coding:utf-8 -*-
import os
import time
import logging
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import (
    open_file,
    ListDir,
    check_path,
    copy_file,
    isForD,
)
from apps.addresses.models import Address

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
        #fix_rubrics() # depricated
        #fix_phones() # depricated
        #fix_main_companies_logos() # helper
        parse_folders() # main function

        fill_main_company()

def parse_folders(root_folder: str = None):
    """Парсинг папки с рубриками
       :param root_folder: папка с рубриками
    """
    companies_folder = 'companies'
    if not root_folder:
        #root_folder = '2gis/%s' % companies_folder
        root_folder = '2gis'
    #print('parse_folders', root_folder)

    folders = ListDir(root_folder)
    for folder in folders:
        cur_folder = os.path.join(root_folder, folder)
        if not isForD(cur_folder) == 'dir':
            continue
        cur_companies_folder = os.path.join(cur_folder, companies_folder)
        if not check_path(cur_companies_folder):
            parse_companies(cur_companies_folder)
        else:
            parse_folders(cur_folder)

def parse_companies(folder: str):
    """Парсинг папки с компаниями
       :param folder: папка с компаниями
    """
    print('parse_companies', folder)
    companies_files = ListDir(folder)
    for company_file in companies_files:
        if not company_file.endswith('.json'):
            continue
        company_id = company_file.split('.json')[0]
        path = os.path.join(folder, company_file)
        with open_file(path, 'r', encoding='utf-8') as f:
            company_obj = json.loads(f.read())

        if not is8800(company_obj):
            continue
        #print(json_pretty_print(company_obj))

        company = Company.objects.select_related('main_company', 'address').filter(tag=company_id).first()

        if not company:
            company = Company.objects.create(tag=company_id)
        company_name = company_obj.get('name')
        if not company_name == company.name:
            Company.objects.filter(pk=company.id).update(name=company_name)
            company.name = company_name

        parse_ads(company_obj, company)
        parse_contact_groups(company_obj, company)
        parse_org(company_obj, company)
        #repair_company_without_tag(company) # depricated
        parse_address(company_obj, company)
        parse_rubrics(company_obj, company)


def is8800(company_obj: dict):
    """Определяем 8800 компания?"""
    contact_groups = company_obj.get('contact_groups', [])
    for contact_group in contact_groups:
        contacts = contact_group.get('contacts', {})
        for contact in contacts:
            ctype = contact.get('type')
            value = contact.get('value')
            if ctype == 'phone':
                if value.startswith('8800'):
                    return True
    return False


def parse_address(company_obj: dict, company: Company):
    """Парсинг адреса
       :param company_obj: джисонина компании
       :param company: экземеляр модели базы данных Company
    """
    # address
    address_obj = company_obj.get('address', {})
    building_id = address_obj.get('building_id')
    if not building_id:
        #print('[ERROR]: building_id absent', address_obj)
        return

    address = Address.objects.filter(tag=building_id).first()
    if not address:
        address = Address.objects.create(tag=building_id)

    # point
    point_obj = company_obj.get('point', {})
    lat = point_obj.get('lat')
    lon = point_obj.get('lon')
    Address.objects.filter(pk=address.id).update(latitude=lat, longitude=lon)

    building_name = address_obj.get('building_name')
    if building_name and not address.place == building_name:
        Address.objects.filter(pk=address.id).update(place=building_name)
    # address.components
    components = address_obj.get('components', [])
    postcode = address_obj.get('postcode')
    if postcode and not address.postalCode == postcode:
        Address.objects.filter(pk=address.id).update(postalCode=postcode)
    for component in components:
        if component['type'] == 'street_number':
            street = component['street']
            if not address.street == street:
                Address.objects.filter(pk=address.id).update(street=street)
            number = component['number']
            if not address.houseNumber == number:
                Address.objects.filter(pk=address.id).update(houseNumber=number)
        elif component['type'] == 'location':
            pass # тут только comment: Москва
        else:
            print(component, company.tag)
    # adm_div
    adm_div_obj = company_obj.get('adm_div', [])
    for adm_div in adm_div_obj:
        name = adm_div['name']
        if adm_div['type'] == 'country':
            if not address.country == name:
                Address.objects.filter(pk=address.id).update(country=name)
        elif adm_div['type'] == 'city':
            if not address.city == name:
                Address.objects.filter(pk=address.id).update(city=name)
        elif adm_div['type'] == 'district':
            if not address.district == name:
                Address.objects.filter(pk=address.id).update(district=name)
        elif adm_div['type'] == 'region':
            if not address.county == name:
                Address.objects.filter(pk=address.id).update(county=name)
        elif adm_div['type'] == 'district_area':
            if not address.subdistrict == name:
                Address.objects.filter(pk=address.id).update(subdistrict=name)
        elif adm_div['type'] == 'division':
            if not address.state == name:
                Address.objects.filter(pk=address.id).update(state=name)

    if not company.address_id == address.id:
        Company.objects.filter(pk=company.id).update(address=address)
        company.address = address

def parse_org(company_obj: dict, company: Company):
    """Парсинг компании, например,
       "org": {
         "branch_count": 64,
         "id": "4504136498282890",
         "name": "Mr.Doors, сеть мебельных салонов"
       },
       :param company_obj: джисонина компании
       :param company: экземеляр модели базы данных Company
    """
    org = company_obj.get('org', {})
    if not org:
        return
    main_company_id = org.get('id')
    if company.main_company and company.main_company.tag == main_company_id:
        return

    main_company_name = org.get('name')
    main_company = MainCompany.objects.filter(tag=main_company_id).first()
    if not main_company:
        main_company = MainCompany.objects.create(
            tag=main_company_id,
            name=main_company_name,
        )
    Company.objects.filter(pk=company.id).update(main_company=main_company)
    company.main_company = main_company

def parse_ads(company_obj: dict, company: Company):
    """Парсинг ads
       :param company_obj: джисонина компании
       :param company: экземеляр модели базы данных Company
    """
    ads = company_obj.get('ads', {})
    options = ads.get('options', {})
    buy_here = options.get('buy_here', [])
    for item in buy_here:
        logo = item.get('logo', {})
        img_url = logo.get('img_url')
        if img_url:
            imga = img_url.replace('/image.', '/image_150x150.')
            if not company.img:
                Company.objects.filter(pk=company.id).update(img=imga)
                company.img = imga

def parse_rubrics(company_obj: dict, company: Company):
    """Парсинг rubrics
       :param company_obj: джисонина компании
       :param company: экземеляр модели базы данных Company
    """
    rubrics = company_obj.get('rubrics', {})
    for rubric in rubrics:
        kind = rubric.get('primary')
        short_id = rubric.get('short_id')
        block = Blocks.objects.filter(
            tag=short_id,
            state=4,
            container__tag='catalogue',
            container__state=7,
        ).first()
        if not block:
            #print('[ERROR]: rubric %s not found' % short_id)
            continue
        analog = Company2Category.objects.filter(
            company=company,
            cat=block,
        ).first()
        if not analog:
            Company2Category.objects.create(company=company, cat=block)

def parse_contact_groups(company_obj: dict, company: Company, only8800: bool = True):
    """Парсинг контактных групп
       :param company_obj: джисонина компании
       :param company: экземеляр модели базы данных Company
       :param only8800: только 8800 компании хаваем
    """
    def parse_site(site: str):
        """Парсинг сайта - отдельная тема"""
        if 'link.2gis.ru' in site:
            site = 'http://%s' % site.split('://')[-1]
        if len(site) > MAX_VARCHAR:
            print(site, 'too long')
            return None
        return site

    mapping = {
        'phone': 'phone',
        'website': 'site',
        'email': 'email',
        'twitter': 'twitter',
        'facebook': 'facebook',
        'instagram': 'instagram',
    }
    contact_groups = company_obj.get('contact_groups', [])
    for contact_group in contact_groups:
        contacts = contact_group.get('contacts', {})
        for contact in contacts:
            ctype = contact.get('type')
            value = contact.get('value')
            if ctype in ('website', 'twitter', 'facebook', 'instagram'):
                value = parse_site(value)
            elif ctype == 'phone' and only8800:
                if not '8800' in value:
                    continue

            for key in mapping.keys():
                if ctype == key:
                    # Тут будет IndexError если не встретим нашего типа
                    contact_type = [choice[0] for choice in Contact.ctype_choices
                                    if choice[1] == mapping[key]][0]
                    contact_value = value
                    if key == 'phone':
                        contact_value = contact['text']
                    contact_row = Contact.objects.filter(
                        company=company,
                        ctype=contact_type,
                        value=contact_value,
                    ).first()
                    comment = contact.get('comment')
                    if not contact_row:
                        Contact.objects.create(
                            company=company,
                            # TODO: post-update field
                            #main_company=company.main_company,
                            ctype=contact_type,
                            value=contact_value,
                            comment=comment,
                        )
                    elif contact_row.comment != comment:
                        Contact.objects.filter(pk=contact_row.id).update(comment=comment)
                    company_value = getattr(company, mapping[key])
                    if company_value != value:
                        params = {mapping[key]: value}

                        Company.objects.filter(pk=company.id).update(**params)
                        setattr(company, mapping[key], value)


def fix_main_companies_logos():
    """Заполняем логотипы компаний из филиалов
       Тут надо понимать, что это только
       после основных прогонов будет работать,
       когда есть все привязки
    """
    for main_company in MainCompany.objects.all():
        # Копируем с филиала логотип
        main_company.drop_img()

        branch = Company.objects.filter(
            main_company=main_company,
            img__isnull=False,
        ).exclude(img='').exclude(
            img__startswith='http',
        ).first()

        if not branch:
            continue
        source = os.path.join(branch.get_folder(), branch.img)
        if check_path(source):
            print('------', branch, 'img not found')
        else:
            imga = '%s.%s' % (main_company.id, branch.img.split('.')[-1])
            dest = os.path.join(main_company.get_folder(), imga)
            copy_file(source, dest)
            MainCompany.objects.filter(pk=main_company.id).update(img=imga)

def fill_main_company():
    """Заполняем в контактах головную компанию как филиал
       Заполняем рубрики MainCompany2Category из филиалов
    """
    for contact in Contact.objects.select_related('company', 'company__main_company').filter(main_company__isnull=True):
        Contact.objects.filter(pk=contact.id).update(
            main_company=contact.company.main_company
        )
    for company in Company.objects.select_related('main_company').all():
        cats = company.company2category_set.select_related('cat').all()
        for cat in cats:
            analog = MainCompany2Category.objects.filter(
                cat=cat.cat,
                main_company=company.main_company,
            )
            if not analog:
                MainCompany2Category.objects.create(
                    cat=cat.cat,
                    main_company=company.main_company,
                )

# DEPRICATED
def fix_rubrics():
    """Задаем state=4 для блоков каталога
    """
    Blocks.objects.filter(
        container__tag='catalogue',
        container__state=7,
    ).update(state=4)

# DEPRICATED
def fix_phones():
    """При сохранении с маской телефоны зашли,
       такие надо найти и пересохранить
    """
    companies = Company.objects.filter(phone__startswith='8(')
    for company in companies:
        company.save()

# DEPRICATED
def repair_company_without_tag(company: Company):
    """Фикс на код компании,
       многие компании обновили вручную и они без кодов
       надо найти первую без кода и сдуть с нее лого,
       которое поставили вручную
    """
    company_analog = Company.objects.filter(
        tag = '',
        name = company.name,
        phone = company.phone,
        site = company.site or '',
        email = company.email or '',
        twitter = company.twitter or '',
        facebook = company.facebook or '',
        instagram = company.instagram or '',
    ).first()

    if company_analog:
        # Копируем с аналога логотип и нахер удаляем
        if company_analog.img:
            source = os.path.join(company_analog.get_folder(), company_analog.img)
            if check_path(source):
                print('------', company, company_analog, 'img not found')
                return
            imga = '%s.%s' % (company.id, company_analog.img.split('.')[-1])
            dest = os.path.join(company.get_folder(), imga)
            copy_file(source, dest)
            Company.objects.filter(pk=company.id).update(img=imga)
            print(company, 'set logo', company_analog, 'dropping')
            company_analog.delete()