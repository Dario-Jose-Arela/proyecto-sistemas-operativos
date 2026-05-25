import math


class BloqueMemoria:

    def __init__(
        self,
        inicio,
        tamaño,
        libre=True,
        proceso=None
    ):

        self.inicio = inicio

        self.tamaño = tamaño

        self.libre = libre

        self.proceso = proceso

    def __str__(self):

        if self.libre:

            return (
                f"[Libre: {self.tamaño} KB]"
            )

        return (
            f"[{self.proceso.nombre}: "
            f"{self.tamaño} KB]"
        )


class GestorMemoria:

    def __init__(self, tamaño_total):

        self.tamaño_total = tamaño_total

        self.bloques = [

            BloqueMemoria(
                0,
                tamaño_total,
                True
            )
        ]

    # =================================================
    # FIRST FIT
    # =================================================

    def first_fit(self, proceso):

        for i, bloque in enumerate(self.bloques):

            if (
                bloque.libre and
                bloque.tamaño >= proceso.memoria
            ):

                return self.dividir_bloque(
                    i,
                    bloque,
                    proceso
                )

        return False

    # =================================================
    # BEST FIT
    # =================================================

    def best_fit(self, proceso):

        mejor_indice = -1

        mejor_tamaño = float('inf')

        for i, bloque in enumerate(self.bloques):

            if (
                bloque.libre and
                bloque.tamaño >= proceso.memoria
            ):

                if bloque.tamaño < mejor_tamaño:

                    mejor_tamaño = bloque.tamaño

                    mejor_indice = i

        if mejor_indice == -1:

            return False

        bloque = self.bloques[mejor_indice]

        return self.dividir_bloque(
            mejor_indice,
            bloque,
            proceso
        )

    # =================================================
    # WORST FIT
    # =================================================

    def worst_fit(self, proceso):

        peor_indice = -1

        peor_tamaño = -1

        for i, bloque in enumerate(self.bloques):

            if (
                bloque.libre and
                bloque.tamaño >= proceso.memoria
            ):

                if bloque.tamaño > peor_tamaño:

                    peor_tamaño = bloque.tamaño

                    peor_indice = i

        if peor_indice == -1:

            return False

        bloque = self.bloques[peor_indice]

        return self.dividir_bloque(
            peor_indice,
            bloque,
            proceso
        )

    # =================================================
    # BUDDY SYSTEM
    # =================================================

    def buddy_system(self, proceso):

        # Potencia de 2 mínima
        tamaño_necesario = 1

        while tamaño_necesario < proceso.memoria:

            tamaño_necesario *= 2

        for i, bloque in enumerate(self.bloques):

            if (
                bloque.libre and
                bloque.tamaño >= tamaño_necesario
            ):

                # Dividir hasta tamaño exacto
                while (
                    bloque.tamaño // 2
                    >= tamaño_necesario
                ):

                    mitad = bloque.tamaño // 2

                    bloque1 = BloqueMemoria(
                        bloque.inicio,
                        mitad,
                        True
                    )

                    bloque2 = BloqueMemoria(
                        bloque.inicio + mitad,
                        mitad,
                        True
                    )

                    self.bloques[i:i+1] = [
                        bloque1,
                        bloque2
                    ]

                    bloque = bloque1

                bloque.libre = False

                bloque.proceso = proceso

                return True

        return False

    # =================================================
    # DIVIDIR BLOQUE
    # =================================================

    def dividir_bloque(
        self,
        indice,
        bloque,
        proceso
    ):

        ocupado = BloqueMemoria(
            bloque.inicio,
            proceso.memoria,
            False,
            proceso
        )

        restante = (
            bloque.tamaño -
            proceso.memoria
        )

        nuevos = [ocupado]

        if restante > 0:

            libre = BloqueMemoria(
                bloque.inicio +
                proceso.memoria,

                restante,

                True
            )

            nuevos.append(libre)

        self.bloques[
            indice:indice+1
        ] = nuevos

        return True

    # =================================================
    # LIBERAR MEMORIA
    # =================================================

    def liberar(self, proceso):

        for bloque in self.bloques:

            if (
                not bloque.libre and
                bloque.proceso == proceso
            ):

                bloque.libre = True

                bloque.proceso = None

        self.fusionar_libres()

    # =================================================
    # FUSIONAR LIBRES
    # =================================================

    def fusionar_libres(self):

        nuevos = []

        i = 0

        while i < len(self.bloques):

            actual = self.bloques[i]

            while (
                i + 1 < len(self.bloques)
                and actual.libre
                and self.bloques[i + 1].libre
            ):

                actual.tamaño += (
                    self.bloques[i + 1].tamaño
                )

                i += 1

            nuevos.append(actual)

            i += 1

        self.bloques = nuevos

    # =================================================
    # USO MEMORIA
    # =================================================

    def uso_memoria(self):

        usado = 0

        for bloque in self.bloques:

            if not bloque.libre:

                usado += bloque.tamaño

        return (
            usado /
            self.tamaño_total
        ) * 100

    # =================================================
    # FRAGMENTACIÓN
    # =================================================

    def fragmentacion_externa(self):

        libre = 0

        for bloque in self.bloques:

            if bloque.libre:

                libre += bloque.tamaño

        return libre

    # =================================================
    # MOSTRAR MEMORIA
    # =================================================

    def mostrar_memoria(self):

        for bloque in self.bloques:

            print(bloque)