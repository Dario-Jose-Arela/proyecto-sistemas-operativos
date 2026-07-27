from process import Proceso
from simulator import SimuladorSO


procesos = [
    Proceso("P1", 0, 4, 100, 12),
    Proceso("P2", 1, 3, 150, 20),
    Proceso("P3", 2, 5, 200, 8)
]

simulador = SimuladorSO(
    procesos=procesos,
    algoritmo_cpu="FCFS",
    algoritmo_memoria="First Fit",
    algoritmo_almacenamiento="Contigua",
    quantum=2
)

while len(simulador.finalizados) < len(procesos):
    simulador.ejecutar_tick()

print("\nSIMULACIÓN FINALIZADA")

simulador.almacenamiento.mostrar_estado()
simulador.almacenamiento.mostrar_metricas()