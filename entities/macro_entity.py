import uuid

class Macro(object):
    def __init__(self, guild_id, title, text):
        self.macro_id = uuid.uuid4()
        self.guild_id = guild_id
        self.title = title
        self.text = text

      
    def to_dict(self):
        return {
            "macro_id": str(self.macro_id),
            "guild_id": str(self.guild_id),
            "title": self.title,
            "text": self.text
        }
