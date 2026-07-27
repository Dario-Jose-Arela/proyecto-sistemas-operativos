import tkinter as tk
from tkinter import ttk, filedialog

from simulator import SimuladorSO
from file_reader import leer_procesos
from metrics import calcular_metricas


class SistemaOperativoGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Simulador de Sistema Operativo")
        self.root.geometry("1400x950")
        self.root.minsize(1100, 750)

        # Ruta CSV por defecto
        self.ruta_csv = "data/procesos.csv"

        # Procesos iniciales
        procesos = leer_procesos(self.ruta_csv)

        self.sim = SimuladorSO(procesos)

        # Variables del diagrama de Gantt
        self.gantt_x = 20
        self.bloque_gantt = 40

        # Velocidad de simulación en milisegundos
        self.velocidad = tk.IntVar(value=500)

        # Control para evitar varias simulaciones simultáneas
        self.after_id = None
        self.simulacion_activa = False

        # Paleta utilizada para procesos
        self.lista_colores = [
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

        self.crear_widgets()

        # Dibujos iniciales
        self.dibujar_memoria()
        self.dibujar_disco()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def crear_widgets(self):

        # =================================================
        # BARRA SUPERIOR
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
            font=("Arial", 17, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        self.label_tiempo.pack(
            side="left",
            padx=15,
            pady=20
        )

        # =============================================
        # CPU
        # =============================================

        self.label_cpu = tk.Label(
            top,
            text="CPU: Libre",
            font=("Arial", 17, "bold"),
            fg="cyan",
            bg="#1e1e1e"
        )
        self.label_cpu.pack(
            side="left",
            padx=15
        )

        # =============================================
        # SELECTOR CPU
        # =============================================

        tk.Label(
            top,
            text="CPU:",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(side="left", padx=(10, 2))

        self.cpu_var = tk.StringVar(value="FCFS")

        self.cpu_combo = ttk.Combobox(
            top,
            textvariable=self.cpu_var,
            values=[
                "FCFS",
                "SPN",
                "SRT",
                "RR"
            ],
            width=8,
            state="readonly"
        )
        self.cpu_combo.pack(
            side="left",
            padx=5
        )

        # =============================================
        # SELECTOR MEMORIA
        # =============================================

        tk.Label(
            top,
            text="RAM:",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(side="left", padx=(10, 2))

        self.mem_var = tk.StringVar(value="First Fit")

        self.mem_combo = ttk.Combobox(
            top,
            textvariable=self.mem_var,
            values=[
                "First Fit",
                "Best Fit",
                "Worst Fit",
                "Buddy System"
            ],
            width=13,
            state="readonly"
        )
        self.mem_combo.pack(
            side="left",
            padx=5
        )

        # =============================================
        # SELECTOR DE ALMACENAMIENTO
        # =============================================

        tk.Label(
            top,
            text="Disco:",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(side="left", padx=(10, 2))

        self.storage_var = tk.StringVar(value="Contigua")

        self.storage_combo = ttk.Combobox(
            top,
            textvariable=self.storage_var,
            values=[
                "Contigua",
                "Enlazada",
                "Indexada"
            ],
            width=11,
            state="readonly"
        )
        self.storage_combo.pack(
            side="left",
            padx=5
        )

        # =============================================
        # BOTÓN CARGAR CSV
        # =============================================

        self.btn_cargar = tk.Button(
            top,
            text="Cargar CSV",
            font=("Arial", 11),
            bg="#444444",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            command=self.cargar_archivo
        )
        self.btn_cargar.pack(
            side="right",
            padx=8
        )

        # =============================================
        # BOTÓN INICIAR
        # =============================================

        self.btn_inicio = tk.Button(
            top,
            text="Iniciar",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            activebackground="#007000",
            activeforeground="white",
            command=self.iniciar_simulacion
        )
        self.btn_inicio.pack(
            side="right",
            padx=10
        )

        # =============================================
        # CONTROL DE VELOCIDAD
        # =============================================

        tk.Label(
            top,
            text="Velocidad",
            font=("Arial", 10),
            fg="white",
            bg="#1e1e1e"
        ).pack(
            side="right",
            padx=3
        )

        self.slider_velocidad = tk.Scale(
            top,
            from_=50,
            to=2000,
            resolution=50,
            orient="horizontal",
            variable=self.velocidad,
            bg="#1e1e1e",
            fg="white",
            highlightthickness=0,
            length=150
        )
        self.slider_velocidad.pack(
            side="right",
            padx=5
        )

        # =================================================
        # READY QUEUE
        # =================================================

        ready_frame = tk.Frame(
            self.root,
            bg="#2b2b2b",
            height=75
        )
        ready_frame.pack(fill="x")

        tk.Label(
            ready_frame,
            text="Procesos en espera",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2b2b2b"
        ).pack(
            anchor="w",
            padx=10,
            pady=(5, 0)
        )

        self.ready_label = tk.Label(
            ready_frame,
            text="[]",
            font=("Arial", 13),
            fg="yellow",
            bg="#2b2b2b"
        )
        self.ready_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 5)
        )

        # =================================================
        # MÉTRICAS
        # =================================================

        metricas = tk.Frame(
            self.root,
            bg="#151515",
            height=60
        )
        metricas.pack(fill="x")

        self.label_uso = tk.Label(
            metricas,
            text="Uso RAM: 0%",
            font=("Arial", 13),
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
            font=("Arial", 13),
            fg="orange",
            bg="#151515"
        )
        self.label_frag.pack(
            side="left",
            padx=20
        )

        # Métrica nueva de almacenamiento
        self.label_disco = tk.Label(
            metricas,
            text="Uso Disco: 0%",
            font=("Arial", 13),
            fg="cyan",
            bg="#151515"
        )
        self.label_disco.pack(
            side="left",
            padx=20
        )

        self.label_bloques_disco = tk.Label(
            metricas,
            text="Bloques libres: 64",
            font=("Arial", 13),
            fg="#DDA0DD",
            bg="#151515"
        )
        self.label_bloques_disco.pack(
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
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=(4, 0))

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
            height=105,
            xscrollcommand=scroll_x.set
        )
        self.canvas_gantt.pack(
            fill="x",
            padx=20,
            pady=5
        )

        scroll_x.config(
            command=self.canvas_gantt.xview
        )

        # =================================================
        # CONTENEDOR DE RAM Y DISCO
        # =================================================

        recursos_frame = tk.Frame(
            self.root,
            bg="#1a1a1a"
        )
        recursos_frame.pack(
            fill="both",
            expand=True
        )

        # Dividir el espacio en dos columnas
        recursos_frame.grid_columnconfigure(
            0,
            weight=1
        )
        recursos_frame.grid_columnconfigure(
            1,
            weight=1
        )
        recursos_frame.grid_rowconfigure(
            0,
            weight=1
        )

        # =================================================
        # MEMORIA RAM
        # =================================================

        memoria_frame = tk.Frame(
            recursos_frame,
            bg="#1a1a1a",
            bd=1,
            relief="solid"
        )
        memoria_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=5
        )

        tk.Label(
            memoria_frame,
            text="Memoria RAM",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(pady=5)

        self.canvas = tk.Canvas(
            memoria_frame,
            bg="white",
            height=230
        )
        self.canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # ALMACENAMIENTO EN DISCO
        # =================================================

        disco_frame = tk.Frame(
            recursos_frame,
            bg="#1a1a1a",
            bd=1,
            relief="solid"
        )
        disco_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=5
        )

        tk.Label(
            disco_frame,
            text="Almacenamiento en Disco",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(pady=5)

        self.canvas_disco = tk.Canvas(
            disco_frame,
            bg="white",
            height=230
        )
        self.canvas_disco.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # LOG
        # =================================================

        self.log = tk.Text(
            self.root,
            height=7,
            bg="black",
            fg="lime",
            insertbackground="white",
            font=("Consolas", 10)
        )
        self.log.pack(fill="both")

    # =====================================================
    # CARGAR CSV
    # =====================================================

    def cargar_archivo(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de procesos",
            filetypes=[
                ("Archivos CSV", "*.csv")
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
    # INICIAR SIMULACIÓN
    # =====================================================

    def iniciar_simulacion(self):

        # Detener cualquier actualización anterior
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        try:
            procesos = leer_procesos(
                self.ruta_csv
            )

            if not procesos:
                self.escribir_log(
                    "El archivo no contiene procesos."
                )
                return

            self.sim = SimuladorSO(
                procesos,
                algoritmo_cpu=self.cpu_var.get(),
                algoritmo_memoria=self.mem_var.get(),
                algoritmo_almacenamiento=(
                    self.storage_var.get()
                )
            )

        except Exception as error:
            self.escribir_log(
                f"Error al iniciar: {error}"
            )
            return

        self.simulacion_activa = True

        # Reiniciar interfaz
        self.canvas_gantt.delete("all")
        self.canvas.delete("all")
        self.canvas_disco.delete("all")
        self.log.delete("1.0", tk.END)

        self.gantt_x = 20

        # Ajustar dinámicamente el tamaño del Gantt
        total_cpu = sum(
            proceso.ejecucion
            for proceso in procesos
        )

        self.bloque_gantt = max(
            8,
            1200 // max(total_cpu, 1)
        )

        self.escribir_log(
            "Simulación iniciada"
        )
        self.escribir_log(
            f"CPU: {self.cpu_var.get()}"
        )
        self.escribir_log(
            f"RAM: {self.mem_var.get()}"
        )
        self.escribir_log(
            f"Disco: {self.storage_var.get()}"
        )

        self.actualizar()

    # =====================================================
    # ACTUALIZAR SIMULACIÓN
    # =====================================================

    def actualizar(self):

        if not self.simulacion_activa:
            return

        try:
            self.sim.ejecutar_tick()

        except Exception as error:
            self.simulacion_activa = False
            self.escribir_log(
                f"Error durante la simulación: {error}"
            )
            return

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
                text=f"CPU: {self.sim.cpu.nombre}"
            )
        else:
            self.label_cpu.config(
                text="CPU: Libre"
            )

        # =============================================
        # READY QUEUE
        # =============================================

        ready = [
            proceso.nombre
            for proceso in self.sim.ready_queue
        ]

        self.ready_label.config(
            text=str(ready)
        )

        # =============================================
        # MÉTRICAS DE MEMORIA RAM
        # =============================================

        uso_ram = self.sim.memoria.uso_memoria()

        fragmentacion = (
            self.sim.memoria.fragmentacion_externa()
        )

        self.label_uso.config(
            text=f"Uso RAM: {uso_ram:.2f}%"
        )

        self.label_frag.config(
            text=(
                f"Fragmentación: "
                f"{fragmentacion} KB"
            )
        )

        # =============================================
        # MÉTRICAS DE ALMACENAMIENTO
        # =============================================

        metricas_disco = (
            self.sim.almacenamiento.obtener_metricas()
        )

        porcentaje_disco = metricas_disco.get(
            "porcentaje_uso",
            0
        )

        bloques_libres = metricas_disco.get(
            "bloques_libres",
            0
        )

        self.label_disco.config(
            text=(
                f"Uso Disco: "
                f"{porcentaje_disco:.2f}%"
            )
        )

        self.label_bloques_disco.config(
            text=(
                f"Bloques libres: "
                f"{bloques_libres}"
            )
        )

        # =============================================
        # DIBUJOS
        # =============================================

        self.dibujar_memoria()
        self.dibujar_disco()
        self.actualizar_gantt()

        # =============================================
        # LOG
        # =============================================

        texto_cpu = (
            self.sim.cpu.nombre
            if self.sim.cpu
            else "Libre"
        )

        self.escribir_log(
            f"Tiempo {self.sim.tiempo} "
            f"| CPU: {texto_cpu} "
            f"| Ready: {ready} "
            f"| RAM: {uso_ram:.2f}% "
            f"| Disco: {porcentaje_disco:.2f}%"
        )

        # =============================================
        # CONTINUAR O FINALIZAR
        # =============================================

        if (
            len(self.sim.finalizados)
            < len(self.sim.procesos)
        ):
            self.after_id = self.root.after(
                self.velocidad.get(),
                self.actualizar
            )
        else:
            self.simulacion_activa = False
            self.after_id = None

            self.label_cpu.config(
                text="CPU: Libre"
            )

            self.escribir_log(
                "Simulación finalizada correctamente."
            )

            self.mostrar_metricas()

    # =====================================================
    # ESCRIBIR EN EL LOG
    # =====================================================

    def escribir_log(self, texto):

        self.log.insert(
            tk.END,
            texto + "\n"
        )
        self.log.see(tk.END)

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
        ventana.title("Métricas Finales")
        ventana.geometry("760x450")

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

        for resultado in resultados:

            fila = (
                f"{resultado['nombre']:<10}"
                f"{resultado['llegada']:<10}"
                f"{resultado['ejecucion']:<10}"
                f"{resultado['fin']:<10}"
                f"{resultado['retorno']:<12}"
                f"{resultado['espera']:<10}\n"
            )

            tabla.insert(
                tk.END,
                fila
            )

        metricas_disco = (
            self.sim.almacenamiento.obtener_metricas()
        )

        tabla.insert(
            tk.END,
            "\n"
        )

        tabla.insert(
            tk.END,
            f"Promedio de espera: "
            f"{prom_esp:.2f}\n"
        )

        tabla.insert(
            tk.END,
            f"Promedio de retorno: "
            f"{prom_ret:.2f}\n"
        )

        tabla.insert(
            tk.END,
            f"Algoritmo CPU: "
            f"{self.sim.algoritmo_cpu}\n"
        )

        tabla.insert(
            tk.END,
            f"Algoritmo RAM: "
            f"{self.sim.algoritmo_memoria}\n"
        )

        tabla.insert(
            tk.END,
            f"Algoritmo de disco: "
            f"{self.sim.algoritmo_almacenamiento}\n"
        )

        tabla.insert(
            tk.END,
            f"Uso final del disco: "
            f"{metricas_disco.get('porcentaje_uso', 0):.2f}%\n"
        )

        tabla.config(
            state="disabled"
        )

    # =====================================================
    # DIAGRAMA DE GANTT
    # =====================================================

    def actualizar_gantt(self):

        # No dibujar si la CPU está libre
        if self.sim.cpu is None:
            return

        proceso = self.sim.cpu.nombre
        color = self.obtener_color_proceso(proceso)

        x1 = self.gantt_x
        x2 = x1 + self.bloque_gantt

        self.canvas_gantt.create_rectangle(
            x1,
            25,
            x2,
            75,
            fill=color,
            outline="black"
        )

        if self.bloque_gantt >= 15:
            self.canvas_gantt.create_text(
                (x1 + x2) / 2,
                50,
                text=proceso,
                font=("Arial", 8, "bold")
            )

        if self.bloque_gantt >= 10:
            self.canvas_gantt.create_text(
                x1,
                88,
                text=str(self.sim.tiempo),
                font=("Arial", 7)
            )

        self.gantt_x += self.bloque_gantt

        self.canvas_gantt.config(
            scrollregion=(
                0,
                0,
                self.gantt_x + 200,
                105
            )
        )

        self.canvas_gantt.xview_moveto(1)

    # =====================================================
    # OBTENER COLOR DE UN PROCESO
    # =====================================================

    def obtener_color_proceso(self, nombre):

        valor = sum(
            ord(caracter)
            for caracter in nombre
        )

        posicion = valor % len(
            self.lista_colores
        )

        return self.lista_colores[posicion]

    # =====================================================
    # DIBUJAR MEMORIA RAM
    # =====================================================

    def dibujar_memoria(self):

        self.canvas.delete("all")
        self.canvas.update_idletasks()

        ancho_canvas = self.canvas.winfo_width()

        if ancho_canvas <= 1:
            ancho_canvas = 620

        ancho_util = ancho_canvas - 30
        x = 15

        for bloque in self.sim.memoria.bloques:

            ancho = (
                bloque.tamaño
                / self.sim.memoria.tamaño_total
            ) * ancho_util

            if bloque.libre:
                color = "#DFFFD6"
                texto = "Libre"
            else:
                texto = bloque.proceso.nombre
                color = self.obtener_color_proceso(
                    texto
                )

            self.canvas.create_rectangle(
                x,
                50,
                x + ancho,
                180,
                fill=color,
                outline="black"
            )

            # Mostrar texto solamente si el bloque
            # tiene suficiente espacio visual.
            if ancho >= 35:
                self.canvas.create_text(
                    x + ancho / 2,
                    115,
                    text=(
                        f"{texto}\n"
                        f"{bloque.tamaño} KB"
                    ),
                    font=("Arial", 9, "bold")
                )

            x += ancho

        self.canvas.create_text(
            15,
            25,
            text="0 KB",
            anchor="w",
            font=("Arial", 9)
        )

        self.canvas.create_text(
            ancho_canvas - 15,
            25,
            text=(
                f"{self.sim.memoria.tamaño_total} KB"
            ),
            anchor="e",
            font=("Arial", 9)
        )

    # =====================================================
    # DIBUJAR ALMACENAMIENTO EN DISCO
    # =====================================================

    def dibujar_disco(self):

        self.canvas_disco.delete("all")
        self.canvas_disco.update_idletasks()

        disco = self.sim.almacenamiento.disco

        total_bloques = len(disco)

        if total_bloques == 0:
            return

        # Distribución visual de los bloques
        columnas = 8

        filas = (
            total_bloques + columnas - 1
        ) // columnas

        ancho_canvas = self.canvas_disco.winfo_width()
        alto_canvas = self.canvas_disco.winfo_height()

        if ancho_canvas <= 1:
            ancho_canvas = 620

        if alto_canvas <= 1:
            alto_canvas = 230

        margen_x = 15
        margen_y = 15
        espacio = 4

        ancho_bloque = (
            ancho_canvas
            - (margen_x * 2)
            - (espacio * (columnas - 1))
        ) / columnas

        alto_bloque = (
            alto_canvas
            - (margen_y * 2)
            - (espacio * (filas - 1))
        ) / filas

        for indice, contenido in enumerate(disco):

            fila = indice // columnas
            columna = indice % columnas

            x1 = (
                margen_x
                + columna * (ancho_bloque + espacio)
            )

            y1 = (
                margen_y
                + fila * (alto_bloque + espacio)
            )

            x2 = x1 + ancho_bloque
            y2 = y1 + alto_bloque

            if contenido is None:
                color = "#F2F2F2"
                texto = "Libre"
            else:
                # Normalmente el contenido es el nombre
                # del archivo o proceso.
                nombre = str(contenido)

                color = self.obtener_color_proceso(
                    nombre
                )

                texto = nombre

            self.canvas_disco.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="#333333",
                width=1
            )

            # Número del bloque
            self.canvas_disco.create_text(
                x1 + 4,
                y1 + 4,
                text=str(indice),
                anchor="nw",
                font=("Arial", 7),
                fill="#333333"
            )

            # Nombre del proceso o estado libre
            if ancho_bloque >= 45 and alto_bloque >= 20:
                self.canvas_disco.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2 + 3,
                    text=texto,
                    font=("Arial", 8, "bold")
                )


# =========================================================
# EJECUTAR LA APLICACIÓN
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    aplicacion = SistemaOperativoGUI(root)

    root.mainloop()