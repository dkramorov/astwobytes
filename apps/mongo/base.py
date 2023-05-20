from pymongo import MongoClient, DESCENDING

def get_database(host: str = '127.0.0.1',
                 port: str = '27017',
                 db_name: str = 'potestua',
                 login: str = '',
                 passwd: str = ''):
    conn = 'mongodb://%s:%s@%s:%s/%s' % (login, passwd, host, port, db_name)
    if not login or not passwd:
        conn = 'mongodb://%s:%s/%s' % (host, port, db_name)
    client = MongoClient(conn)
    return client[db_name]

def get_collection(collection_name: str = 'example'):
    db = get_database()
    return db[collection_name]

def insert_many(collection, docs: list = None):
    if not docs:
        item_1 = {
            'price': 340,
            'name': 'test1',
        }
        item_2 = {
            'price': 36,
            'name': 'test2',
        }
        docs = [item_1, item_2]
    return collection.insert_many(docs)

def insert_one(collection, doc: dict = None):
    if not doc:
        item_1 = {
            'price': 340,
            'name': 'test1',
        }
    return collection.insert_one(doc)

def create_index(collection, fields: str):
    return collection.create_index(fields)

def get_sort_desc():
    return [( '_id', DESCENDING )]

def find_one_last(collection, query):
    return collection.find_one(query, sort=get_sort_desc())
