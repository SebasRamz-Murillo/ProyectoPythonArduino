from interSensores import sensoresContr
import time
from Senso import Sensores
from JSON_Handle import JSON_Handle
import os
from interBD import interBD
from Mongo import Mongo
import threading


class main:
    def __init__(self):
        self.disp = sensoresContr() #pide datos pero no se
        self.sensores = Sensores()
        self.bandera = 0
        self.dispositivo=""
        self.mongo=Mongo()
        self.obj=Mongo()
        self.bandera=""

    def contador(self, tiempo):
        for i in range(tiempo, -1, -1):
            print(i)
            time.sleep(1)
        return True

    def lectura(self):
        print("Lectura de sensores")
        if self.bandera2==1: #si esta en conexion
            print("Conexion")
            lista=self.sensores.mostrar()
            if len(lista)>=1: #si la lista de sensores tiene objetos, debe ingresarlos a la bd antes de los otros
                print("Historial no actualizado encontrado")
                self.obj.insert_many("Sensores",lista)
                self.sensores.borrarInfo("Sensores.json")
            print("Empezando..")
            contador_thread = threading.Thread(target=self.contador, args=(30,))
            contador_thread.start()
            while contador_thread.is_alive(): #tiempo en segundos
                #descomenta estas lineas para hacerlo controlable con espacio
                # user_input = input()
                # # if user_input == " ":
                # #     break
                sens, val = self.disp.lectura()
                nombre, id = self.disp.nom.filter("clave", sens)
                sensor = Sensores(nombre[0]['nombre'], val)
                self.sensores.agregar(sensor.to_dict())
                # print(nombre[0]['nombre'])
                if self.obj.insert_one("Sensores",sensor.to_dict()) is False: #si no se inserto, debe cambiar la bandera
                    self.bandera2=2
                    print("Se perdio la conexion, guardando solo localmente")
                    ultimoSensor=sensor.to_dict() #guarda la lecutra donde sucede la desconexion
                    self.sensores.borrarInfo("Sensores.json")#borra datos para no repetirlos
                    self.sensores.agregar(ultimoSensor)
                    return self.lectura()#debe regresar al metodo para empezar a guardar solo local
            self.sensores.borrarInfo("Sensores.json")            #despues del que se cumpla el tiempo, borra los datos
            return self.lectura()
        else: #guarda solo local
            while True:
                print("Escritura..")
                user_input = input()
                if user_input == " ":
                    break
                sens, val = self.disp.lectura()
                nombre, id = self.disp.nom.filter("clave", sens)
                sensor = Sensores(nombre[0]['nombre'], val)
                self.sensores.agregar(sensor.to_dict())
                # print(nombre[0]['nombre'])


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
