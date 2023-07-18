import uuid
from models.ademir_cfg import AdemirCfg
from repository.base_repository import BaseRepository

class AdemirCfgRepository(BaseRepository):
    def __init__(self):
        super().__init__('ademir_cfg')

    def set_guild_conversation_role(self: BaseRepository, guild_id: int, conv_role_id):
        cfg: AdemirCfg = self.collection.find_one({"GuildId": guild_id})
        if cfg is None:
            cfg = vars(AdemirCfg(
                AdemirConfigId = uuid.uuid4(),
                GuildId = guild_id,
                AdemirRoleId = conv_role_id
            ))
        else:
            cfg["AdemirRoleId"] = conv_role_id
        
        self.collection.replace_one({"GuildId": guild_id}, cfg, upsert=True)