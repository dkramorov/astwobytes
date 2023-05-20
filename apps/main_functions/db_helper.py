

class DBAbstract:
    """Абстрактный класс для базы данных,
       чтобы работать с маппингом по таблице
       Пример:

from django.db import connections

CRM_DB = 'vallomcrm'
class CRMCatalogue(DBAbstract):
    table = 'product_categories'
    fields = (
        'id',
        'pid',
        'name',
        'link',
        ...
    )

def load_categories():
    crm_catalogue = CRMCatalogue()
    with connections[CRM_DB].cursor() as cursor:
        cursor.execute(crm_catalogue.get_count_query(table=crm_catalogue.table))
        rows = cursor.fetchall()[0]
        logger.info('total categories in CRM %s' % rows)
        by = 100
        total_pages = int(rows[0] / by) + 1
        logger.info('total categories pages %s, by %s' % (total_pages, by))
        for i in range(total_pages):
            query = crm_catalogue.get_query(table=crm_catalogue.table, fields=crm_catalogue.fields, limit=by, offset=i*by)
            cursor.execute(query)
            rows = cursor.fetchall()
            categories = crm_catalogue.rows2dict(fields=crm_catalogue.fields, rows=rows)
            ...
    """
    def get_count_query(self, table: str):
        return 'select count(id) from %s' % table

    def get_query(self,
                  table: str,
                  fields: list,
                  where: str = None,
                  limit: int = 10,
                  offset: int = 0,
                  order_by: str = 'id'):
        """Запрос в базень"""
        query = 'SELECT %s FROM %s' % (','.join(fields), table)
        if where:
            query += ' WHERE %s' % where
        if order_by:
            query += ' ORDER BY %s' % order_by
        if limit:
            query += ' LIMIT %s' % limit
        if offset:
            query += ' OFFSET %s' % offset
        return query

    def rows2dict(self, fields: list, rows: list):
        """Получение из базени полей словарем"""
        result = {}
        for row in rows:
            item = {field_name: None for field_name in fields}
            for i, value in enumerate(row):
                field_name = fields[i]
                item[field_name] = value
            result[item['id']] = item
        return result
