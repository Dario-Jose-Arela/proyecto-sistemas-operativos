class BloqueMemoria:

    def __init__(self,
                 inicio,
                 tamaño,
                 libre=True,
                 proceso=None):

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

    # FIRST FIT
    def first_fit(self, proceso):

        for i, bloque in enumerate(self.bloques):

            if (
                bloque.libre and
                bloque.tamaño >= proceso.memoria
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

                self.bloques[i:i+1] = nuevos

                return True

        return False

    # LIBERAR MEMORIA
    def liberar(self, proceso):

        for bloque in self.bloques:

            if (
                not bloque.libre and
                bloque.proceso == proceso
            ):

                bloque.libre = True

                bloque.proceso = None

    def mostrar_memoria(self):

        for bloque in self.bloques:

            print(bloque)