import pymongo
import config

def get_database():
    return pymongo.MongoClient(config.MONGO_URI, tls=True, tlsCertificateKeyFile=config.CERTIFICATE_FILE)[config.DATABASE_NAME]