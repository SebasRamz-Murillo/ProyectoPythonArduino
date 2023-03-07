from Lista import Lista

#clave = nombre que viene desde arduino
#nombre= nombre que el usuario da
#valor = pos el valor que tiene el sensor

class ultimaLectura(Lista):
    def __init__(self,clave="", nombre="", valor="", tipo=""):
        super().__init__("lecturaSensores.json")
        self.nombre=nombre
        self.clave=clave
        self.tipo=tipo
        self.valor=valor

    def __str__(self):
        return f"{self.clave},{self.nombre},{self.tipo}"

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
            if self.nombre=="":
                self.nombre=self.clave
            diccionario = {"clave":self.clave, "nombre": self.nombre,"valor":self.valor, "tipo":self.tipo}
            listaDicc.append(diccionario)
            return diccionario

    def from_json(self):
        sensor_json = self.json.leer_de_json()
        sensor_obj = []
        for sensor in sensor_json:
            cli = Nombres(sensor["clave"], sensor["nombre"], sensor["valor"], sensor["tipo"])
            sensor_obj.append(cli)
        return sensor_obj
