import tkinter as tk
from tkinter import ttk

from simulator import SimuladorSO
from file_reader import leer_procesos


class SistemaOperativoGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Simulador de Sistema Operativo"
        )

        self.root.geometry("1200x700")

        # Cargar procesos
        procesos = leer_procesos(
            "data/procesos.csv"
        )

        self.sim = SimuladorSO(procesos)

        self.crear_widgets()

    def crear_widgets(self):

        # ===== FRAME SUPERIOR =====

        top = tk.Frame(
            self.root,
            bg="#1e1e1e",
            height=80
        )

        top.pack(fill="x")

        # Tiempo
        self.label_tiempo = tk.Label(
            top,
            text="Tiempo: 0",
            font=("Arial", 18),
            fg="white",
            bg="#1e1e1e"
        )

        self.label_tiempo.pack(
            side="left",
            padx=20,
            pady=20
        )

        # CPU
        self.label_cpu = tk.Label(
            top,
            text="CPU: Libre",
            font=("Arial", 18),
            fg="cyan",
            bg="#1e1e1e"
        )

        self.label_cpu.pack(
            side="left",
            padx=20
        )

        # Botón iniciar
        self.btn_inicio = tk.Button(
            top,
            text="Iniciar Simulación",
            font=("Arial", 14),
            command=self.actualizar
        )

        self.btn_inicio.pack(
            side="right",
            padx=20
        )

        # ===== READY QUEUE =====

        ready_frame = tk.Frame(
            self.root,
            bg="#2b2b2b",
            height=100
        )

        ready_frame.pack(fill="x")

        tk.Label(
            ready_frame,
            text="Ready Queue",
            font=("Arial", 16),
            fg="white",
            bg="#2b2b2b"
        ).pack(anchor="w", padx=10)

        self.ready_label = tk.Label(
            ready_frame,
            text="[]",
            font=("Arial", 14),
            fg="yellow",
            bg="#2b2b2b"
        )

        self.ready_label.pack(anchor="w", padx=20)

        # ===== MEMORIA =====

        memoria_frame = tk.Frame(
            self.root,
            bg="#1a1a1a"
        )

        memoria_frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            memoria_frame,
            text="Memoria RAM",
            font=("Arial", 16),
            fg="white",
            bg="#1a1a1a"
        ).pack()

        self.canvas = tk.Canvas(
            memoria_frame,
            bg="white",
            height=200
        )

        self.canvas.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # ===== LOG =====

        self.log = tk.Text(
            self.root,
            height=10,
            bg="black",
            fg="lime",
            font=("Consolas", 11)
        )

        self.log.pack(fill="both")

    # ===================================

    def actualizar(self):

        self.sim.ejecutar_tick()

        # Tiempo
        self.label_tiempo.config(
            text=f"Tiempo: {self.sim.tiempo}"
        )

        # CPU
        if self.sim.cpu:

            self.label_cpu.config(
                text=f"CPU: {self.sim.cpu.nombre}"
            )

        else:

            self.label_cpu.config(
                text="CPU: Libre"
            )

        # Ready Queue
        ready = [
            p.nombre
            for p in self.sim.ready_queue
        ]

        self.ready_label.config(
            text=str(ready)
        )

        # Dibujar memoria
        self.dibujar_memoria()

        # Repetir simulación
        self.root.after(
            1000,
            self.actualizar
        )

    # ===================================

    def dibujar_memoria(self):

        self.canvas.delete("all")

        ancho_total = 1000

        x = 10

        for bloque in self.sim.memoria.bloques:

            ancho = (
                bloque.tamaño /
                self.sim.memoria.tamaño_total
            ) * ancho_total

            color = (
                "lightgreen"
                if bloque.libre
                else "skyblue"
            )

            self.canvas.create_rectangle(
                x,
                50,
                x + ancho,
                150,
                fill=color
            )

            texto = (
                "Libre"
                if bloque.libre
                else bloque.proceso.nombre
            )

            self.canvas.create_text(
                x + ancho/2,
                100,
                text=f"{texto}\n{bloque.tamaño} KB"
            )

            x += ancho