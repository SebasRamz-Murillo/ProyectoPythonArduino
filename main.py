from interSensores import sensoresContr
import time
from Senso import Sensores
from JSON_Handle import JSON_Handle
import os
from interBD import interBD
from Mongo import Mongo


class main:
    def __init__(self):
        self.disp = sensoresContr() #pide datos pero no se
        self.sensores = Sensores()
        self.tiempo = 0
        self.tiempoMax = 5
        self.bandera = 0
        self.dispositivo=""
        self.mongo=Mongo()
        self.obj=Mongo()
        self.bandera=""



    def lectura(self):
        print("Lectura de sensores")
        print(self.bandera2)
        if self.bandera2==1: #si esta en conexion
            tiempo = time.time()
            print("Conexion")
            if self.sensores.mostrar() > 1:
                pass

            while True:
                #descomenta estas lineas para hacerlo controlable con espacio
                # user_input = input()
                # # if user_input == " ":
                # #     break

                sens, val = self.disp.lectura()
                nombre, id = self.disp.nom.filter("clave", sens)
                sensor = Sensores(nombre[0]['nombre'], val)
                self.sensores.agregar(sensor.to_dict())
                print(nombre[0]['nombre'])
                if self.obj.insert_one("Sensores",sensor.to_dict()) is False:
                    self.bandera2==2
                    print("Se perdio la conexion, guardando solo localmente")
                    self.sensores.borrarInfo("Sensores.json")
                    self.lectura()
            # self.sensores.borrarInfo("Sensores.json")
        else:
            while True:
                # user_input = input()
                # if user_input == " ":
                #     break
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
        resultado = interBD().checkarConexionEnUso()
        if resultado:
            self.bandera2 = 1
            self.obj=resultado[0]
            self.obj.conect()
            self.bandera=resultado[1]
            print(f"Datos de conexion: {self.obj.user}-{self.obj.cluster}-{self.obj.bd}------")
            print(f"Estado: {self.bandera}")

        else:
            self.bandera2 = 2
            print("No hay conexion activa")
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
