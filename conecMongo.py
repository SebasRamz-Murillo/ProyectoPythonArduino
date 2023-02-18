import pymongo
from pymongo.server_api import ServerApi


class MongoConexion:
    def __init__(self, url, dbname, cluster):
        self.url = url
        self.dbname = dbname
        self.cluster=cluster
        self.client=None
        self.db=None
    def conect(self):
        self.client = pymongo.MongoClient(self.url, server_api=ServerApi('1'))
        try:
            self.client.server_info()
        except Exception as e:
            print("Error en datos")
        else:
            print(f"Conectado al cliente MongoDB {self.cluster}")
            print(f"Buscando bd {self.dbname}....")
            if self.dbname in self.client.list_database_names():
                self.db = self.client[self.dbname]
                print(f"Conectado a {self.dbname}")
            else:
                print(f"Base de datos no encontrada")
                print(f"Creando base de datos {self.dbname} ")
                self.db = self.client[self.dbname]
                print(f"Bd {self.dbname} creada y conectada")

    def getStatus(self):
        self.client = pymongo.MongoClient(self.url, server_api=ServerApi('1'))
        try:
            self.client.server_info()
        except Exception as e:
            return "Desconectado"
        else:
            return "Conectado"

    def getError(self):
        self.client = pymongo.MongoClient(self.url, server_api=ServerApi('1'))
        try:
            self.client.server_info()

        except Exception as e:
            pass
        else:
            return "Conectado"


    def insert_one(self, collection, data):
        coll = self.db[collection]
        coll.insert_one(data)
        if self.find_one(collection,data):
            return True
        else:
            return False

    def insert_many(self, collection, data_list):
        coll = self.db[collection]
        result = coll.insert_many(data_list)
        return result.acknowledged

    def find_one(self, collection, query={}):
        coll = self.db[collection]
        return coll.find_one(query)

    def find_many(self, collection, query={}):
        coll = self.db[collection]
        return coll.find(query)

    def update_one(self, collection, query, new_values):
        coll = self.db[collection]
        coll.update_one(query, {"$set": new_values})

    def delete_one(self, collection, query):
        coll = self.db[collection]
        coll.delete_one(query)

    def delete_many(self, collection, query):
        coll = self.db[collection]
        coll.delete_many(query)


if __name__ == "__main__":
    #mongodb+srv://admin:root@cluster0.hcy4jnm.mongodb.net/?retryWrites=true&w=majority

    mongo_object = MongoConexion("mongodb+srv://admin:root@cluster0.hcy4jnm.mongodb.net/?retryWrites=true&w=majority","Prueba","cluster0")
    datos={"codigo": "2333", "nombre": "214", "descripcion": "32", "precio": 23, "stat": 2}
    print(mongo_object.getStatus())
