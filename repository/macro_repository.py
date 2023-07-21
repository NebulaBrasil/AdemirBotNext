from http.client import NOT_FOUND
import re
import bson
from pymongo.collection import Collection
from database import get_database
from repository.base_repository import BaseRepository
from entities.macro_entity import Macro

class MacroRepository(BaseRepository):
    def __init__(self):
        super().__init__("macros")

    def get_macro_by_id(self, macro_id):
        return self.collection.find_one({"_id": macro_id})
    
    def get_macro_by_title(self, title: str):
        regex_pattern = re.compile(f'^{re.escape(title)}$', re.IGNORECASE)
        macro_data = self.collection.find_one({"title": {"$regex": regex_pattern}})
        if macro_data:
            return Macro(macro_data["guild_id"], macro_data["title"], macro_data["text"])
        return None

    def create_macro(self, macro_data: Macro):
        return self.collection.insert_one(macro_data.to_dict())

    def update_macro(self, macro_id, macro_data: Macro):
        return self.collection.update_one({"_id": macro_id}, {"$set": macro_data.to_dict()})

    def delete_macro(self, macro_id):
        return self.collection.delete_one({"_id": macro_id})