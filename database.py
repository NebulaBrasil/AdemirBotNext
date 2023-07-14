import pymongo
import config

def connect_to_database():
    client = pymongo.MongoClient(config.MONGO_URI)
    database = client[config.DATABASE_NAME]
    return database

def obter_config_ademir(guildId):
    db = connect_to_database()
    result = db.ademir_cfg.find_one({"GuildId": guildId})
    return result