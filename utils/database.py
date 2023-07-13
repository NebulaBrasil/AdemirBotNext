# database.py
import pymongo

# Configurações do MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "nome_do_banco_de_dados"
COLLECTION_NAME = "nome_da_colecao"

# Função para conectar ao MongoDB
def connect_to_database():
    client = pymongo.MongoClient(MONGO_URI)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]
    return collection

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