import xml.etree.ElementTree as ET
from django.db.models import Q

def parse_query(query: str = None):
    """Парсинг строки в xml формат
       :param query: запрос строкой, например,
                     distance=1 AND enabed=true OR (distance=2 AND enabled=false)
    """
    xml_query = ''
    query = query.replace('(', ' ( ').replace(')', ' ) ')
    query_arr = query.split()
    # print(query_arr)
    for item in query_arr:
        item = item.strip()
        if item.upper() == 'AND':
            xml_query += '<and />'
        elif item.upper() == 'OR':
            xml_query += '<or />'
        elif item == '(':
            xml_query += '<nested>'
        elif item == ')':
            xml_query += '</nested>'
        else:
            if not item.strip() or item.count('=') != 1:
                continue
            key, value = item.split('=')
            xml_query += '<cond><key>%s</key><value>%s</value></cond>' % (key, value)

    xml_query = ET.fromstring('<query>%s</query>' % xml_query)
    ET.indent(xml_query)
    # print(ET.tostring(xml_query, encoding='unicode'))
    return xml_query

def make_query(xml_query: ET.Element):
    """Делаем из xml запрос в django стиле
       :param xml_query: результат работы parse_query
    """
    q_item: Q = Q()
    cond = None
    conn_type = Q.AND
    for child in xml_query:
        print('_%s' % child.tag, ET.tostring(child, encoding='unicode'))
        if child.tag == 'cond':
            cond = {child[0].text: child[1].text}
        elif child.tag in ['and', 'or']:
            conn_type = Q.AND if child.tag == 'and' else Q.OR
        elif child.tag == 'nested':
            q_item.add(make_query(child), conn_type)
        if cond:
            q_item.add(Q(**cond), conn_type)
            cond = None
    return q_item
