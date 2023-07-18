from pymongo.collection import Collection
from database import get_database

class BaseRepository:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
    
    def get_collection(self):
        return get_database().get_collection(self.collection_name)
        
    collection: Collection = property(get_collection)
    
    def get_all(self):
        return self.collection.find()

    def get_by_id(self, obj_id):
        return self.collection.find_one({'_id': obj_id})

    def create(self, obj_data):
        return self.collection.insert_one(obj_data)

    def update(self, obj_id, obj_data):
        return self.collection.update_one({'_id': obj_id}, {'$set': obj_data})

    def delete(self, obj_id):
        return self.collection.delete_one({'_id': obj_id})