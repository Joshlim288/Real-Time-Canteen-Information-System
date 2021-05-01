from datetime import datetime

from bson import ObjectId

from main.app import DB


class Menu(object):

    def __init__(self, _id, restaurant_id, name, description, start_datetime, end_datetime, day_of_week,
                 weekly_recurring, average_waiting_time, menu_type):
        """
        Menu object model.

        Args:
            _id (ObjectId):
            restaurant_id (ObjectId):
            name (str):
            description (str):
            start_datetime (datetime):
            end_datetime (datetime):
            day_of_week (list):
            weekly_recurring (bool):
            average_waiting_time (int):
            menu_type (int):
        """
        self._id = _id
        self.restaurant_id = restaurant_id
        self.name = name
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.day_of_week = day_of_week
        self.weekly_recurring = weekly_recurring
        self.average_waiting_time = average_waiting_time
        self.menu_type = menu_type

    def insert(self):
        if not DB.find_one(DB.MENU_COLLECTION_NAME, {"_id": self._id}):
            DB.insert(collection=DB.MENU_COLLECTION_NAME, data=self.json())

    def json(self):
        """
        Transforms python Menu object into json.

        Returns:
            JSON object/Python dictionary.
        """
        return {
            "_id": self._id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "description": self.description,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "day_of_week": self.day_of_week,
            "weekly_recurring": self.weekly_recurring,
            "average_waiting_time": self.average_waiting_time,
            "menu_type": self.menu_type
        }
