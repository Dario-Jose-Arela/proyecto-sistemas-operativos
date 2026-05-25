import tkinter as tk
from tkinter import ttk, filedialog

from simulator import SimuladorSO
from file_reader import leer_procesos
from metrics import calcular_metricas


class SistemaOperativoGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Simulador de Sistema Operativo"
        )

        self.root.geometry("1400x900")

        # Ruta CSV por defecto
        self.ruta_csv = "data/procesos.csv"

        # Procesos iniciales
        procesos = leer_procesos(
            self.ruta_csv
        )

        self.sim = SimuladorSO(procesos)

        # Variables Gantt
        self.gantt_x = 20

        self.bloque_gantt = 40

        self.crear_widgets()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def crear_widgets(self):

        # =================================================
        # TOP BAR
        # =================================================

        top = tk.Frame(
            self.root,
            bg="#1e1e1e",
            height=80
        )

        top.pack(fill="x")

        # =============================================
        # TIEMPO
        # =============================================

        self.label_tiempo = tk.Label(
            top,
            text="Tiempo: 0",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1e1e1e"
        )

        self.label_tiempo.pack(
            side="left",
            padx=20,
            pady=20
        )

        # =============================================
        # CPU
        # =============================================

        self.label_cpu = tk.Label(
            top,
            text="CPU: Libre",
            font=("Arial", 18, "bold"),
            fg="cyan",
            bg="#1e1e1e"
        )

        self.label_cpu.pack(
            side="left",
            padx=20
        )

        # =============================================
        # SELECTOR CPU
        # =============================================

        self.cpu_var = tk.StringVar()

        self.cpu_var.set("FCFS")

        cpu_combo = ttk.Combobox(
            top,
            textvariable=self.cpu_var,
            values=[
                "FCFS",
                "SPN",
                "SRT",
                "RR"
            ],
            width=10
        )

        cpu_combo.pack(
            side="left",
            padx=10
        )

        # =============================================
        # SELECTOR MEMORIA
        # =============================================

        self.mem_var = tk.StringVar()

        self.mem_var.set("First Fit")

        mem_combo = ttk.Combobox(
            top,
            textvariable=self.mem_var,
            values=[
                "First Fit",
                "Best Fit",
                "Worst Fit",
                "Buddy System"
            ],
            width=15
        )

        mem_combo.pack(
            side="left",
            padx=10
        )

        # =============================================
        # BOTÓN CARGAR CSV
        # =============================================

        self.btn_cargar = tk.Button(
            top,
            text="Cargar CSV",
            font=("Arial", 12),
            bg="#444",
            fg="white",
            command=self.cargar_archivo
        )

        self.btn_cargar.pack(
            side="right",
            padx=10
        )

        # =============================================
        # BOTÓN INICIAR
        # =============================================

        self.btn_inicio = tk.Button(
            top,
            text="Iniciar Simulación",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.iniciar_simulacion
        )

        self.btn_inicio.pack(
            side="right",
            padx=20
        )

        # =================================================
        # READY QUEUE
        # =================================================

        ready_frame = tk.Frame(
            self.root,
            bg="#2b2b2b",
            height=100
        )

        ready_frame.pack(fill="x")

        tk.Label(
            ready_frame,
            text="procesos en espera",
            font=("Arial", 16, "bold"),
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

        self.ready_label.pack(
            anchor="w",
            padx=20
        )

        # =================================================
        # MÉTRICAS
        # =================================================

        metricas = tk.Frame(
            self.root,
            bg="#151515",
            height=80
        )

        metricas.pack(fill="x")

        self.label_uso = tk.Label(
            metricas,
            text="Uso RAM: 0%",
            font=("Arial", 14),
            fg="lightgreen",
            bg="#151515"
        )

        self.label_uso.pack(
            side="left",
            padx=20,
            pady=10
        )

        self.label_frag = tk.Label(
            metricas,
            text="Fragmentación: 0 KB",
            font=("Arial", 14),
            fg="orange",
            bg="#151515"
        )

        self.label_frag.pack(
            side="left",
            padx=20
        )

        # =================================================
        # GANTT
        # =================================================

        gantt_frame = tk.Frame(
            self.root,
            bg="#202020"
        )

        gantt_frame.pack(fill="x")

        tk.Label(
            gantt_frame,
            text="Diagrama de Gantt CPU",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#202020"
        ).pack()

        # Scroll horizontal
        scroll_x = tk.Scrollbar(
            gantt_frame,
            orient="horizontal"
        )

        scroll_x.pack(
            side="bottom",
            fill="x"
        )

        self.canvas_gantt = tk.Canvas(
            gantt_frame,
            bg="white",
            height=120,
            xscrollcommand=scroll_x.set
        )

        self.canvas_gantt.pack(
            fill="x",
            padx=20,
            pady=10
        )

        scroll_x.config(
            command=self.canvas_gantt.xview
        )

        # =================================================
        # MEMORIA
        # =================================================

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
            text="Memoria",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack()

        self.canvas = tk.Canvas(
            memoria_frame,
            bg="white",
            height=220
        )

        self.canvas.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # =================================================
        # LOG
        # =================================================

        self.log = tk.Text(
            self.root,
            height=10,
            bg="black",
            fg="lime",
            font=("Consolas", 11)
        )

        self.log.pack(fill="both")

    # =====================================================
    # CARGAR CSV
    # =====================================================

    def cargar_archivo(self):

        ruta = filedialog.askopenfilename(

            filetypes=[
                ("CSV files", "*.csv")
            ]
        )

        if ruta:

            self.ruta_csv = ruta

            self.log.insert(
                tk.END,
                f"Archivo cargado: {ruta}\n"
            )

            self.log.see(tk.END)

    # =====================================================
    # INICIAR
    # =====================================================

    def iniciar_simulacion(self):

        procesos = leer_procesos(
            self.ruta_csv
        )

        self.sim = SimuladorSO(

            procesos,

            algoritmo_cpu=self.cpu_var.get(),

            algoritmo_memoria=self.mem_var.get()
        )

        # Reiniciar Gantt
        self.canvas_gantt.delete("all")

        self.gantt_x = 20

        # =============================================
        # GANTT DINÁMICO
        # =============================================

        total_cpu = sum(

            p.ejecucion

            for p in procesos
        )

        self.bloque_gantt = max(

            5,

            1200 // max(total_cpu, 1)
        )

        self.actualizar()

    # =====================================================
    # ACTUALIZAR
    # =====================================================

    def actualizar(self):

        self.sim.ejecutar_tick()

        # =============================================
        # TIEMPO
        # =============================================

        self.label_tiempo.config(
            text=f"Tiempo: {self.sim.tiempo}"
        )

        # =============================================
        # CPU
        # =============================================

        if self.sim.cpu:

            self.label_cpu.config(
                text=(
                    f"CPU: "
                    f"{self.sim.cpu.nombre}"
                )
            )

        else:

            self.label_cpu.config(
                text="CPU: Libre"
            )

        # =============================================
        # READY QUEUE
        # =============================================

        ready = [

            p.nombre

            for p in self.sim.ready_queue
        ]

        self.ready_label.config(
            text=str(ready)
        )

        # =============================================
        # MÉTRICAS
        # =============================================

        uso = self.sim.memoria.uso_memoria()

        frag = (
            self.sim.memoria
            .fragmentacion_externa()
        )

        self.label_uso.config(
            text=f"Uso RAM: {uso:.2f}%"
        )

        self.label_frag.config(
            text=f"Fragmentación: {frag} KB"
        )

        # =============================================
        # DIBUJOS
        # =============================================

        self.dibujar_memoria()

        self.actualizar_gantt()

        # =============================================
        # LOG
        # =============================================

        texto_cpu = (

            self.sim.cpu.nombre

            if self.sim.cpu

            else "Libre"
        )

        self.log.insert(

            tk.END,

            f"Tiempo {self.sim.tiempo} "
            f"| CPU: {texto_cpu}\n"
        )

        self.log.see(tk.END)

        # =============================================
        # CONTINUAR
        # =============================================

        if (

            len(self.sim.finalizados)

            <

            len(self.sim.procesos)

        ):

            self.root.after(
                10,
                self.actualizar
            )

        else:

            self.mostrar_metricas()
            

    # =====================================================
    # MÉTRICAS FINALES
    # =====================================================

    def mostrar_metricas(self):

        resultados, prom_esp, prom_ret = (

            calcular_metricas(
                self.sim.finalizados
            )
        )

        ventana = tk.Toplevel(self.root)

        ventana.title(
            "Métricas Finales"
        )

        ventana.geometry("700x400")

        tabla = tk.Text(

            ventana,

            font=("Consolas", 12)
        )

        tabla.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        encabezado = (

            f"{'Proceso':<10}"
            f"{'Llegada':<10}"
            f"{'CPU':<10}"
            f"{'Fin':<10}"
            f"{'Retorno':<12}"
            f"{'Espera':<10}\n"
        )

        tabla.insert(
            tk.END,
            encabezado
        )

        tabla.insert(
            tk.END,
            "-" * 65 + "\n"
        )

        for r in resultados:

            fila = (

                f"{r['nombre']:<10}"
                f"{r['llegada']:<10}"
                f"{r['ejecucion']:<10}"
                f"{r['fin']:<10}"
                f"{r['retorno']:<12}"
                f"{r['espera']:<10}\n"
            )

            tabla.insert(
                tk.END,
                fila
            )

        tabla.insert(
            tk.END,
            "\n"
        )

        tabla.insert(
            tk.END,
            f"Promedio Espera: "
            f"{prom_esp:.2f}\n"
        )

        tabla.insert(
            tk.END,
            f"Promedio Retorno: "
            f"{prom_ret:.2f}\n"
        )

    # =====================================================
    # GANTT
    # =====================================================

    def actualizar_gantt(self):

    # ==========================================
    # NO DIBUJAR SI CPU ESTÁ LIBRE
    # ==========================================

        if self.sim.cpu is None:
            return

        proceso = self.sim.cpu.nombre

    # ==========================================
    # COLORES
    # ==========================================

    # Generar color automático según número de proceso

        numero = int(
            proceso.replace("P", "")
)

        lista_colores = [

    "#87CEEB",
    "#90EE90",
    "#FFA500",
    "#FFC0CB",
    "#FFFF00",
    "#FF6347",
    "#40E0D0",
    "#9370DB",
    "#00FA9A",
    "#FF69B4",
    "#CD5C5C",
    "#7B68EE",
    "#3CB371",
    "#FFD700",
    "#6495ED",
    "#DC143C",
    "#00CED1",
    "#BA55D3",
    "#F4A460",
    "#20B2AA"

]

        color = lista_colores[
            numero % len(lista_colores)
]

    # ==========================================
    # POSICIONES
    # ==========================================

        x1 = self.gantt_x

        x2 = x1 + self.bloque_gantt

    # ==========================================
    # DIBUJAR BLOQUE
    # ==========================================

        self.canvas_gantt.create_rectangle(
            x1,
            30,
            x2,
            80,
            fill=color,
            outline="black"
    )

    # ==========================================
    # TEXTO DEL PROCESO
    # ==========================================

        if self.bloque_gantt >= 15:

            self.canvas_gantt.create_text(
                (x1 + x2) // 2,
                55,
                text=proceso,
                font=("Arial", 8)
        )

    # ==========================================
    # TIEMPO
    # ==========================================

        if self.bloque_gantt >= 10:

            self.canvas_gantt.create_text(
                x1,
                90,
                text=str(self.sim.tiempo),
                font=("Arial", 7)
        )

    # ==========================================
    # AVANZAR GANTT
    # ==========================================

        self.gantt_x += self.bloque_gantt

    # ==========================================
    # SCROLL AUTOMÁTICO
    # ==========================================

        self.canvas_gantt.config(
            scrollregion=(
                0,
                0,
                self.gantt_x + 200,
                120
        )
    )

        self.canvas_gantt.xview_moveto(1)
    # =====================================================
    # MEMORIA
    # =====================================================

    def dibujar_memoria(self):

        self.canvas.delete("all")

        ancho_total = 1200

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

                170,

                fill=color,

                outline="black"
            )

            texto = (

                "Libre"

                if bloque.libre

                else bloque.proceso.nombre
            )

            self.canvas.create_text(

                x + ancho / 2,

                110,

                text=f"{texto}\n{bloque.tamaño} KB",

                font=("Arial", 10, "bold")
            )

            x += ancho