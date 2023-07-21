import uuid

class Macro(object):
    def __init__(self, guild_id, title, text):
        self.macro_id = uuid.uuid4()
        self.guild_id = guild_id
        self.title = title
        self.text = text

    def __repr__(self):
        return f"Macro(macro_id={self.macro_id}, guild_id={self.guild_id}, nome={self.title}, mensagem={self.text})"
    
    def to_dict(self):
        return {
            "macro_id": self.macro_id,
            "guild_id": self.guild_id,
            "title": self.title,
            "text": self.text
        }
