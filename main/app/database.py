import pymongo


class DB(object):

    DATABASE_IP = "localhost"
    DATABASE_PORT = "27017"
    DATABASE_NAME = "Real-Time-Canteen-Information-System"

    RESTAURANT_COLLECTION_NAME = "restaurant"
    MENU_ITEM_COLLECTION_NAME = "menu_item"
    MENU_COLLECTION_NAME = "menu"

    COLLECTIONS = [RESTAURANT_COLLECTION_NAME, MENU_ITEM_COLLECTION_NAME,
                   MENU_COLLECTION_NAME]

    @staticmethod
    def initialize():
        URI = "mongodb://" + DB.DATABASE_IP + ":" + DB.DATABASE_PORT + "/"
        print(URI)
        client = pymongo.MongoClient(URI)
        DB.DATABASE = client[DB.DATABASE_NAME]

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert(data)

    @staticmethod
    def find_one(collection, query):
        return DB.DATABASE[collection].find_one(query)
