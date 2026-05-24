class Proceso:

    def __init__(self, nombre, llegada, ejecucion, memoria):

        self.nombre = nombre

        self.llegada = int(llegada)

        self.ejecucion = int(ejecucion)

        self.restante = int(ejecucion)

        self.memoria = int(memoria)

        # Métricas
        self.inicio = None
        self.fin = None
        self.espera = 0
        self.retorno = 0

        # Memoria
        self.memoria_inicio = None
        self.memoria_fin = None

    def __str__(self):

        return (
            f"{self.nombre} | "
            f"Llegada: {self.llegada} | "
            f"CPU: {self.ejecucion} | "
            f"RAM: {self.memoria} KB"
        )