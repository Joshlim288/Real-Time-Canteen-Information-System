from bson import ObjectId

from main.app import DB


class Restaurant(object):

    def __int__(self, _id, name, information, image):
        """
        Restaurant object model.

        Args:
            _id (ObjectId):
            name (str):
            information (str):
            image (str):
        """
        self._id = _id
        self.name = name
        self.information = information
        self.image = image

    def insert(self):
        """
        If Restaurant object does not exist in database, create with current
        restaurant instance data.

        Returns:

        """
        if not DB.find_one(DB.RESTAURANT_COLLECTION_NAME, {"_id": self._id}):
            DB.insert(collection=DB.RESTAURANT_COLLECTION_NAME, data=self.json())

    def json(self):
        """
        Transforms python Restaurant object into json.

        Returns:
            JSON object/Python dictionary.

        """
        return {
            "_id": self._id,
            "name": self.name,
            "information": self.information,
            "image": self.image
        }
