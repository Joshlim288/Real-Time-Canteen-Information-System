import json
import os
import pprint
import sys
from datetime import datetime
from datetime import timedelta

import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from bson.json_util import loads
from flask import abort, has_request_context
from pymongo.errors import CollectionInvalid

DATABASE_IP = "localhost"
DATABASE_PORT = "27017"
DATABASE_NAME = "Real-Time-Canteen-Information-System"

RESTAURANT_COLLECTION_NAME = "restaurant"
MENU_ITEM_COLLECTION_NAME = "menu_item"
MENU_COLLECTION_NAME = "menu"

COLLECTIONS = [RESTAURANT_COLLECTION_NAME, MENU_ITEM_COLLECTION_NAME,
               MENU_COLLECTION_NAME]

try:
    client = pymongo.MongoClient("mongodb+srv://public_user:1234@cluster0-6pzvi.mongodb.net/test?retryWrites=true&w=majority")
    db = client[DATABASE_NAME]
except Exception as e:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client[DATABASE_NAME]
    print(e, file=sys.stderr)


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
        with open(abs_file_path + "menu.json") as menus:
            menu_data = loads(json.load(menus))['menu']

        with open(abs_file_path + "menu_items.json") as menu_items:
            menu_item_data = loads(json.load(menu_items))["menu_item"]

        with open(abs_file_path + "restaurants.json") as restaurants:
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
        return abort(404) if has_request_context() else {}


def retrieve_collection_count(collection_name):
    """
    Retrieves number of documents in collection.

    Args:
        collection_name (str): Name of collection. It is advised to use pre-defined collection name variables.

    Returns:
        The number of documents in the specified collection.
    """
    if collection_name not in COLLECTIONS:
        print("Invalid collection name while trying to run retrieve_document_by_id()", file=sys.stderr)
        return 0

    collection = db[collection_name]
    return collection.count()


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
    except CollectionInvalid as e:
        print(e, file=sys.stderr)
        return abort(404) if has_request_context() else {}


def _retrieve_restaurant(object_id, with_menus=False, with_menu_items=False):
    """
    Returns restaurant object with menus(if with_menus == True) and menu_items(if with_menu_items = True)

    Args:
        object_id (ObjectId or str): id of the restaurant for retrieval

    Returns:
        If object id is valid, Json restaurant super object is returned. Otherwise, an empty object is returned instead.
    """
    try:
        object_id = ObjectId(object_id)
        restaurant_object = db.restaurant.find_one({"_id": object_id})
        if with_menus and with_menu_items:
            menus = _retrieve_menus(object_id, search_with_restaurant_id=True)
            print(menus)
            restaurant_object["menus"] = menus
        elif with_menus:
            menus_cursor = db.menu.find({"restaurant_id": object_id})
            menus = []
            for menu in menus_cursor:
                menus.append(menu)
            restaurant_object["menus"] = menus

        return restaurant_object

    except InvalidId as e:
        print(e, file=sys.stderr)
        return abort(404) if has_request_context() else {}


def retrieve_restaurant_by_name(name, super_object=False):
    """
    Retrieve restaurant object or restaurant super object via restaurant name

    Args:
        name (str): Accepts strings. String must be a valid restaurant name.
        super_object (bool): Accepts boolean values. Default is False.

    Returns:
        If name is valid:
            If super_object=True, returns restaurant super object
            Otherwise, returns restaurant object only
        Otherwise, returns empty object
    """
    object_id = db.restaurant.find_one({"name": name}, {"_id": True})
    if object_id is None:
        print("Invalid restaurant name while trying to run retrieve_restaurant_by_name()", file=sys.stderr)
        return {}
    else:
        if super_object:
            return _retrieve_restaurant(object_id, with_menus=True, with_menu_items=True)
        else:
            return _retrieve_restaurant(object_id, with_menus=False, with_menu_items=False)


def menu_is_available(menu_object, current_datetime=datetime.now(), by_date_only=False):
    """
    Checks if menu object is available at current application time

    Args:
        menu_object (JSON menu object): menu to be evaluated
        current_datetime (datetime): Time to take as 'now', defaults to current system datetime
        by_date_only (bool): Retrieve based only on date

    Returns:
        If menu object is valid:
            If menu is available, returns True
            Else, returns False
        Else, returns False and prints error-handling message
    """
    # Checks that menu_object is structured like a JSON menu object
    menu_object_check = True
    if isinstance(menu_object, dict):
        menu_object_fields = ["_id", "restaurant_id", "name", "description", "start_datetime", "end_datetime",
                              "day_of_week", "weekly_recurring", "menu_type", "average_waiting_time", ]
        for field in menu_object_fields:
            if not (field in menu_object):
                menu_object_check = False
                print("Invalid menu object while running menu_is_available(). ",
                      "'", field, "' is missing from the object.", sep="", file=sys.stderr)
                break
    else:
        menu_object_check = False
        print("Invalid menu object while running menu_is_available().",
              "Object passed is not a JSON object", file=sys.stderr)

    # Check if menu is available
    if menu_object_check:
        opening_datetime = datetime.strptime(menu_object["start_datetime"], "%Y-%m-%dT%H:%M:%SZ")
        closing_datetime = datetime.strptime(menu_object["end_datetime"], "%Y-%m-%dT%H:%M:%SZ")

        # Check if menu is a special menu, and if it is within available period
        if menu_object["menu_type"] == 2 and not opening_datetime <= current_datetime <= closing_datetime:
            return False

        # Check if menu is available on current application_datetime day
        if current_datetime.isoweekday() not in menu_object["day_of_week"]:
            return False

        # Check if menu is available at current time
        if by_date_only or opening_datetime.time() <= current_datetime.time() <= closing_datetime.time():
            return True
        else:
            return False

    # Error-handling output value
    else:
        return False


def retrieve_available_restaurants(starting_index, ending_index, current_datetime=datetime.now()):
    """
    Retrieves restaurants that are available at current APPLICATION_DATETIME, returns list of
    varying number of restaurant objects, depending on input parameters

    Args:
        starting_index (int): index of first element in results list to be returned
        ending_index (int): index of last element to be returned
        current_datetime (datetime): Time to take as 'now', defaults to current system datetime

    Returns:
        dictionary containing a list of restaurants available, sliced with [starting_index, ending_index + 1]
    """
    restaurant_list = []
    ending_index += 1
    # find which restaurants are currently available
    available_restaurant_ids = []
    all_menus = db.menu.find({})
    for menu in all_menus:

        # skip menu if the restaurant has already been processed
        if menu["restaurant_id"] not in available_restaurant_ids and menu_is_available(menu, current_datetime):
            available_restaurant_ids.append(menu["restaurant_id"])

            # Retrieve operating hours for all of the restaurant's menus
            operating_hours = retrieve_restaurant_operating_hours(menu["restaurant_id"], current_datetime, only_current_day=True)
            operating_hours = operating_hours[current_datetime.isoweekday()]
            start_time = datetime.max.time()
            end_time = datetime.min.time()

            # Take the total period the restaurant is open for current_datetime.date()
            for menu_operating_hour in operating_hours:
                if menu_operating_hour["start_time"] < start_time:
                    start_time = menu_operating_hour["start_time"]
                if menu_operating_hour["end_time"] > end_time:
                    end_time = menu_operating_hour["end_time"]

            # Calculate the average waiting time among all currently available menus for the restaurant
            time_sum = 0
            count = 0
            available_menus = retrieve_menus_by_datetime(menu["restaurant_id"], current_datetime)

            for available_menu in available_menus:
                time_sum += available_menu["average_waiting_time"]
                count += 1
                average_waiting_time = round(time_sum / count, 2)

            restaurant = db.restaurant.find_one({"_id": menu["restaurant_id"]})
            restaurant["average_waiting_time"] = average_waiting_time
            restaurant["start_time"] = str(start_time)
            restaurant["end_time"] = str(end_time)
            restaurant_list.append(restaurant)

    # sort entries according to waiting time
    restaurant_list.sort(key=lambda x: float(x["average_waiting_time"]))
    restaurant_dictionary = {"restaurant_count": len(restaurant_list)}

    # Slice list with index given
    if ending_index <= len(restaurant_list):
        restaurant_dictionary["restaurants"] = restaurant_list[starting_index:ending_index]
    elif starting_index < len(restaurant_list):
        restaurant_dictionary["restaurants"] = restaurant_list[starting_index:]
    else:
        restaurant_dictionary["restaurants"] = {}

    return restaurant_dictionary


def retrieve_menus_by_datetime(restaurant_id, current_datetime=datetime.now(), by_date_only=False):
    """
    Retrieve all menus from a restaurant that are currently available based on application time

    Args:
        restaurant_id (ObjectId):  Restaurant's object id
        current_datetime (datetime): Time to take as 'now', defaults to current system datetime
        by_date_only (bool): Only take date into account

    Returns:
        list of JSON menu super objects if any are currently available, and an empty list otherwise
    """
    # Called function retrieve_all_restaurant_menus() provides error-handling for invalid id
    menu_list = []
    all_menus = retrieve_all_restaurant_menus(restaurant_id)
    for menu in all_menus:
        if menu_is_available(menu, current_datetime, by_date_only):
            menu_list.append(menu)
    return menu_list


def retrieve_all_restaurant_menus(restaurant_id):
    """
    Retrieve only all restaurant menus via restaurant's object id.
    Args:
        restaurant_id (ObjectId): restaurant's object id

    Returns:
        List of restaurants menu

    """
    menu_list = []
    try:
        if not restaurant_id:
            print("Invalid restaurant id while trying to run restaurant_current_menus()", file=sys.stderr)
        else:
            cursor = db.menu.aggregate([
                {"$match": {"restaurant_id": ObjectId(restaurant_id)}}, {
                    "$lookup": {
                        "from": "menu_item",
                        "localField": "_id",
                        "foreignField": "menu_id",
                        "as": "menu_items"
                    }
                }
            ])
            for menu in cursor:
                menu_list.append(menu.copy())
        return menu_list
    except InvalidId as e:
        print(e, file=sys.stderr)
        return abort(404) if has_request_context() else menu_list


def retrieve_entire_restaurant(object_id):
    """
    Retrieves restaurant super object

    Args:
        object_id (ObjectId): Accepts ObjectId or str types. Must be a valid ObjectId formatted string.

    Returns:
        If object id is valid, returns restaurant super object
        Otherwise, returns empty object
    """
    try:
        return _retrieve_restaurant(ObjectId(object_id), with_menus=False, with_menu_items=False)

    except InvalidId as e:
        print(e, file=sys.stderr)
        return abort(404) if has_request_context() else {}


def retrieve_restaurant_operating_hours(object_id, current_datetime=datetime.now(), only_current_day=False):
    """
    Retrieve restaurant's operating hours

    Args:
        object_id (ObjectId): Accepts restaurant ObjectId or str types. Must be a valid ObjectId formatted string.
        current_datetime (datetime): Accepts Datetime objects, will be used to determine if seasonal menus are available
        only_current_day (bool): If True, will return only the operating hours for the current day, according to
                                 current_datetime

    Returns:
        If object id is valid, returns operating hours super object (dictionary):
            keys are integers representing days of the weeks (1-7)
            values:
                lists of corresponding operating hour objects (with start and end time objects)
                or empty list if there are no available menus on that day
        Otherwise, returns empty object

        If only_current_day is True, returns a list of operating hours for the restaurant, only on the day specified
        in current_datetime
    """
    try:
        all_menus = retrieve_all_restaurant_menus(ObjectId(object_id))
        # Super object starts with an empty list for each day
        operating_hours_dict = {day: [] for day in range(1, 8)}

        for menu in all_menus:
            menu_opening_datetime = datetime.strptime(menu["start_datetime"], "%Y-%m-%dT%H:%M:%SZ")
            menu_closing_datetime = datetime.strptime(menu["end_datetime"], "%Y-%m-%dT%H:%M:%SZ")
            menu_opening_time = menu_opening_datetime.time()
            menu_closing_time = menu_closing_datetime.time()

            # Check if special menu is running
            if menu["menu_type"] == 2:
                # Special menu is running, check menu's start and end dates
                if menu_opening_datetime <= current_datetime <= menu_closing_datetime:
                    day_1_timedelta = timedelta(days=1)
                    current_day_int = current_datetime.isoweekday()
                    start_of_week_datetime = current_datetime - ((current_day_int - 1) * day_1_timedelta)
                    end_of_week_datetime = current_datetime + ((7 - current_day_int) * day_1_timedelta)
                    # Account for special menu start date
                    if menu_opening_datetime > start_of_week_datetime:
                        for day in range(1, current_day_int):
                            if day in menu["day_of_week"]:
                                menu["day_of_week"].remove(day)
                    # Account for special menu end date
                    if menu_closing_datetime < end_of_week_datetime:
                        for day in range(7, current_day_int, -1):
                            if day in menu["day_of_week"]:
                                menu["day_of_week"].remove(day)
                # Special menu is not running and will be skipped
                else:
                    continue

            # Update list for each day
            for day in menu["day_of_week"]:
                if only_current_day and day != current_datetime.isoweekday():
                    continue
                new_operating_hour_check = True

                # If the day's list is empty, add a new operating hours object
                if not operating_hours_dict[day]:
                    operating_hours_dict[day].append({"start_time": menu_opening_time, "end_time": menu_closing_time})

                # Overlaps with operating hours objects currently in operating_hours_dict, update operating hours object
                for operating_hours_object in operating_hours_dict[day]:
                    if not (menu_closing_time < operating_hours_object["start_time"] or
                            menu_opening_time > operating_hours_object["end_time"]):
                        operating_hours_object["start_time"] = min(menu_opening_time,
                                                                   operating_hours_object["start_time"])
                        operating_hours_object["end_time"] = max(menu_closing_time,
                                                                 operating_hours_object["end_time"])
                        new_operating_hour_check = False

                # No overlaps with operating hours objects currently in operating_hours_dict,
                # Add a new operating hours object and sort list according to start time
                if new_operating_hour_check:
                    operating_hours_dict[day].append({"start_time": menu_opening_time, "end_time": menu_closing_time})
                    # Sorts operating hours of a day by start time
                    operating_hours_dict[day] = sorted(operating_hours_dict[day], key=lambda k: k["start_time"])

        return operating_hours_dict

    except InvalidId as e:
        print(e, file=sys.stderr)
        return abort(404) if has_request_context() else {}


def retrieve_current_restaurants_with_operating_hours(current_datetime=datetime.now()):
    """
    Retrieve list of tuples for restaurants that are currently available.
    tuple[0] contains restaurant object, tuple[1] contains it's operating hours

    Returns:
        list of tuples if any restaurants are open, empty list otherwise
    """
    final_list = []
    restaurant_ids = []
    all_menus = db.menu.find({})

    # retrieve ids of available restaurants
    for menu in all_menus:
        if menu_is_available(menu, current_datetime):
            restaurant_ids.append(menu["restaurant_id"])

    # fetch restaurants, fetch their operating hours, combine them into a tuple
    for _id in set(restaurant_ids):
        final_list.append((retrieve_entire_restaurant(_id), retrieve_restaurant_operating_hours(_id)))
    return final_list


def _retrieve_menus(object_id, search_with_restaurant_id=False):
    """
    If search_with_restaurant_id param is False, retrieves an individual menu super object.
    Else when True, method will fetch a list of menu super objects associated with the restaurant id that is
    passed via the object_id param.

    Args:
        object_id (ObjectId): Accepts ObjectId or str types. Must be a valid ObjectId formatted string.
        search_with_restaurant_id (bool): Accepts boolean values. Default parameter value is False.

    Returns:
        If search_with_restaurant_id is false:
            If menu object id is valid, returns a single menu super object
            Otherwise, returns empty object
        Else if search_with_restaurant_id is true:
            If restaurant object id is valid, returns list of menu super objects related to the restaurant
            Otherwise, returns empty list
    """
    # Return list of menu super objects related to the restaurant
    # Called function retrieve_all_restaurant_menus() provides error-handling for invalid id
    if search_with_restaurant_id:
        menu_list = retrieve_all_restaurant_menus(object_id)
        menu_super_object_list = []
        if not menu_list:
            print("Invalid restaurant id while trying to run _retrieve_menus(search_with_restaurant_id=True)", file=sys.stderr)
        for menu in menu_list:
            menu_id = menu["_id"]
            menu_item_list = list(db.menu_item.find({"menu_id": menu_id}))
            # Create menu super object and add it to the list
            menu_super_object = menu
            menu_super_object["menu_items"] = menu_item_list
            menu_super_object_list.append(menu_super_object)
        return menu_super_object_list

    # Return single menu super object
    else:
        try:
            menu_object = db.menu.find_one({"_id": ObjectId(object_id)})
            if menu_object:
                menu_item_list = list(db.menu_item.find({"menu_id": ObjectId(object_id)}))
                # Create menu super object
                menu_super_object = menu_object
                menu_super_object["menu_items"] = menu_item_list
                return menu_super_object
            else:
                print("Invalid restaurant id while trying to run _retrieve_menus(search_with_restaurant_id=False)", file=sys.stderr)
                return {}

        except InvalidId as e:
            print(e, file=sys.stderr)
            return abort(404) if has_request_context() else {}


def retrieve_menu_user_input(user_start_datetime=datetime.min, user_end_datetime=datetime.max, min_duration=1):
    """
    Retrieves menu super objects based on user-defined datetime

    Args:
        user_start_datetime (datetime): Accepts datetime objects. Must precede end_datetime.
        user_end_datetime (datetime): Accepts datetime objects. Must succeed user_start_datetime.
        min_duration (int): Accepts integer or float values. Must have a positive or zero value. Default is 1.

    Returns:
        If user_start_datetime, user_end_datetime and min_duration are valid, returns list of menu super objects
        Otherwise, returns empty list
    """
    # Check if start and end datetimes are valid
    datetime_check = False
    if isinstance(user_start_datetime, datetime) and isinstance(user_end_datetime, datetime):
        if user_start_datetime < user_end_datetime:
            datetime_check = True

    # Check if min_duration is valid
    min_duration_check = False
    if isinstance(min_duration, int) or isinstance(min_duration, float):
        if min_duration >= 0:
            min_duration_check = True
            min_duration_timedelta = timedelta(hours=min_duration)

    # Create list of menu super objects
    super_object_list = []
    if datetime_check and min_duration_check:
        cursor = db.menu.find({}, projection={"start_datetime": True, "end_datetime": True})
        for menu in cursor:
            menu_opening_datetime = datetime.strptime(menu["start_datetime"], "%Y-%m-%dT%H:%M:%SZ")
            menu_closing_datetime = datetime.strptime(menu["end_datetime"], "%Y-%m-%dT%H:%M:%SZ")
            # Check for overlap between menu operating hours and user-defined datetime range
            if (menu_closing_datetime < user_start_datetime + min_duration_timedelta or
               menu_opening_datetime > user_end_datetime - min_duration_timedelta):
                continue
            else:
                super_object_list.append(_retrieve_menus(menu["_id"]))
        return super_object_list

    # Error handling
    else:
        if not datetime_check:
            print("Invalid start and end datetime while trying to run calc_wait_time()", file=sys.stderr)
        elif not min_duration_check:
            print("Invalid min duration while trying to run calc_wait_time()", file=sys.stderr)
        return []


def retrieve_menu_items(object_id):
    """
    Retrieve's all of menu's menu items.

    Args:
        object_id (ObjectId): Accepts ObjectId or str types. Must be a valid ObjectId formatted string.

    Returns:
        If object id is valid, returns list of menu items otherwise, an empty list will be returned.
    """
    try:
        menu_items_list = list(db.menu_item.find({"menu_id": ObjectId(object_id)}))
        if not menu_items_list:
            print("Invalid menu id while trying to run retrieve_menu_items()", file=sys.stderr)
        return menu_items_list

    except InvalidId as e:
        print(e, file=sys.stderr)
        return abort(404) if has_request_context() else []


def calc_wait_time(object_id, people_in_queue):
    """
    Retrieves average waiting time then calculates waiting time

    Args:
        object_id (ObjectId): Accepts restaurant ObjectId or str types. Must be a valid ObjectId formatted string.
        people_in_queue (int): Accepts integer values. Integer must have a positive or zero value.

    Returns:
        If object_id is valid and people_in_queue is a positive integer, returns waiting time integer in minutes
        Else, returns 0
    """
    try:
        # Check is people_in_queue is valid
        people_in_queue_check = False
        if isinstance(people_in_queue, int):
            if people_in_queue >= 0:
                people_in_queue_check = True

        # Calculate waiting time
        if people_in_queue_check:
            all_menus = list(db.menu.find({"restaurant_id": ObjectId(object_id)}))
            if all_menus:
                waiting_time_sum = 0
                menu_no = 0
                for menu in all_menus:
                    waiting_time_sum += menu["average_waiting_time"]
                    menu_no += 1
                waiting_time = round(people_in_queue * waiting_time_sum / menu_no, 2)
                return waiting_time

            # Error handling for invalid restaurant id
            else:
                print("Invalid restaurant id while trying to run calc_wait_time()", file=sys.stderr)
                return 0

        # Error handling for invalid people_in_queue
        else:
            print("Invalid number of people while trying to run calc_wait_time()", file=sys.stderr)
            return 0

    # Error handling for invalid object id
    except InvalidId as e:
        print(e, file=sys.stderr)
        return abort(404) if has_request_context() else 0


def close_mongodb_connection():
    client.close()


# Check mongodb connection and print out server info for logging purposes.
pprint.pprint(client.server_info())
