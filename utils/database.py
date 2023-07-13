# database.py
import pymongo
import config

# Função para conectar ao MongoDB
def connect_to_database():
    client = pymongo.MongoClient(config.MONGO_URI)
    database = client[config.DATABASE_NAME]
    return database

# Exemplo de função para inserir um documento na coleção
def insert_document(document):
    collection = connect_to_database()
    result = collection.insert_one(document)
    return result.inserted_id

# Exemplo de função para buscar documentos na coleção
def find_documents(query):
    collection = connect_to_database()
    documents = collection.find(query)
    return list(documents)