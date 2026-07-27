from memory_manager import GestorMemoria
from storage_manager import GestorAlmacenamiento


class SimuladorSO:

    def __init__(
        self,
        procesos,
        algoritmo_cpu="FCFS",
        algoritmo_memoria="First Fit",
        algoritmo_almacenamiento="Contigua",
        quantum=2
    ):
        # ==========================================
        # MEMORIA RAM
        # ==========================================

        self.memoria = GestorMemoria(1024)

        # ==========================================
        # ALMACENAMIENTO EN DISCO
        # ==========================================

        self.almacenamiento = GestorAlmacenamiento(
            bloques=64,
            tam_bloque=4,
            algoritmo=algoritmo_almacenamiento
        )

        # ==========================================
        # INFORMACIÓN GENERAL
        # ==========================================

        self.tiempo = 0
        self.procesos = procesos
        self.ready_queue = []
        self.finalizados = []

        # Algoritmos seleccionados
        self.algoritmo_cpu = algoritmo_cpu
        self.algoritmo_memoria = algoritmo_memoria
        self.algoritmo_almacenamiento = (
            algoritmo_almacenamiento
        )

        # CPU actual
        self.cpu = None

        # Round Robin
        self.quantum = max(1, int(quantum))
        self.quantum_actual = 0

    # ==========================================
    # ASIGNAR MEMORIA RAM
    # ==========================================

    def asignar_memoria(self, proceso):

        if self.algoritmo_memoria == "First Fit":
            return self.memoria.first_fit(proceso)

        elif self.algoritmo_memoria == "Best Fit":
            return self.memoria.best_fit(proceso)

        elif self.algoritmo_memoria == "Worst Fit":
            return self.memoria.worst_fit(proceso)

        else:
            return self.memoria.first_fit(proceso)

    # ==========================================
    # ASIGNAR ALMACENAMIENTO
    # ==========================================

    def asignar_almacenamiento(self, proceso):

        # Mientras el CSV todavía no tenga almacenamiento,
        # los procesos con valor 0 no ocuparán disco.
        if proceso.almacenamiento <= 0:
            return True

        return self.almacenamiento.asignar(
            proceso.nombre,
            proceso.almacenamiento
        )

    # ==========================================
    # LLEGADA DE PROCESOS
    # ==========================================

    def procesos_llegados(self):

        for proceso in self.procesos:

            if (
                proceso.llegada <= self.tiempo
                and not proceso.cargado
            ):
                print(
                    f"[Tiempo {self.tiempo}] "
                    f"Llegó {proceso.nombre}"
                )

                # Primero se intenta asignar RAM
                memoria_asignada = self.asignar_memoria(
                    proceso
                )

                if not memoria_asignada:
                    print(
                        f"NO hay memoria RAM para "
                        f"{proceso.nombre}"
                    )
                    continue

                print(
                    f"{proceso.nombre} entró a memoria RAM"
                )

                # Después se intenta asignar disco
                disco_asignado = (
                    self.asignar_almacenamiento(proceso)
                )

                if not disco_asignado:
                    print(
                        f"NO hay almacenamiento para "
                        f"{proceso.nombre}"
                    )

                    # Si no entra al disco, se deshace
                    # la asignación que se realizó en RAM.
                    self.memoria.liberar(proceso)

                    continue

                if proceso.almacenamiento > 0:
                    print(
                        f"{proceso.nombre} ocupó "
                        f"{proceso.almacenamiento} KB "
                        f"en disco"
                    )

                proceso.cargado = True

                self.ready_queue.append(proceso)

                print(
                    f"{proceso.nombre} ingresó a "
                    f"la Ready Queue"
                )

    # ==========================================
    # REGISTRAR INICIO
    # ==========================================

    def registrar_inicio(self, proceso):

        if proceso.inicio is None:
            proceso.inicio = self.tiempo

    # ==========================================
    # FCFS
    # ==========================================

    def planificar_fcfs(self):

        if self.cpu is None and self.ready_queue:

            self.cpu = self.ready_queue.pop(0)

            self.registrar_inicio(self.cpu)

            print(
                f"FCFS asignó CPU a "
                f"{self.cpu.nombre}"
            )

    # ==========================================
    # SPN
    # ==========================================

    def planificar_spn(self):

        if self.cpu is None and self.ready_queue:

            self.ready_queue.sort(
                key=lambda proceso: proceso.ejecucion
            )

            self.cpu = self.ready_queue.pop(0)

            self.registrar_inicio(self.cpu)

            print(
                f"SPN seleccionó "
                f"{self.cpu.nombre}"
            )

    # ==========================================
    # SRT
    # ==========================================

    def planificar_srt(self):

        if self.cpu is not None:
            self.ready_queue.append(self.cpu)
            self.cpu = None

        if self.ready_queue:

            self.ready_queue.sort(
                key=lambda proceso: proceso.restante
            )

            self.cpu = self.ready_queue.pop(0)

            self.registrar_inicio(self.cpu)

            print(
                f"SRT seleccionó "
                f"{self.cpu.nombre}"
            )

    # ==========================================
    # ROUND ROBIN
    # ==========================================

    def planificar_rr(self):

        # Round Robin únicamente selecciona otro
        # proceso cuando la CPU está libre.
        if self.cpu is None and self.ready_queue:

            self.cpu = self.ready_queue.pop(0)
            self.quantum_actual = 0

            self.registrar_inicio(self.cpu)

            print(
                f"RR asignó CPU a "
                f"{self.cpu.nombre}"
            )

    # ==========================================
    # FINALIZAR PROCESO
    # ==========================================

    def finalizar_proceso(self):

        proceso = self.cpu

        # Liberar memoria RAM
        self.memoria.liberar(proceso)

        # Liberar almacenamiento en disco
        if proceso.almacenamiento > 0:
            self.almacenamiento.liberar(
                proceso.nombre
            )

        proceso.fin = self.tiempo + 1

        proceso.retorno = (
            proceso.fin - proceso.llegada
        )

        proceso.espera = (
            proceso.retorno - proceso.ejecucion
        )

        self.finalizados.append(proceso)

        print(
            f"{proceso.nombre} TERMINÓ"
        )

        print(
            f"{proceso.nombre} liberó su RAM "
            f"y sus bloques de disco"
        )

        self.cpu = None
        self.quantum_actual = 0

    # ==========================================
    # EJECUTAR CPU
    # ==========================================

    def ejecutar_cpu(self):

        if self.cpu is None:
            print("CPU inactiva")
            return

        self.cpu.restante -= 1

        print(
            f"Ejecutando {self.cpu.nombre} "
            f"| Restante: {self.cpu.restante}"
        )

        # El proceso terminó
        if self.cpu.restante <= 0:
            self.finalizar_proceso()
            return

        # Control del quantum únicamente en RR
        if self.algoritmo_cpu == "RR":

            self.quantum_actual += 1

            if self.quantum_actual >= self.quantum:

                print(
                    f"Quantum terminado para "
                    f"{self.cpu.nombre}"
                )

                self.ready_queue.append(self.cpu)

                self.cpu = None
                self.quantum_actual = 0

    # ==========================================
    # READY QUEUE
    # ==========================================

    def mostrar_ready(self):

        nombres = [
            proceso.nombre
            for proceso in self.ready_queue
        ]

        print(
            "Ready Queue:",
            nombres
        )

    # ==========================================
    # MOSTRAR ALMACENAMIENTO
    # ==========================================

    def mostrar_almacenamiento(self):

        print("\nALMACENAMIENTO:")

        bloques_ocupados = []

        for numero, contenido in enumerate(
            self.almacenamiento.disco
        ):
            if contenido is not None:
                bloques_ocupados.append(
                    f"{numero}:{contenido}"
                )

        if bloques_ocupados:
            print(
                "Bloques ocupados:",
                " | ".join(bloques_ocupados)
            )
        else:
            print("Todos los bloques están libres")

        metricas = (
            self.almacenamiento.obtener_metricas()
        )

        print(
            f"Uso del disco: "
            f"{metricas['porcentaje_uso']:.2f}%"
        )

        print(
            f"Bloques libres: "
            f"{metricas['bloques_libres']}"
        )

    # ==========================================
    # TICK PRINCIPAL
    # ==========================================

    def ejecutar_tick(self):

        print(
            f"\n===== Tiempo "
            f"{self.tiempo} ====="
        )

        # Llegada de procesos
        self.procesos_llegados()

        # Planificación de CPU
        if self.algoritmo_cpu == "FCFS":
            self.planificar_fcfs()

        elif self.algoritmo_cpu == "SPN":
            self.planificar_spn()

        elif self.algoritmo_cpu == "SRT":
            self.planificar_srt()

        elif self.algoritmo_cpu == "RR":
            self.planificar_rr()

        else:
            self.planificar_fcfs()

        # Ejecutar una unidad de CPU
        self.ejecutar_cpu()

        # Mostrar Ready Queue
        self.mostrar_ready()

        # Mostrar memoria RAM
        print("\nMEMORIA RAM:")
        self.memoria.mostrar_memoria()

        # Mostrar almacenamiento
        self.mostrar_almacenamiento()

        # Avanzar tiempo
        self.tiempo += 1