import json
import os
import pprint
import sys
from datetime import datetime

import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from bson.json_util import loads
from flask import Flask

DATABASE_IP = "localhost"
DATABASE_PORT = "27017"
DATABASE_NAME = "Real-Time-Canteen-Information-System"

RESTAURANT_COLLECTION_NAME = "restaurant"
MENU_ITEM_COLLECTION_NAME = "menu_item"
MENU_COLLECTION_NAME = "menu"
OPERATING_HOUR_COLLECTION_NAME = "operating_hour"

COLLECTIONS = [RESTAURANT_COLLECTION_NAME, MENU_ITEM_COLLECTION_NAME,
               MENU_COLLECTION_NAME, OPERATING_HOUR_COLLECTION_NAME]

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Real-Time-Canteen-Information-System"
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client[DATABASE_NAME]


def create_test_data():
    """
    Creates test data from json file generated from online json generator.

    Returns:
        boolean success

    """
    try:
        cur_path = os.path.dirname(__file__).split('/')
        cur_path = '\\'.join(cur_path[:-2])
        desktop_abs_file_path = cur_path + '\\data\\'
        abs_file_path = desktop_abs_file_path
        with open(abs_file_path + "menu(2).json") as menus:
            menu_data = loads(json.load(menus))['menu']

        with open(abs_file_path + "menu_items(2).json") as menu_items:
            menu_item_data = loads(json.load(menu_items))["menu_item"]

        with open(abs_file_path + "restaurants(2).json") as restaurants:
            restaurant_data = loads(json.load(restaurants))["restaurant"]

        # Print test data for checking.
        print("\nRestaurants\n==================================")
        pprint.pprint(restaurant_data)

        print("\nMenus\n==================================")
        pprint.pprint(menu_data)

        print("\nMenu Items\n==================================")
        pprint.pprint(menu_item_data)

        # Create the individual collections if it does not exist.
        if db.restaurant is None:
            menu_item_collection = db[RESTAURANT_COLLECTION_NAME]

        if db.menu is None:
            menu_item_collection = db[MENU_COLLECTION_NAME]

        if db.menu_item is None:
            menu_item_collection = db[MENU_ITEM_COLLECTION_NAME]

        # Inserts formatted json data into Mongodb collections
        db.menu_item.insert_many(menu_item_data)
        db.menu.insert_many(menu_data)
        db.restaurant.insert_many(restaurant_data)

        return True
    except Exception as e:
        print(e)
        return False


def retrieve_document_by_id(collection_name="", object_id=""):
    """
    Retrieve single document filtered by it's object id value.
    NOTE: Method will ONLY return the document without it's related objects.

    Args:
        collection_name (str): Collection that document resides in.
        object_id (ObjectId): Accepts ObjectId or str types. Must be a valid ObjectId formatted string.

    Returns:
        If collection name is valid, returns document json otherwise, an empty object will be returned.

    """
    if collection_name not in COLLECTIONS:
        print("Invalid collection name while trying to run retrieve_document_by_id()", file=sys.stderr)
        return {}

    try:
        collection = db[collection_name]
        document = collection.find_one({"_id": ObjectId(object_id)})
        return document
    except InvalidId as e:
        print(e, file=sys.stderr)
        return {}


def delete_all_collection_data(collection_name):
    """
    Deletes all documents from a collection.

    Args:
        collection_name (str): Name of collection for deletion.

    Returns:
        response object
    """
    if collection_name not in COLLECTIONS:
        print("Invalid collection name while trying to run retrieve_collection()", file=sys.stderr)
        return {}

    collection = db[collection_name]
    response = collection.delete_many({})
    print(response.deleted_count, "documents deleted.")

    return response


def retrieve_collection(collection_name=""):
    """
    Retrieve all documents from a specific collection.
    NOTE: This method retrieves all documents without it's relations from the specified collection.

    Args:
        collection_name (str): collection for retrieval

    Returns:
        If collection name is valid, returns entire collection otherwise, an empty object will be returned.

    """
    if collection_name not in COLLECTIONS:
        print("Invalid collection name while trying to run retrieve_collection()", file=sys.stderr)
        return {}

    try:
        collection = db[collection_name]
        document = list(collection.find())
        return document
    except InvalidId as e:
        print(e, file=sys.stderr)
        return {}


def _retrieve_restaurant(object_id, with_restaurant=True, with_menus=False, with_menu_items=False):
    """
    TODO

    Args:
        object_id (ObjectId): id of the restaurant for retrieval

    Returns:
        If object id is valid, Json restaurant super object is returned. Otherwise, an empty object is returned instead.
    """
    try:
        query = [
            {"$match": {"_id": ObjectId(object_id)}}, {
                "$project": {
                    "_id": 1,
                    "name": 1,
                    "information": 1,
                    "logo": 1
                }
            }
        ]

        query_project = query[1]["$project"]
        # if with_restaurant is False:
        #     query_project["name"] = 0
        #     query_project["information"] = 0
        #     query_project["logo"] = 0

        if with_menus is True:
            menu_query = {
                "$lookup": {
                    "from": "menu",
                    "pipeline": [
                        {"$match": {"restaurant_id": ObjectId(object_id)}}
                    ],
                    "as": "menus"
                }
            }
            query_project["menus"] = 1

            if with_menu_items is True:
                query_project["menu_items"] = 1
                menu_item_query = {
                    "$lookup": {
                        "from": "menu_item",
                        "let": {"menu_items": "$menu_items"},
                        "pipeline": [
                            {"$match": {"$expr": {"$in": ["$_id", "$$menu_items"]}}}
                        ],
                        "as": "menu_items"
                    }
                }
                menu_query["$lookup"]["pipeline"].append(menu_item_query)

        pprint.pprint(query)

        restaurant = db.restaurant.aggregate(query)
        return list(restaurant)

    except InvalidId as e:
        print(e, file=sys.stderr)
        return {}


def restaurant_by_name(name=""):
    # TODO
    pass


def retrieve_available_restaurants(application_time=datetime.now()):
    """
    TODO convert to mongodb query?
    Retrieves a list of ids for restaurants that are open based on application time

    Args:
        application_time (datetime): Accepts datetime object for a user defined time. Default value is current system time

    Returns:
        list of JSON restaurant super objects for all available restaurants if any are open, and an empty list otherwise
    """

    restaurant_collection = db[RESTAURANT_COLLECTION_NAME]
    operating_hours_collection = db[OPERATING_HOUR_COLLECTION_NAME]
    cursor = restaurant_collection.find({})
    available_restaurants_list = []
    for restaurant in cursor:
        for operating_hour in restaurant['operating_hours']:
            operating_hour_id = operating_hour['operating_hour_id']
            operating_hour = operating_hours_collection.find_one({"_id": ObjectId(operating_hour_id)})
            opening_time = operating_hour['start_datetime']
            closing_time = operating_hour['end_datetime']
            if opening_time < application_time < closing_time:
                available_restaurants_list.append(restaurant)
                break

    return available_restaurants_list


def retrieve_restaurant_current_menus(object_id):
    """"""
    # TODO
    pass


def retrieve_all_restaurant_menus(object_id):
    """
    TODO
    Retrieve only all restaurant menus via restaurant's object id.
    Args:
        object_id (ObjectId): restaurant's object id

    Returns:
        List of restaurants menu

    """
    return _retrieve_restaurant(object_id, with_restaurant=True, with_menus=True, with_menu_items=True)


def retrieve_entire_restaurant(object_id):
    """
    TODO
    Args:
        object_id:

    Returns:

    """
    return _retrieve_restaurant(object_id, with_restaurant=True, with_menus=True, with_menu_items=True)



# def retrieve_restaurants_by_operating_hours(starting_index, ending_index, start_datetime=datetime.min(), end_datetime=datetime.max()):
#     """
#     Retrieve list of base restaurant objects using operating hours.
#     Dates: Starting date taken from start_datetime.date()
#            Ending date taken from end_datetime.date()
#     Time: Takes time from .time() components of inputs
#     If menu is available any day in the stated period, the menu is returned
#
#     Args:
#         starting_index (int): index of first element in results list to be returned
#         ending_index (int): index of last element to be returned
#         start_datetime (datetime): Starting datetime to search from
#         end_datetime (datetime): Datetime to search until
#
#     Returns:
#         List of restaurants stated within start datetime and end datetime. Number of elements varies based on
#         user input.
#     """
#     restaurant_list = []
#     restaurant_ids = []
#     all_menus = db.menu.find({})
#     days_difference = int(str((end_datetime - start_datetime)).split(' ')[0])
#
#     # Generate list of which days which are in the date range passed into the function
#     if days_difference >= 7:
#         days_list = [i for i in range(1, 8)]
#     elif end_datetime.isoweekday() < start_datetime.isoweekday():
#         days_list = [i for i in range(start_datetime.isoweekday(), 8)] + [i for i in range(1, end_datetime.isoweekday() + 1)]
#     else:
#         days_list = [i for i in range(start_datetime.isoweekday(), end_datetime.isoweekday() + 1)]
#
#     # retrieve ids of available restaurants
#     for menu in all_menus:
#         opening_datetime = datetime.strptime(menu["start_datetime"], "%Y-%m-%dT%H:%M:%SZ")
#         closing_datetime = datetime.strptime(menu["end_datetime"], "%Y-%m-%dT%H:%M:%SZ")
#
#         # Check if menu is a special menu, and if it is within available period
#         if menu["menu_type"] == 2:
#             if not opening_datetime.date() <= start_datetime.date() and not end_datetime.date() >= closing_datetime.date():
#                 continue
#
#         # Check if restaurants are open on any days within the period
#         for day in days_list:
#             if day in menu["day_of_week"]:
#                 break
#         else:
#             continue
#
#         # Check if menu is available at time stated in argument
#         if opening_datetime.time() <= start_datetime.time() and closing_datetime.time() >= end_datetime.time():
#             restaurant_ids.append(menu["restaurant_id"])
#
#     # Get list of restaurants that meet operating hour criteria, add them to the list and sort them
#     for _id in set(restaurant_ids):
#         restaurant_list.append(retrieve_entire_restaurant(_id))
#     restaurant_list.sort(key=lambda x: x['name'].lower())
#
#     # Slice list with index given
#     if ending_index <= len(restaurant_list):
#         return restaurant_list[starting_index:ending_index]
#     elif starting_index < len(restaurant_list):
#         return restaurant_list[starting_index:]
#     else:
#         return []



def _retrieve_menus(object_id="", search_with_restaurant_id=False,
                    start_datetime=datetime.min, end_datetime=datetime.max):
    """
        TODO Rework method and purpose to query for
        Depending on method call, this method has two main functions.
        First, the method by default will query a super menu
        If search_with_restaurant_id param is False, method will retrieve an individual super menu object.
        Else when True, method will fetch a list of menus associated with the restaurant id that is
        passed via the object_id param.

        Args:
            object_id (ObjectId): id of the menu for retrieval.
            search_with_restaurant_id (bool): If true, method will query for menu super object via restaurant_id index. Otherwise, menu's _id will be used instead. Default parameter value is False.
            start_datetime (datetime): start datetime of datetime range for query to check against.
            end_datetime (datetime): end datetime of datetime range for query to check against.

        Returns:
            If object id is valid, Json menu super object is returned. Otherwise, an empty object is returned instead.
        """
    try:
        # Check if either only start or end datetime have been set by method call. If so, reset both to default.
        if (start_datetime != datetime.min and end_datetime == datetime.max) or \
                (start_datetime == datetime.min and end_datetime != datetime.max):
            start_datetime = datetime.min
            end_datetime = datetime.max

        menu = db.menu.aggregate([
            {
                "$match": {
                    "_id" if search_with_restaurant_id is False else "restaurant_id": ObjectId(object_id)
                }
            }, {
                "$lookup": {
                    "from": "menu_item",
                    "let": {"menu_items": "$menu_items"},
                    "pipeline": [
                        {"$match": {
                            "$expr": {
                                "$and": [
                                    {"$in": ["$_id", "$$menu_items"]},
                                    {"$lte": ["$start_datetime", end_datetime]},
                                    {"$gte": ["$start_datetime", start_datetime]},
                                    {"$lte": ["$end_datetime", end_datetime]},
                                    {"$gte": ["$end_datetime", start_datetime]}
                                ]
                            }}
                        }
                    ],
                    "as": "menu_items"
                }
            }
        ])
        return list(menu)

    except InvalidId as e:
        print(e, file=sys.stderr)
        return {}


def retrieve_menu_user_input(start_datetime=datetime.min, end_datetime=datetime.max):
    # TODO
    pass


def retrieve_menu_items(object_id):
    """Retrieve's all of menu's menu items.

    Args:
        object_id (ObjectId): Accepts ObjectId or str types. Must be a valid ObjectId formatted string.

    Returns:
        If object id is valid, returns list of menu items otherwise, an empty object will be returned.
    """
    try:
        menu_collection = db[MENU_COLLECTION_NAME]
        menu = menu_collection.find_one({"_id": ObjectId(object_id)})

        menu_item_collection = db[MENU_ITEM_COLLECTION_NAME]
        menu_items = list(menu_item_collection.find({
            "_id": {
                "$in": menu["menu_items"]
            }
        }))
    except InvalidId as e:
        print(e, file=sys.stderr)
        return {}

    return menu_items


def calculate_waiting_time(object_id, no_of_people):
    """
    Retrieves average waiting time then calculates waiting time
    Args:
        object_id (ObjectId): Accepts ObjectId or str types. Must be a valid ObjectId formatted string.
        no_of_people (int): Accepts integer values. Integer must have a positive value.
    Returns:
        If object id is valid, returns integer value of waiting time otherwise, a 0 will be returned.
    """
    try:
        menu_collection = db[MENU_COLLECTION_NAME]
        average_waiting_time = menu_collection.find_one({"_id": object_id}, {"average_waiting_time": 1})
        waiting_time = no_of_people * average_waiting_time

    except InvalidId as e:
        print(e, file=sys.stderr)
        return 0

    return waiting_time


client.close()
