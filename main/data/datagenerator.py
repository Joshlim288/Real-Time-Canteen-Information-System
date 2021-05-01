from datetime import datetime
from random import randint, choice, sample, uniform
import os
from bson import ObjectId
import pprint
from bson.json_util import dumps
import json
import curated_data

# Get address of data folder
cur_path = os.path.dirname(__file__).split('/')
cur_path = '\\'.join(cur_path[:-1])
desktop_abs_file_path = cur_path + '\\data\\'
abs_file_path = desktop_abs_file_path

with open(abs_file_path + 'restaurant_names', 'r') as file:
    RESTAURANT_NAMES = file.read().splitlines()
with open(abs_file_path + 'food_names', 'r') as file:
    FOOD_NAMES = file.read().splitlines()


def create_restaurants(num_restaurants, range_reg, range_day, range_special, range_dishes):
    restaurants_object = {
        "restaurant": []
    }
    template = {
        "_id": "",
        "name": "",
        "information": "This is a quick description of our restaurant",
        "logo": "http://placehold.it/32x32"
    }
    reg_list = []
    daily_list = []
    special_list = []
    names_list = sample(RESTAURANT_NAMES, num_restaurants)
    for name in names_list:
        restaurant = template.copy()
        object_id = ObjectId()
        restaurant["_id"] = object_id
        num_reg = randint(range_reg[0], range_reg[1])
        num_day = randint(range_day[0], range_day[1])
        num_special = randint(range_special[0], range_special[1])
        for reg in range(num_reg):
            reg_list.append(object_id)
        for day in range(num_day):
            daily_list.append(object_id)
        for special in range(num_special):
            special_list.append(object_id)
        restaurant["name"] = name
        restaurants_object["restaurant"].append(restaurant)

    for restaurant in curated_data.curated_restaurants.values():
        restaurants_object["restaurant"].append(restaurant)

    menus_object, menu_id_list = create_menus(reg_list, daily_list, special_list, range_dishes)
    menu_items_object = create_menu_items(menu_id_list)
    return restaurants_object, menus_object, menu_items_object


def create_menus(reg_list, daily_list, special_list, range_dishes):
    menu_object = {
        "menu": []
    }
    template = {
      "_id": "",
      "restaurant_id": "",
      "name": "",
      "description": "This is a description of our menu",
      "start_datetime": "",
      "end_datetime": "",
      "day_of_week": [],
      "weekly_recurring": True,
      "menu_type": 0,
      "average_waiting_time": 0
    }
    menu_id_list = []
    # generate regular menus
    count = 1
    for _id in reg_list:
        menu = template.copy()
        object_id = ObjectId()
        menu["_id"] = object_id
        menu["restaurant_id"] = _id
        menu["name"] = "Regular menu {}".format(count)
        menu["start_datetime"] = datetime(2019, 1, 1, randint(8, 10), randint(0, 59)).strftime("%Y-%m-%dT%H:%M:%SZ")
        menu["end_datetime"] = datetime(2019, 1, 1, randint(17, 22), randint(0, 59)).strftime("%Y-%m-%dT%H:%M:%SZ")
        menu["day_of_week"] = choice([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7]])
        num_menu_items = randint(range_dishes[0], range_dishes[1])
        for i in range(num_menu_items):
            menu_id_list.append(object_id)
        menu["average_waiting_time"] = round(uniform(5, 7), 2)
        menu_object["menu"].append(menu)
        count += 1
    # generate daily menus
    count = 1
    for _id in daily_list:
        menu = template.copy()
        object_id = ObjectId()
        menu["_id"] = object_id
        menu["restaurant_id"] = _id
        menu["name"] = "Daily menu {}".format(count)
        menu["start_datetime"] = datetime(year=2019, month=1, day=1, hour=randint(8, 10), minute=randint(0, 59)).strftime("%Y-%m-%dT%H:%M:%SZ")
        menu["end_datetime"] = datetime(year=2019, month=1, day=1, hour=randint(17, 22), minute=randint(0, 59)).strftime("%Y-%m-%dT%H:%M:%SZ")
        day_of_week = sample([1, 2, 3, 4, 5, 6, 7], k=randint(1, 3))
        menu["day_of_week"] = day_of_week
        num_menu_items = randint(range_dishes[0], range_dishes[1])
        for i in range(num_menu_items):
            menu_id_list.append(object_id)
        menu["menu_type"] = 1
        menu["average_waiting_time"] = round(uniform(5, 6), 2)
        menu_object["menu"].append(menu)
        count += 1

    # generate special menus
    count = 1
    for _id in special_list:
        special_type = choice([" morning", " night", ""])
        if special_type == " morning":
            h1 = randint(6, 7)
            h2 = randint(10, 12)
        elif special_type == " night":
            h1 = randint(17, 19)
            h2 = randint(21, 23)
        else:
            h1 = randint(8, 10)
            h2 = randint(17, 22)
        menu = template.copy()
        object_id = ObjectId()
        menu["_id"] = object_id
        menu["restaurant_id"] = _id
        menu["name"] = "Special{} menu {}".format(special_type, count)
        start_datetime = datetime(2019, randint(9, 11), randint(1, 10), h1, randint(0, 59))
        end_datetime = datetime(2019, randint(11, 12), randint(15, 29), h2, randint(0, 59))
        menu["start_datetime"] = start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        menu["end_datetime"] = end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        menu["weekly_recurring"] = False
        day_of_week = sample([1, 2, 3, 4, 5, 6, 7], k=randint(1, 3))
        menu["day_of_week"] = day_of_week
        num_menu_items = randint(range_dishes[0], range_dishes[1])
        for i in range(num_menu_items):
            menu_id_list.append(object_id)
        menu["menu_type"] = 2
        menu["average_waiting_time"] = round(uniform(7, 8), 2)
        menu_object["menu"].append(menu)
        count += 1

    for menu in curated_data.curated_menus.values():
        menu_object["menu"].append(menu)

    return menu_object, menu_id_list


def create_menu_items(menu_id_list):
    menu_items_object = {
        "menu_item": []
    }
    template = {
      "_id": "",
      "menu_id": "",
      "name": "",
      "price": 0,
      "image": "http://placehold.it/32x32",
      "category": 0
    }
    names_list = sample(FOOD_NAMES, len(menu_id_list))
    for i in range(len(menu_id_list)):
        menu_item = template.copy()
        object_id = ObjectId()
        menu_item["_id"] = object_id
        menu_item["menu_id"] = menu_id_list[i]
        menu_item["name"] = names_list[i]
        menu_item["price"] = round(uniform(1, 20), 2)
        menu_item["category"] = randint(0, 2)
        menu_items_object["menu_item"].append(menu_item)

    for menu_item_list in curated_data.curated_menu_items.values():
        for menu_item in menu_item_list:
            menu_items_object["menu_item"].append(menu_item)

    return menu_items_object


# Generate data, then write data to JSON file
restaurants, menus, menu_items = create_restaurants(14, [1, 1], [0, 1], [0, 1], [5, 10])


with open('restaurants.json', 'w') as outfile:
    json.dump(dumps(restaurants), outfile, indent=4)

with open('menu.json', 'w') as outfile:
    json.dump(dumps(menus), outfile, indent=4)

with open('menu_items.json', 'w') as outfile:
    json.dump(dumps(menu_items), outfile, indent=4)

