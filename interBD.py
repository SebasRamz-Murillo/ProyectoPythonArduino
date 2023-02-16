from Mongo import Mongo


class interBD:
    def __init__(self):
        self.mong = Mongo()

    def conectarABd(self):
        print("------Conexion a MongoDB------")
        print("1. Ingresar por url")
        print("2. Ingresar por datos")
        opci = input("Seleccione una opcion: ")
        if opci == "2":
            print("Inserte los datos de conexion")
            user = input("Usuario: ")
            contra = input("Contraseña: ")
            clus = input("Cluster: ")
            token = input("Toke: ")
            op = input("Desea nombrar la bd?(Nombre predeterminado: VentasRamirez): y/n   ")
            if op == "y":
                nomBd = input("Nombre de la bd:")
                bd = nomBd
            else:
                bd = "SensoresEquipo"
            mongoBD = Mongo(user=user, contra=contra, cluster=clus, token=token, bd=bd)
        elif opci == "1":
            print("Inserte la url de conexion")
            url = input("Url: ")
            op = input("Desea nombrar la bd?(Nombre predeterminado: VentasRamirez): y/n   ")
            if op == "y":
                nomBd = input("Nombre de la bd:")
                bd = nomBd
            else:
                bd = "VentasRamirez"
            mongoBD = Mongo(url=url,
                            bd=bd)
        self.mong.agregar(mongoBD.to_dict())

    def actualizarConexion(self):
        print("Que conexion quiere modifiar?")
        id, info = self.seleccionarConexion()
        print(f"Conexion a modificar: #{id + 1}")
        print(f"User: {info.user}")
        print(f"Token: {info.token}")
        print(f"Cluster: {info.cluster}")
        print(f"Bd: ${info.bd}")
        print("Ingrese los datos nuevos: ")
        contra = input("Confirmar contraseña: ")
        if contra == info.contra:
            user = input("Inserte el usuario")
            token = input("Inserte el token")
            cluster = input("Inserte el cluster")
            bd = input("Inserte el nombre de la bd")
            op = input("Desea cambiar la contraseña?")
            if op == "y":
                contra = input("Nueva contraseña: ")
            conexionNueva = Mongo(user=user, contra=contra, cluster=cluster, token=token, bd=bd)
            self.mong.actualizar(id, conexionNueva.to_dict())
        else:
            print("Contraseña incorrecta")

    def borrarConexion(self):
        print("Que conexion quiere eliminar?")
        id, info = self.seleccionarConexion()
        print(f"Conexion a modificar: #{id + 1}")
        print(f"User: {info.user}")
        print(f"Token: {info.token}")
        print(f"Cluster: {info.cluster}")
        print(f"Bd: ${info.bd}")
        print("Ingrese los datos nuevos: ")
        contra = input("Confirmar contraseña: ")
        if contra == info.contra:
            self.mong.eliminar(id)
        else:
            print("Contraseña incorrecta")

    def mostrarConexiones(self):
        conexiones_data = self.mong.from_json()
        print("{:<1} {:<20} {:<20} {:<20} {:<20}".format("#", "User", "Cluster", "BD", "Status"))
        i = 0
        for conexion in conexiones_data:
            i = i + 1
            print("{:<1} {:<20} {:<20} {:<20} {:<20}".format(i, conexion.user, conexion.cluster, conexion.bd,
                                                             conexion.getStatus()))
        return len(conexiones_data), conexiones_data

    def mostrarConexionesConectadas(self):
        conexiones_data = self.mong.from_json()
        print("{:<1} {:<20} {:<20} {:<20} {:<20}".format("#", "User", "Cluster", "BD", "Status"))
        i = 0
        j = 0
        x = []
        for conexion in conexiones_data:
            i = i + 1
            status = conexion.getStatus()
            if conexion.getStatus() == "Conectado":
                x.append(i - 1)
                j = j + 1
                print(
                    "{:<1} {:<20} {:<20} {:<20} {:<20}".format(j, conexion.user, conexion.cluster, conexion.bd, status))
        return len(conexiones_data), conexiones_data, x

    def checkarConexionEnUso(self):
        if self.mong.filter("stat", 1):
            conexAc, id = self.mong.filter("stat", 1)
            check = Mongo(url=conexAc[0]['url'], bd=conexAc[0]['bd'], stat=1)
            bandera = check.getStatus()
            return check, bandera, True

    def seleccionarConexionesConectadas(self):
        tam, data, x = self.mostrarConexionesConectadas()
        seleccion = input("Seleccione una conexion ingresando el número correspondiente: ")
        try:
            seleccion = int(seleccion)
            if seleccion > 0 and seleccion <= tam:
                seleccion = seleccion - 1

                return x[seleccion], data[seleccion]
            else:
                print("Opción inválida, intente de nuevo.")
                return interBD.seleccionar_producto()
        except ValueError:
            print("Opción inválida, intente de nuevo.")
            return interBD.seleccionar_producto()

    def seleccionarConexion(self):  # devuelve id y objeto
        tam, data = self.mostrarConexiones()
        seleccion = input("Seleccione una conexion ingresando el número correspondiente: ")
        try:
            seleccion = int(seleccion)
            if seleccion > 0 and seleccion <= tam:
                seleccion = seleccion - 1
                return seleccion, data[seleccion]
            else:
                print("Opción inválida, intente de nuevo.")
                return interBD.seleccionar_producto()
        except ValueError:
            print("Opción inválida, intente de nuevo.")
            return interBD.seleccionar_producto()

    def selecConexionActual(self):
        if self.mong.filter("stat", 1):
            conexAc, id = self.mong.filter("stat", 1)
            print("Ya esta una conexion en uso")
            print(f"Datos de conexion: {conexAc[0]['user']}-{conexAc[0]['cluster']}-{conexAc[0]['bd']}")
            print("Url de conexion:")
            print(conexAc[0]['url'])
            print("Desea cambiar la conexion utilizada?")
            op = input("y/n")
            if op == "y":
                conexionNueva = Mongo(url=conexAc[0]['url'], bd=conexAc[0]['bd'], stat=0)
                self.mong.actualizar(id, conexionNueva.to_dict())
                self.selecConexionActual()
            else:
                self.mainBd()
        else:
            print("Seleccione la conexion a usar")
            id, info = self.seleccionarConexionesConectadas()
            conexionCambiada = Mongo(url=info.url, bd=info.bd, stat=1)
            self.mong.actualizar(id, conexionCambiada.to_dict())

    def sinConexion(self):
        conexAc, id = self.mong.filter("stat", 1)
        conexionNueva = Mongo(url=conexAc[0]['url'], bd=conexAc[0]['bd'], stat=0)
        self.mong.actualizar(id, conexionNueva.to_dict())

    def menuBd(self):
        if self.checkarConexionEnUso():
            obj, bandera, bool = self.checkarConexionEnUso()
            print(f"Datos de conexion: {obj.user}-{obj.cluster}-{obj.bd}------")
            print(f"Estado: {bandera}")
        else:
            print("No hay conexion activa")
        print("1. Agregar conexion a mongo bd")
        print("2. Sin conexion")
        print("3. Seleccionar conexion")
        print("4. Actualizar datos de conexion")
        print("5. Borrar conexion")
        print("6. Ver datos de conexion")
        print("7. Regresar")
        print("------------------------------------")
        opcion = input("Selection una opción: ")
        return opcion

    def mainBd(self):

        opcion = ""
        while opcion != "7":
            opcion = self.menuBd()
            if opcion == "1":
                self.conectarABd()
                input("Presione Enter para continuar...")
            elif opcion == "2":
                self.sinConexion()
                input("Presione Enter para continuar...")
            elif opcion == "3":
                self.selecConexionActual()
                input("Presione Enter para continuar...")
            elif opcion == "4":
                print(self.actualizarConexion())
                input("Presione Enter para continuar...")
            elif opcion == "5":

                input("Presione Enter para continuar...")
            elif opcion == "6":
                self.mostrarConexiones()
                input("Presione Enter para continuar...")
            elif opcion == "7":
                print("Saliendo del sistema...")
                return 1
                break
            else:
                print("Opción inválida, intente de nuevo.")
                input("Presione Enter para continuar...")


if __name__ == "__main__":
    interBD().mainBd()

    # mongodb+srv://admin:root@cluster0.hcy4jnm.mongodb.net/?retryWrites=true&w=majority
    # mongodb+srv://pablo:1010@cluster0.qfgfj6v.mongodb.net/?retryWrites=true&w=majority

    # mongodb+srv://pablaao:1010@cluster0.qfgfj6v.mongodb.net/?retryWrites=true&w=majority
