from Lista import Lista


# clave = nombre que viene desde arduino
# nombre= nombre que el usuario da
# valor = pos el valor que tiene el sensor
class Sensores(Lista):
    def __init__(self, nombre="", valor=""):
        self.archivo = "Sensores.json"
        super().__init__(self.archivo)
        self.nombre = nombre
        self.valor = valor

    def __str__(self):
        return f"{self.nombre},{self.valor}"

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

            diccionario = {"nombre": self.nombre, "valor": self.valor}
            listaDicc.append(diccionario)
            return diccionario

    def from_json(self):
        sensor_json = self.json.leer_de_json()
        sensor_obj = []
        for sensor in sensor_json:
            cli = Sensores(sensor["nombre"], sensor["valor"])
            sensor_obj.append(cli)
        return sensor_obj


if __name__ == "__main__":
    sns = Sensores("", "sens2", 21)
    print(sns.to_dict())
