from interSensores import sensoresContr
import time
from Senso import Sensores
from JSON_Handle import JSON_Handle
import os
from interBD import interBD
from Mongo import Mongo
import threading
import keyboard
from ultimaLectura import ultimaLectura


class main:
    def __init__(self):
        self.disp = sensoresContr()  # pide datos pero no se
        self.sensores = Sensores()
        self.bandera = 0
        self.dispositivo = ""
        self.mongo = Mongo()
        self.obj = Mongo()
        self.bandera = ""
        self.flag = 0
        self.stop_event = threading.Event()
        self.ultLectura = ultimaLectura

        self.tiempoEspera = 60  # tiempo en segundos
        self.timer_count = 0  # contador de tiempo para borrar historial local

        self.veces = 2

    def contador(self, tiempo):
        for i in range(tiempo, -1, -1):
            time.sleep(1)
        return True

    def detectar_enter(self):
        self.enter_pressed = False
        keyboard.wait("enter")  # espera hasta que se presione Enter
        self.enter_pressed = True

    def lectura(self):
        print("Lectura de sensores")
        if self.bandera2 == 1:  # si esta en conexion
            print("Conexion")
            lista = self.sensores.mostrar()
            if len(lista) >= 1:  # si la lista de sensores tiene objetos, debe ingresarlos a la bd antes de los otros
                passo = 0
                for i in lista:
                    if self.obj.find_one("Sensores", i):
                        pass
                    else:
                        self.obj.insert_one("Sensores", i)
                        passo = 1
                if passo == 1:
                    self.sensores.borrarInfo("Sensores.json")
            print("Empezando..")
            enter_thread = threading.Thread(target=self.detectar_enter)
            enter_thread.start()
            while True:  # tiempo en segundos
                if enter_thread.is_alive():
                    pass
                else:
                    aux = self.sensores.mostrar()
                    if len(aux) >= 1:
                        ubi = len(aux) - 1
                        if self.obj.find_one("Sensores", aux[ubi]):
                            pass
                        else:
                            self.obj.insert_one("Sensores", aux[ubi])
                    print("Enter presionado, deteniendo lectura de sensores")
                    self.main()
                sens, val = self.disp.lectura()
                nombre, id = self.disp.nom.filter("clave", sens)
                sensor = Sensores(nombre[0]['nombre'], val)
                self.sensores.agregar(sensor.to_dict())
                print("|{:<25} {:<4}|".format(nombre[0]['nombre'], val))

                if self.obj.insert_one("Sensores",
                                       sensor.to_dict()) is False:  # si no se inserto, debe cambiar la bandera
                    self.bandera2 = 2
                    print("Se perdio la conexion, guardando solo localmente")
                    ultimoSensor = sensor.to_dict()  # guarda la lecutra donde sucede la desconexion
                    self.sensores.borrarInfo("Sensores.json")  # borra datos para no repetirlos
                    self.sensores.agregar(ultimoSensor)
                    self.lectura()  # debe regresar al metodo para empezar a guardar solo local

        else:  # guarda solo local
            enter_thread = threading.Thread(target=self.detectar_enter)
            enter_thread.start()
            while True:
                print("Escritura..")
                user_input = input()
                if user_input == " ":
                    break
                sens, val = self.disp.lectura()
                nombre, id = self.disp.nom.filter("clave", sens)
                sensor = Sensores(nombre[0]['nombre'], val)
                self.sensores.agregar(sensor.to_dict())
                self.ultLectura.agregar(sensor.to_dict())
                print("|{:<25} {:<4}|".format(nombre[0]['nombre'], val))

                if self.enter_pressed:  # si se ha detectado la pulsación de Enter, romper el ciclo
                    print("Enter presionado, deteniendo lectura de sensores")
                    return self.main()
                # print(nombre[0]['nombre'])

    def ultimaLectura(self):
        sensores = self.sensores.from_json()
        print("|{:<25} {:<5}|".format("Sensor", "Valor"))
        for sens in sensores:
            print("|{:<25} {:<5}|".format(sens.nombre, sens.valor))

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def menuGeneral(self):
        self.clear()
        print("----------------------------------------------")
        print("Sistema de gestión de dispositivos arduinos")
        if self.veces == 2:
            resultado = interBD().checkarConexionEnUso()
            if resultado:
                self.bandera2 = 1
                self.obj = resultado[0]
                self.obj.conect()
                self.bandera = resultado[1]
                print(f"Datos de conexion: {self.obj.user}-{self.obj.cluster}-{self.obj.bd}------")
                print(f"Estado: {self.bandera}")
                self.veces = 1

            else:
                self.bandera2 = 2
                self.veces = 1
                print("No hay conexion activa")
            self.hiloBorrarPTiempo()
        print(f"----Puerto: {self.disp.puerto}-----")
        print("1. Configurar sensores")
        print("2. Conexiones")
        print("3. Lectura de sensores")
        print("4. Lectura guardada")
        print("5. Salir")
        print("------------------------------------")
        opcion = input("Seleccione una opción: ")
        return opcion

    def hiloBorrarPTiempo(self):
        timer = threading.Timer(self.tiempoEspera, self.hiloBorrarPTiempo)
        timer.start()

        if self.bandera2 == 1:  # si esta en conexion
            self.timer_count += 1  # incrementa el contador de tiempo
            if self.timer_count >= self.tiempoEspera / 60:  # verifica si han pasado 15 minutos
                self.sensores.borrarInfo("Sensores.json")
                print("Se borro historial local")
                self.timer_count = 0  # resetea el contador de tiempo
        else:
            print("Se reinicio el contador")
            self.timer_count = 0

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
            elif opcion == "4":
                self.ultimaLectura()
                input("Presione Enter para continuar...")
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
