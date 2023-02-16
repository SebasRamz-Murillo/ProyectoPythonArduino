import os

import serial
import time
from Senso import Sensores
from SensoNom import Nombres


class sensoresContr:
    def __init__(self):
        self.sens = Sensores()
        self.nom = Nombres()
        self.puerto = "COM3"
        self.baud = 9600
        self.ser = serial.Serial(self.puerto, int(self.baud))
        self.ser.flushInput()
        self.sensDef()

    def error(self):
        print("Se desconecto dispositivo del puerto COM")

    def main(self):
        self.sensDef()

    def nombrarSens(self):
        sensores = self.nom.from_json()
        print("Sensores detectados:")
        print("{:<1} {:<20} | {:<20} {:<20} | ".format("#", "Clave", "Sensor", "Tipo"))
        i = 0
        for sensor in sensores:
            i = i + 1
            print("{:<1} {:<20} | {:<20} {:<20} | ".format(i, sensor.clave, sensor.nombre, sensor.tipo))
        seleccion = input("Seleccione un sensor con el id: ")
        seleccion = int(seleccion)
        nuevoNom = input("Nombre del sensor: ")
        nuevo = Nombres(sensores[seleccion - 1].clave, nuevoNom, sensores[seleccion - 1].tipo)
        self.nom.actualizar(seleccion - 1, nuevo.to_dict())

    def sensDef(self):
        sensores = []
        j = 0
        while True:
            try:
                data = self.ser.readline().decode().strip()
            except serial.SerialException as e:
                sensoresContr.error()
            else:
                values = data.split(':')
                if len(sensores) > 0:
                    if values[0] == sensores[0]:
                        break
                sensores.append(values[0])
                time.sleep(.2)
        for sens in sensores:
            j = j + 1
            if sens.startswith("ult"):
                tipo = "Ultrasonico"
            elif sens.startswith("tmp"):
                tipo = "Temperatura"
            elif sens.startswith("hum"):
                tipo = "Humedad"
            elif sens.startswith("bat"):
                tipo = "Bateria"
            elif sens.startswith("nva"):
                tipo = "Nivel de agua"
            elif sens.startswith("pes"):
                tipo = "Peso"
            else:
                tipo = "No definido"
            x = self.nom.filter("clave", sens)
            if x is None:
                # no existia
                self.nom.agregar(Nombres(sens, "", tipo).to_dict())

    def verTipo(self):
        sensores = self.nom.from_json()
        print("Tipos de sensores detectados:")
        print("{:<1} {:<20} ".format("#", "Tipo"))
        i = 0
        for sensor in sensores:
            i = i + 1
            print("{:<1} {:<20} ".format(i, sensor.tipo))

    def lectura(self):
        while True:
            try:
                data = self.ser.readline().decode().strip()
            except serial.SerialException as e:
                sensoresContr.error()
            else:
                values = data.split(':')
                # se = Sensores(values[0],"", values[1])
                return values[0], values[1]
                time.sleep(1)

    def menuSensores(self):
        print(f"------Puerto: {self.puerto}------")
        print("1. Nombrar sensor")
        print("2. Ver tipos de sensores")
        print("3. Regresar")
        print("------------------------------------")
        opcion = input("Seleccione una opción: ")
        return opcion

    def mainSensores(self):
        opcion = ""
        while opcion != "3":
            opcion = self.menuSensores()
            if opcion == "1":
                self.nombrarSens()
                input("Presione Enter para continuar...")
            elif opcion == "2":
                self.nombrarSens()
                input("Presione Enter para continuar...")
            elif opcion == "3":
                print("Saliendo del sistema...")
                return 1
                break
            else:
                print("Opción inválida, intente de nuevo.")
                input("Presione Enter para continuar...")


if __name__ == "__main__":
    sen = sensoresContr("COM3", 9600).mainSensores()

# if len(values) == 2:
#     sensor_name, sensor_value = values
#     if sensor_name == 'sens1':
#         sensor_name = 'ultrasonic'
#     elif sensor_name == 'sens2':
#         sensor_name = 'temperature'
#     print(f'{sensor_name}: {sensor_value}')
