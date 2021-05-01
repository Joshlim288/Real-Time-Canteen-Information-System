import math
import sys
from datetime import datetime

from bson.errors import InvalidId
from flask import render_template, abort

from main.app.core import bp
from main.app.core import mongodb
from main.app.utils.RoutesUtil import RoutesUtil

MAIN_MENU_ITEMS_INDEX = 0
DRINKS_MENU_ITEMS_INDEX = 1
SIDES_MENU_ITEMS_INDEX = 2
MAX_RESTAURANT_ITEM_PER_PAGE = 6

# Unfortunately, when testing changes in CSS styling for HTML pages Ctrl + Shift + R must be used instead
# of F5 as the browser caches static files. The method above refresh the page while clearing browser cache.
APPLICATION_DATETIME = datetime(2019, 10, 10, 11, 0, 0, 0)


def retrieve_paginated_available_restaurants(page_number=1, custom_datetime=datetime.now()):
    items_per_page = MAX_RESTAURANT_ITEM_PER_PAGE
    pagination_start_index = (page_number - 1) * items_per_page
    pagination_end_index = (page_number * items_per_page) - 1
    return mongodb.retrieve_available_restaurants(pagination_start_index, pagination_end_index, custom_datetime)


@bp.route("/")
@bp.route("/restaurants")
@bp.route("/restaurants/<page_number>")
def restaurants(page_number=1):
    # Retrieve currently available restaurants
    # Pass list of restaurants and size of list
    page_number = int(page_number)
    restaurant_dictionary = retrieve_paginated_available_restaurants(page_number=page_number)
    available_restaurants_count = restaurant_dictionary["restaurant_count"]

    # If URL called with page number exceeding max pages for current query, abort to Error 404.
    if page_number > math.ceil(available_restaurants_count / MAX_RESTAURANT_ITEM_PER_PAGE):
        abort(404)

    return render_template("landing.html",
                           page_number=page_number,
                           available_restaurants_count=available_restaurants_count,
                           restaurants=restaurant_dictionary["restaurants"]), 200


@bp.route("/restaurants/custom/<custom_datetime>")
@bp.route("/restaurants/custom/<page_number>/<custom_datetime>")
def restaurant_datetime(custom_datetime, page_number=1):
    page_number = int(page_number)
    formatted_custom_datetime = datetime.strptime(custom_datetime, "%Y-%m-%d %H:%M:%S")
    restaurant_dictionary = retrieve_paginated_available_restaurants(page_number, formatted_custom_datetime)
    available_restaurants_count = restaurant_dictionary["restaurant_count"]

    # If URL called with page number exceeding max pages for current query, abort to Error 404.
    if page_number > math.ceil(available_restaurants_count / MAX_RESTAURANT_ITEM_PER_PAGE):
        abort(404)

    return render_template("landing.html",
                           page_number=page_number,
                           available_restaurants_count=available_restaurants_count,
                           restaurants=restaurant_dictionary["restaurants"],
                           custom_dt_value=custom_datetime), 200


@bp.route("/restaurants/current/<restaurant_id>/operating_hours")
@bp.route("/restaurants/custom/<restaurant_id>/<datetime_value>/operating_hours")
def restaurant_operating_hours(restaurant_id, datetime_value=datetime.now()):
    formatted_custom_datetime = datetime_value
    if type(datetime_value) is not datetime:
        formatted_custom_datetime = datetime.strptime(datetime_value, "%Y-%m-%d %H:%M:%S")

    all_restaurant_operating_hours = mongodb.retrieve_restaurant_operating_hours(restaurant_id, formatted_custom_datetime)
    sorted_operating_hours = RoutesUtil.sort_operating_hours(all_restaurant_operating_hours, formatted_custom_datetime.isoweekday())
    return render_template("restaurant-operating-hours.html",
                           operating_hours=sorted_operating_hours), 200


@bp.route("/restaurants/current/<restaurant_id>/menus/")
@bp.route("/restaurants/custom/<restaurant_id>/<datetime_value>/menus/")
def restaurant_menus(restaurant_id, datetime_value=datetime.now()):
    menus = mongodb.retrieve_menus_by_datetime(restaurant_id, datetime_value)
    assigned_menu_items = RoutesUtil.assign_menu_items(menus)
    return render_template("menu-dialog.html",
                           menus=menus,
                           main_menu_items=assigned_menu_items[MAIN_MENU_ITEMS_INDEX],
                           drinks_menu_items=assigned_menu_items[DRINKS_MENU_ITEMS_INDEX],
                           sides_menu_items=assigned_menu_items[SIDES_MENU_ITEMS_INDEX]), 200


@bp.route("/restaurants/<restaurant_id>/<people_queueing>")
def restaurant_average_wait_time(restaurant_id, people_queueing):
    try:
        queue_time = mongodb.calc_wait_time(restaurant_id, int(people_queueing))
        return render_template("queue-time-info.html",
                               restaurant_id=restaurant_id,
                               people_queueing=people_queueing,
                               queue_time=queue_time), 200
    except InvalidId as e:
        print(e, file=sys.stderr)
        abort(404)

