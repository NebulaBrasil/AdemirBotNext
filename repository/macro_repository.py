import re
from uuid import uuid4
from bson.binary import Binary
from database import get_database
from repository.base_repository import BaseRepository
from entities.macro_entity import Macro

class MacroRepository(BaseRepository):
    def __init__(self):
        super().__init__("macros")

    def get_macro_by_id(self, macro_id):
        return self.collection.find_one({"_id": macro_id})
    
    def get_macro_by_title_and_guild_id(self, title: str, guild_id):
        ignore_case = re.compile(f'^{re.escape(title)}$', re.IGNORECASE)
        cursor = self.collection.find_one({"title": {"$regex": ignore_case}, "guild_id": str(guild_id)})
        if cursor:
            return Macro(guild_id=cursor["guild_id"], title=cursor["title"], text=cursor["text"], macro_id=cursor["_id"])
        return None

    def create_macro(self, macro_data: Macro):
        return self.collection.insert_one(macro_data.to_dict())

    def update_macro(self, macro_id, macro_data: Macro):
        return self.collection.update_one({"_id": macro_id}, {"$set": macro_data.to_dict()})

    def delete_macro(self, macro_id):
        return self.collection.delete_one({"_id": macro_id})
    
    def find_all(self, guild_id: int):
        cursor = self.collection.find({"guild_id": str(guild_id)})
        all_macros = list(Macro(**macro) for macro in cursor)
        return all_macros