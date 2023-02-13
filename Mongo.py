from Lista import Lista
from conecMongo import MongoConexion


class Mongo(Lista, MongoConexion):
    def __init__(self, *args, **kwargs):
        self.stat = kwargs.get('stat', 0)
        if 'url' in kwargs:
            self.url = kwargs.get('url', '')
            self.parse_url(self.url)
            self.bd = kwargs.get('bd', '')
        else:
            self.user = kwargs.get('user', '')
            self.contra = kwargs.get('contra', '')
            self.cluster = kwargs.get('cluster', '')
            self.token = kwargs.get('token', '')
            self.bd = kwargs.get('bd', '')
            self.url = f"mongodb+srv://{self.user}:{self.contra}@{self.cluster}.{self.token}.mongodb.net/?retryWrites=true&w=majority"
        super().__init__("Mongo.json")
        MongoConexion.__init__(self, self.url, self.bd, self.cluster)


    def parse_url(self, url):
        url_parts = url.split('://')
        self.protocol = url_parts[0]

        user_parts = url_parts[1].split(':')
        self.user = user_parts[0]

        contra_parts = user_parts[1].split('@')
        self.contra = contra_parts[0]

        cluster_parts = contra_parts[1].split('.')
        self.cluster = cluster_parts[0]
        self.token = cluster_parts[1]

    def __str__(self):
        return f"{self.user},{self.contra},{self.cluster},{self.token},{self.bd},{self.url},{self.stat}"

    def to_dict(self):
        listaDicc = []
        if type(self) == list:
            for item in self:
                if type(item) == dict:
                    listaDicc.append(item)
                else:
                    listaDicc.append(item.to_dict())
            return listaDicc
        elif type(self) == dict:
            listaDicc.append(self.listas)
        else:
            diccionario = {"user": self.user, "contra": self.contra, "cluster": self.cluster, "token": self.token,
                           "bd": self.bd, "url": self.url,"stat": self.stat}
            listaDicc.append(diccionario)
            return diccionario

    def from_json(self):
        mongo_json = self.json.leer_de_json()
        mongo_obj = []
        for mon in mongo_json:
            cli = Mongo(user=mon["user"], contra=mon["contra"], cluster=mon["cluster"], token=mon["token"], bd=mon["bd"], url=mon["url"], stat=mon["stat"])
            mongo_obj.append(cli)
        return mongo_obj


if __name__ == "__main__":
    # mong = Mongo()
    # for conexion in mong.from_json():
    #     print(conexion)

    mongo1 = Mongo(url="mongodb+srv://pablaao:1010@cluster0.qfgfj6v.mongodb.net/?retryWrites=true&w=majority",bd="VentasRamirez")
    # mongo2 = Mongo(user="admin", contra="root", cluster="cluster0", token="hcy4jnm", bd="VentasRamirez")
    print(mongo1.getStatus())
    # mongo1.conect()
    # mongo2.conect()
    # mong.agregar(mongo1.to_dict())
    # data={'nombre': "paaaaaaassssaaaaa"}
    # mongo1.insert_one("Personas",data)
    # mongo2.insert_one("Personas",data)
