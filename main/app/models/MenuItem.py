from bson import ObjectId

from main.app import DB


class MenuItem(object):

    def __int__(self, _id, menu_id, name, price, image, type):
        """
        Menu item model object.

        Args:
            _id (ObjectId):
            menu_id (ObjectId):
            name (str):
            price (float):
            image (str):
            type (int):
        """
        self._id = _id
        self.menu_id = menu_id
        self.name = name
        self.price = price
        self.image = image
        self.type = type

    def insert(self):
        if not DB.find_one(DB.MENU_ITEM_COLLECTION_NAME, {"_id": self._id}):
            DB.insert(collection=DB.MENU_ITEM_COLLECTION_NAME, data=self.json())

    def json(self):
        """
        Transforms python MenuItem object into json.

        Returns:
            JSON object/Python dictionary.

        """
        return {
            "_id": self._id,
            "menu_id": self.menu_id,
            "name": self.name,
            "price": self.price,
            "image": self.image,
            "type": self.type,
        }
