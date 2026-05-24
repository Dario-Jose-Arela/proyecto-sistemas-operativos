from memory_manager import GestorMemoria
class SimuladorSO:

    def __init__(self, procesos):
        self.memoria = GestorMemoria(1024)

        self.tiempo = 0

        self.procesos = procesos

        self.ready_queue = []

        self.finalizados = []

        # CPU actual
        self.cpu = None

    def procesos_llegados(self):

        for proceso in self.procesos:

            if proceso.llegada == self.tiempo:

                print(
                    f"[Tiempo {self.tiempo}] "
                    f"Llegó {proceso.nombre}"
            )

            # Intentar asignar RAM
            asignado = self.memoria.first_fit(
                proceso
            )

            if asignado:

                print(
                    f"{proceso.nombre} "
                    f"entró a memoria"
                )

                self.ready_queue.append(
                    proceso
                )

            else:

                print(
                    f"NO hay memoria para "
                    f"{proceso.nombre}"
                )
    def planificar_fcfs(self):

        # Si CPU libre
        if self.cpu is None:

            if self.ready_queue:

                self.cpu = self.ready_queue.pop(0)

                print(
                    f"CPU asignado a "
                    f"{self.cpu.nombre}"
                )

    def ejecutar_cpu(self):

        if self.cpu is not None:

            self.cpu.restante -= 1

            print(
                f"Ejecutando {self.cpu.nombre} "
                f"| Restante: {self.cpu.restante}"
            )

            # Si termina
            if self.cpu.restante == 0:
                self.memoria.liberar(self.cpu)

                self.cpu.fin = self.tiempo + 1

                self.finalizados.append(self.cpu)

                print(
                    f"{self.cpu.nombre} TERMINÓ"
                )

                self.cpu = None

    def mostrar_ready(self):

        nombres = [
            p.nombre
            for p in self.ready_queue
        ]

        print("Ready Queue:", nombres)

    def ejecutar_tick(self):

        print(f"\n===== Tiempo {self.tiempo} =====")

        # Llegadas
        self.procesos_llegados()

        # FCFS
        self.planificar_fcfs()

        # Ejecutar CPU
        self.ejecutar_cpu()

        # Mostrar ready
        self.mostrar_ready()
        print("\nMEMORIA:")

        self.memoria.mostrar_memoria()

        # Avanzar tiempo
        self.tiempo += 1