import math


class GestorAlmacenamiento:

    def __init__(
        self,
        bloques=64,
        tam_bloque=4,
        algoritmo="Contigua"
    ):
        self.total_bloques = bloques
        self.tam_bloque = tam_bloque
        self.algoritmo = algoritmo

        # None significa que el bloque está libre.
        self.disco = [None] * bloques

        # Guarda información de los archivos almacenados.
        self.archivos = {}

    # =====================================================
    # ASIGNACIÓN GENERAL
    # =====================================================

    def asignar(self, nombre, tam_archivo):
        """
        Ejecuta el algoritmo seleccionado.
        """

        if nombre in self.archivos:
            print(f"El archivo {nombre} ya existe.")
            return False

        if tam_archivo <= 0:
            print("El tamaño del archivo debe ser mayor que cero.")
            return False

        algoritmo = self.algoritmo.lower()

        if algoritmo == "contigua":
            return self.asignar_contigua(nombre, tam_archivo)

        elif algoritmo == "enlazada":
            return self.asignar_enlazada(nombre, tam_archivo)

        elif algoritmo == "indexada":
            return self.asignar_indexada(nombre, tam_archivo)

        else:
            print(f"Algoritmo desconocido: {self.algoritmo}")
            return False

    # =====================================================
    # ASIGNACIÓN CONTIGUA
    # =====================================================

    def asignar_contigua(self, nombre, tam_archivo):

        bloques_necesarios = math.ceil(
            tam_archivo / self.tam_bloque
        )

        inicio = -1
        contador = 0

        for i in range(self.total_bloques):

            if self.disco[i] is None:

                if inicio == -1:
                    inicio = i

                contador += 1

                if contador == bloques_necesarios:

                    bloques_asignados = list(
                        range(
                            inicio,
                            inicio + bloques_necesarios
                        )
                    )

                    for bloque in bloques_asignados:
                        self.disco[bloque] = nombre

                    self.archivos[nombre] = {
                        "metodo": "Contigua",
                        "tamano": tam_archivo,
                        "bloques": bloques_asignados,
                        "inicio": inicio
                    }

                    print(
                        f"{nombre} almacenado mediante asignación contigua."
                    )
                    print(
                        f"Bloques asignados: {bloques_asignados}"
                    )

                    return True

            else:
                inicio = -1
                contador = 0

        print(
            f"No existe espacio contiguo suficiente para {nombre}."
        )

        return False

    # =====================================================
    # ASIGNACIÓN ENLAZADA
    # =====================================================

    def asignar_enlazada(self, nombre, tam_archivo):

        bloques_necesarios = math.ceil(
            tam_archivo / self.tam_bloque
        )

        bloques_libres = [
            i
            for i, bloque in enumerate(self.disco)
            if bloque is None
        ]

        if len(bloques_libres) < bloques_necesarios:
            print(
                f"No hay bloques libres suficientes para {nombre}."
            )
            return False

        bloques_asignados = bloques_libres[
            :bloques_necesarios
        ]

        enlaces = {}

        for posicion, bloque in enumerate(
            bloques_asignados
        ):
            self.disco[bloque] = nombre

            if posicion < len(bloques_asignados) - 1:
                enlaces[bloque] = bloques_asignados[
                    posicion + 1
                ]
            else:
                enlaces[bloque] = None

        self.archivos[nombre] = {
            "metodo": "Enlazada",
            "tamano": tam_archivo,
            "bloques": bloques_asignados,
            "inicio": bloques_asignados[0],
            "enlaces": enlaces
        }

        print(
            f"{nombre} almacenado mediante asignación enlazada."
        )
        print(
            f"Cadena: {self.obtener_cadena_enlazada(nombre)}"
        )

        return True

    # =====================================================
    # ASIGNACIÓN INDEXADA
    # =====================================================

    def asignar_indexada(self, nombre, tam_archivo):

        bloques_datos = math.ceil(
            tam_archivo / self.tam_bloque
        )

        # Necesita un bloque adicional para el índice.
        total_necesario = bloques_datos + 1

        bloques_libres = [
            i
            for i, bloque in enumerate(self.disco)
            if bloque is None
        ]

        if len(bloques_libres) < total_necesario:
            print(
                f"No hay espacio suficiente para almacenar {nombre}."
            )
            return False

        bloque_indice = bloques_libres[0]

        bloques_asignados = bloques_libres[
            1:total_necesario
        ]

        self.disco[bloque_indice] = (
            f"{nombre}-INDICE"
        )

        for bloque in bloques_asignados:
            self.disco[bloque] = nombre

        self.archivos[nombre] = {
            "metodo": "Indexada",
            "tamano": tam_archivo,
            "bloque_indice": bloque_indice,
            "bloques": bloques_asignados
        }

        print(
            f"{nombre} almacenado mediante asignación indexada."
        )
        print(
            f"Bloque índice: {bloque_indice}"
        )
        print(
            f"Bloques de datos: {bloques_asignados}"
        )

        return True

    # =====================================================
    # LIBERAR ARCHIVOS
    # =====================================================

    def liberar(self, nombre):

        if nombre not in self.archivos:
            print(f"{nombre} no existe en el disco.")
            return False

        informacion = self.archivos[nombre]

        for bloque in informacion["bloques"]:
            self.disco[bloque] = None

        if informacion["metodo"] == "Indexada":
            bloque_indice = informacion[
                "bloque_indice"
            ]
            self.disco[bloque_indice] = None

        del self.archivos[nombre]

        print(f"{nombre} eliminado correctamente.")

        return True

    # =====================================================
    # CONSULTAS
    # =====================================================

    def obtener_cadena_enlazada(self, nombre):

        if nombre not in self.archivos:
            return "Archivo inexistente"

        informacion = self.archivos[nombre]

        if informacion["metodo"] != "Enlazada":
            return "El archivo no usa asignación enlazada"

        enlaces = informacion["enlaces"]
        actual = informacion["inicio"]

        cadena = []

        while actual is not None:
            cadena.append(str(actual))
            actual = enlaces[actual]

        cadena.append("FIN")

        return " → ".join(cadena)

    def mostrar_archivos(self):

        print("\nARCHIVOS ALMACENADOS\n")

        if not self.archivos:
            print("No existen archivos almacenados.")
            return

        for nombre, informacion in self.archivos.items():

            print(f"Archivo: {nombre}")
            print(f"Método: {informacion['metodo']}")
            print(f"Tamaño: {informacion['tamano']} KB")

            if informacion["metodo"] == "Indexada":
                print(
                    "Bloque índice:",
                    informacion["bloque_indice"]
                )

            if informacion["metodo"] == "Enlazada":
                print(
                    "Cadena:",
                    self.obtener_cadena_enlazada(nombre)
                )
            else:
                print(
                    "Bloques:",
                    informacion["bloques"]
                )

            print("-" * 40)

    def mostrar_estado(self):

        print("\nESTADO DEL DISCO\n")

        for i, bloque in enumerate(self.disco):

            if bloque is None:
                estado = "Libre"
            else:
                estado = bloque

            print(f"Bloque {i:02}: {estado}")

    # =====================================================
    # MÉTRICAS
    # =====================================================

    def obtener_metricas(self):

        bloques_ocupados = sum(
            1
            for bloque in self.disco
            if bloque is not None
        )

        bloques_libres = (
            self.total_bloques - bloques_ocupados
        )

        porcentaje_uso = (
            bloques_ocupados
            / self.total_bloques
        ) * 100

        espacio_total = (
            self.total_bloques
            * self.tam_bloque
        )

        espacio_ocupado = (
            bloques_ocupados
            * self.tam_bloque
        )

        espacio_libre = (
            bloques_libres
            * self.tam_bloque
        )

        return {
            "bloques_totales": self.total_bloques,
            "bloques_ocupados": bloques_ocupados,
            "bloques_libres": bloques_libres,
            "porcentaje_uso": porcentaje_uso,
            "espacio_total": espacio_total,
            "espacio_ocupado": espacio_ocupado,
            "espacio_libre": espacio_libre
        }

    def mostrar_metricas(self):

        metricas = self.obtener_metricas()

        print("\nMÉTRICAS DEL DISCO\n")

        print(
            f"Bloques totales: "
            f"{metricas['bloques_totales']}"
        )

        print(
            f"Bloques ocupados: "
            f"{metricas['bloques_ocupados']}"
        )

        print(
            f"Bloques libres: "
            f"{metricas['bloques_libres']}"
        )

        print(
            f"Espacio total: "
            f"{metricas['espacio_total']} KB"
        )

        print(
            f"Espacio ocupado: "
            f"{metricas['espacio_ocupado']} KB"
        )

        print(
            f"Espacio libre: "
            f"{metricas['espacio_libre']} KB"
        )

        print(
            f"Uso del disco: "
            f"{metricas['porcentaje_uso']:.2f}%"
        )