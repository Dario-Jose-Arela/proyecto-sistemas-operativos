from memory_manager import GestorMemoria


class SimuladorSO:

    def __init__(
        self,
        procesos,
        algoritmo_cpu="FCFS",
        algoritmo_memoria="First Fit"
    ):

        self.memoria = GestorMemoria(1024)

        self.tiempo = 0

        self.procesos = procesos

        self.ready_queue = []

        self.finalizados = []

        # Algoritmos seleccionados
        self.algoritmo_cpu = algoritmo_cpu

        self.algoritmo_memoria = algoritmo_memoria

        # CPU actual
        self.cpu = None
        # Round Robin
        self.quantum = 2

        self.quantum_actual = 0

    # ==========================================
    # LLEGADA DE PROCESOS
    # ==========================================

    def procesos_llegados(self):

        for proceso in self.procesos:

            if (
                proceso.llegada <= self.tiempo
                and
                not proceso.cargado
            ):

                print(
                    f"[Tiempo {self.tiempo}] "
                    f"Llegó {proceso.nombre}"
                )

                # ==========================
                # ASIGNACIÓN MEMORIA
                # ==========================

                if self.algoritmo_memoria == "First Fit":

                    asignado = self.memoria.first_fit(
                        proceso
                    )

                elif self.algoritmo_memoria == "Best Fit":

                    asignado = self.memoria.best_fit(
                        proceso
                    )

                elif self.algoritmo_memoria == "Worst Fit":

                    asignado = self.memoria.worst_fit(
                        proceso
                    )

                else:

                    asignado = self.memoria.first_fit(
                        proceso
                    )

                # ==========================
                # SI ENTRA A MEMORIA
                # ==========================

                if asignado:

                    print(
                        f"{proceso.nombre} "
                        f"entró a memoria"
                    )

                    proceso.cargado = True

                    self.ready_queue.append(
                        proceso
                )

                else:

                    print(
                        f"NO hay memoria para "
                        f"{proceso.nombre}"
                    )

    # ==========================================
    # FCFS
    # ==========================================

    def planificar_fcfs(self):

        if self.cpu is None:

            if self.ready_queue:

                self.cpu = self.ready_queue.pop(0)

                print(
                    f"CPU asignado a "
                    f"{self.cpu.nombre}"
                )

    # ==========================================
    # SPN
    # ==========================================

    def planificar_spn(self):

        if self.cpu is None:

            if self.ready_queue:

                self.ready_queue.sort(
                    key=lambda p: p.ejecucion
                )

                self.cpu = self.ready_queue.pop(0)

                print(
                    f"SPN seleccionó "
                    f"{self.cpu.nombre}"
                )

    # ==========================================
    # SRT
    # ==========================================

    def planificar_srt(self):

        # Si hay proceso ejecutándose
        if self.cpu is not None:

            self.ready_queue.append(
                self.cpu
            )

        # Elegir menor restante
        if self.ready_queue:

            self.ready_queue.sort(
                key=lambda p: p.restante
            )

            nuevo = self.ready_queue.pop(0)

            if self.cpu != nuevo:

                print(
                    f"SRT cambia CPU a "
                    f"{nuevo.nombre}"
                )

            self.cpu = nuevo

    # ==========================================
    # ROUND ROBIN (temporal)
    # ==========================================

    def planificar_rr(self):

    # ======================================
    # CPU LIBRE
    # ======================================

        if self.cpu is None:

            if self.ready_queue:

                self.cpu = self.ready_queue.pop(0)

                self.quantum_actual = 0

            print(
                f"RR asignó "
                f"{self.cpu.nombre}"
            )

    # ======================================
    # CPU OCUPADA
    # ======================================

        else:

        # Aumentar quantum usado
            self.quantum_actual += 1

        # Quantum terminado
        if self.quantum_actual >= self.quantum:

            print(
                f"Quantum terminado "
                f"para {self.cpu.nombre}"
            )

            # Si aún no termina
            if self.cpu.restante > 0:

                self.ready_queue.append(
                    self.cpu
                )

            # Liberar CPU
            self.cpu = None

            self.quantum_actual = 0

            # Asignar siguiente proceso
            if self.ready_queue:

                self.cpu = self.ready_queue.pop(0)

                print(
                    f"RR cambia a "
                    f"{self.cpu.nombre}"
                )

    # ==========================================
    # EJECUTAR CPU
    # ==========================================

    def ejecutar_cpu(self):

        if self.cpu is not None:

            self.cpu.restante -= 1

            print(
                f"Ejecutando {self.cpu.nombre} "
                f"| Restante: {self.cpu.restante}"
            )

            # TERMINA
            if self.cpu.restante == 0:

                self.memoria.liberar(
                    self.cpu
                )

                self.cpu.fin = (
                    self.tiempo + 1
                )

                self.finalizados.append(
                    self.cpu
                )

                print(
                    f"{self.cpu.nombre} TERMINÓ"
                )

                self.cpu = None
                self.quantum_actual = 1

    # ==========================================
    # READY QUEUE
    # ==========================================

    def mostrar_ready(self):

        nombres = [

            p.nombre

            for p in self.ready_queue
        ]

        print(
            "Ready Queue:",
            nombres
        )

    # ==========================================
    # TICK PRINCIPAL
    # ==========================================

    def ejecutar_tick(self):

        print(
            f"\n===== Tiempo "
            f"{self.tiempo} ====="
        )

        # Llegadas
        self.procesos_llegados()

        # ==========================
        # PLANIFICACIÓN CPU
        # ==========================

        if self.algoritmo_cpu == "FCFS":

            self.planificar_fcfs()

        elif self.algoritmo_cpu == "SPN":

            self.planificar_spn()

        elif self.algoritmo_cpu == "SRT":

            self.planificar_srt()

        elif self.algoritmo_cpu == "RR":

            self.planificar_rr()

        # ==========================
        # EJECUTAR CPU
        # ==========================

        self.ejecutar_cpu()

        # ==========================
        # MOSTRAR READY
        # ==========================

        self.mostrar_ready()

        # ==========================
        # MEMORIA
        # ==========================

        print("\nMEMORIA:")

        self.memoria.mostrar_memoria()

        # ==========================
        # AVANZAR TIEMPO
        # ==========================

        self.tiempo += 1