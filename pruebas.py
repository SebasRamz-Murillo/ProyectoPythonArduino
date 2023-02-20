import time
import threading


class prueba:

    def contador(self, tiempo):
        for i in range(tiempo, -1, -1):
            print(i)
            time.sleep(1)
        return True

    def prueba(self,):
        contador_thread = threading.Thread(target=self.contador, args=(30,))
        contador_thread.start()
        while contador_thread.is_alive():
            print("Pasando")
        print("Termino")


if __name__ == "__main__":
    prueba().prueba()