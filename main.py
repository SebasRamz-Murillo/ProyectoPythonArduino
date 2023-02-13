from interSensores import sensoresContr
import time
from Senso import Sensores
from JSON_Handle import JSON_Handle
import os
from interBD import interBD


class main:
    def __init__(self):
        self.disp = sensoresContr() #pide datos pero no se
        self.sensores = Sensores()
        self.tiempo = 0
        self.tiempoMax = 5
        self.bandera = 0


    def lectura(self):
        tiempo = time.time()
        if self.bandera==2:
            pass
            # if interBD().checkarConexionEnUso():  # si da
            #     obj, bandera, bool = interBD().checkarConexionEnUso()
            #     obj
            # while time.time() < tiempo + self.tiempoMax:
            #     user_input = input()
            #     if user_input == " ":
            #         break
            #     sens, val = self.disp.lectura()
            #     nombre, id = self.disp.nom.filter("clave", sens)
            #     sensor = Sensores(nombre[0]['nombre'], val)
            #     self.sensores.agregar(sensor.to_dict())
            #     print(nombre[0]['nombre'])
            #     # if obj.insertOne
            # self.json.clearFille(self.sensores.archivo)
        else:
            while True:
                user_input = input()
                if user_input == " ":
                    break
                sens, val = self.disp.lectura()
                nombre, id = self.disp.nom.filter("clave", sens)
                sensor = Sensores(nombre[0]['nombre'], val)
                self.sensores.agregar(sensor.to_dict())
                print(nombre[0]['nombre'])


    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def menuGeneral(self):
        self.clear()
        print("------------------------------------")
        print("Sistema de gestión de dispositivos arduinos")
        # if interBD().checkarConexionEnUso():
        #     self.bandera = 1
        #     obj, bandera, bool = interBD().checkarConexionEnUso()
        #     print(f"Datos de conexion: {obj.user}-{obj.cluster}-{obj.bd}------")
        #     print(f"Estado: {bandera}")
        # else:
        #     self.bandera = 2
        #     print("No hay conexion activa")
        self.bandera = 2
        print(f"----Puerto: {self.disp.puerto}-----")
        print("1. Configurar sensores")
        print("2. Conexiones")
        print("3. Lectura de sensores")
        print("4. Salir")
        print("------------------------------------")
        opcion = input("Seleccione una opción: ")
        return opcion


    def main(self):
        opcion = ""
        
        while opcion != "0":
            opcion = self.menuGeneral()
            if opcion == "1":
                self.disp.mainSensores()
            elif opcion == "2":
                interBD().mainBd()
            elif opcion == "3":
                self.lectura()
            elif opcion == "p":
                contra = input("Contra:")
                if contra == "1234":
                    JSON_Handle().clear_all_files()
                else:
                    return main()
            elif opcion == "0":
                # Salir
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida, intente de nuevo.")
                input("Presione Enter para continuar...")


if __name__ == "__main__":
    main().main()
