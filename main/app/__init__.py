import math
import sys
from datetime import datetime

from bson.errors import InvalidId
from flask import Flask, request, redirect
from flask import render_template
from werkzeug.exceptions import NotFound, abort

from main.app.core import mongodb
from main.app.database import DB

BURGER_STATEMENT = "Here's a burger for you to look at while you wonder if you " \
                           "should click on the button below to be redirected to our homepage."


def make_error_page(error_code, title, description="There's an error."):
    """
    Function renders error page.

    Args:
        error_code(int): Http error code
        title(str): Name of error
        description(str): Text describing the error.

    Returns:
        Error HTML page

    """
    return render_template("errors/error.html",
                           error_code=error_code,
                           title=title,
                           description=description)


def retrieve_paginated_available_restaurants(page_number=1, custom_datetime=datetime.now()):
    items_per_page = 6
    pagination_start_index = (page_number - 1) * items_per_page
    pagination_end_index = (page_number * items_per_page) - 1
    return mongodb.retrieve_available_restaurants(pagination_start_index, pagination_end_index, custom_datetime)


def app(config="main.app.config.development"):
    template_directory = "../app/views/templates"
    static_directory = "../app/views/static"
    flask_app = Flask(__name__,
                      instance_relative_config=True,
                      template_folder=template_directory,
                      static_folder=static_directory)

    # Set strict slash to False
    flask_app.url_map.strict_slashes = False

    # Load the configuration
    flask_app.config.from_object(config)

    @flask_app.before_request
    def clear_url_trailing():
        request_path = request.path
        if request_path != "/" and request_path.endswith("/"):
            return redirect(request_path[:-1])

    @flask_app.template_filter("format_datetime")
    def format_datetime(dt, fmt="%Y-%m-%dT%H:%M:%SZ"):
        if dt is None:
            return ""

        if type(dt) is str:
            new_dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
            return new_dt.strftime(fmt)
        else:
            return datetime.strftime(dt, "%Y-%m-%dT%H:%M:%SZ")

    @flask_app.template_filter("format_time")
    def format_time(tm, fmt):
        if tm is None:
            return ""

        if type(tm) is str:
            new_time = datetime.strptime(tm, "%H:%M:%S")

            if new_time.minute == 0:
                fmt = "%#I%p"

            return new_time.strftime(fmt)
        else:
            if tm.minute == 0:
                fmt = "%#I%p"

            return tm.strftime(fmt)

    @flask_app.template_filter("check_24hours_open")
    def check_24hours_open(start_time=datetime.now().time(),
                           end_time=datetime.now().time()):
        if start_time or end_time is None:
            return False

        return start_time == end_time

    @flask_app.template_filter("check_near_closing_time")
    def check_near_closing_time(start_time, end_time, hour_difference_check=1):
        if start_time or end_time is None:
            return False

        return start_time.hour > end_time.hour - hour_difference_check

    @flask_app.template_filter("current_day_index")
    def current_day_index():
        return datetime.now().isoweekday()

    @flask_app.template_filter("check_both_AMPM")
    def current_day_index(start_time, end_time):
        if start_time or end_time is None:
            return False

        mid_day = datetime.time(12)
        return mid_day < (start_time and end_time) < mid_day

    flask_app.config['TRAP_HTTP_EXCEPTIONS'] = True

    @flask_app.errorhandler(InvalidId)
    def invalid_id_handler(e):
        print(e, file=sys.stderr)
        return make_error_page(404, "The id value(s) used are invalid.", "It looks like what you are looking for "
                                                                              "does not exist in our database. " +
                               BURGER_STATEMENT)

    @flask_app.errorhandler(NotFound)
    def handle_not_found_error(e):
        print(e, file=sys.stderr)
        return make_error_page(404, "Page not found.", "The requested URL " + request.path +
                               " you're looking for was not found. We are sorry that you were sent on "
                               "a wild goose chase. " + BURGER_STATEMENT), 404

    @flask_app.route("/")
    @flask_app.route("/restaurants")
    @flask_app.route("/restaurants/<page_number>")
    def restaurants(page_number=1):
        # Retrieve currently available restaurants
        # Pass list of restaurants and size of list
        page_number = int(page_number)
        restaurant_dictionary = retrieve_paginated_available_restaurants(page_number=page_number)
        available_restaurants_count = restaurant_dictionary["restaurant_count"]

        # If URL called with page number exceeding max pages for current query, abort to Error 404.
        if page_number > math.ceil(available_restaurants_count / 6):
            abort(404)

        return render_template("landing.html",
                               page_number=page_number,
                               available_restaurants_count=available_restaurants_count,
                               restaurants=restaurant_dictionary["restaurants"]), 200

    # @flask_app.errorhandler(Exception)
    # def handle_error(e):
    #     print(e, file=sys.stderr)
    #     return make_error_page(500, "Error! Error! Error!", "Oops! Something went wrong. We are sorry that things "
    #                                                         "didn't work out between us." + BURGER_STATEMENT), 500

    # Initialize MongoDB
    db = DB.initialize()
    register_blueprints(flask_app)

    # Load the configuration from the instance folder
    # flask_app.config.from_pyfile("config.py")

    return flask_app


def register_blueprints(app):
    from main.app.core import bp as main_bp
    app.register_blueprint(main_bp)


if __name__ == "__main__":
    app = app()
    app.run()
