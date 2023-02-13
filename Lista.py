from JSON_Handle import JSON_Handle


class Lista:
    def __init__(self, ruta):
        self.json = JSON_Handle(ruta)
        self.listas = self.json.leer_de_json()  # load data from json file when class is instantiated

    def agregar(self, datos):
        self.listas.append(datos)
        self.json.guardar_a_json(self.listas)

    def mostrar(self):
        return self.listas

    def actualizar(self, cli, datos):
        if self.listas:
            self.listas[int(cli)] = datos
            self.json.guardar_a_json(self.listas)

    def eliminar(self, cli):
        self.listas.pop(int(cli))
        self.json.guardar_a_json(self.listas)

    def buscar(self, cli):
        return self.listas[int(cli)]

    def sort(self, key=None, reverse=False):
        self.listas.sort(key=key, reverse=reverse)
        self.json.guardar_a_json(self.listas)

    def filter(self, key, value):
        filtered_list = [item for item in self.listas if item[key] == value]
        if filtered_list:
            id = self.listas.index(filtered_list[0])
            return filtered_list, id
        else:
            return None

    def paginate(self, page_size, page_number):
        start = (page_number - 1) * page_size
        end = start + page_size
        return self.listas[start:end]
