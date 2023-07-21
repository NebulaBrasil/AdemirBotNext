import uuid

class Macro(object):
    def __init__(self, macro_id, guild_id, title, text):
        self.macro_id = macro_id,
        self.guild_id = guild_id,
        self.title = title,
        self.text = text

      
    def to_dict(self):
        return {
            "macro_id": self.macro_id,
            "guild_id": self.guild_id,
            "title": self.title,
            "text": self.text
        }
