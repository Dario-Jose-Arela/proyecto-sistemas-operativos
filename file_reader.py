import csv

from process import Proceso


def leer_procesos(ruta):

    procesos = []

    with open(ruta, newline='') as archivo:

        lector = csv.reader(archivo)

        next(lector)

        for fila in lector:

            if len(fila) < 4:
                continue

            nombre = fila[0].strip()
            llegada = fila[1].strip()
            ejecucion = fila[2].strip()
            memoria = fila[3].strip()

            proceso = Proceso(
                nombre,
                llegada,
                ejecucion,
                memoria
            )

            procesos.append(proceso)

    return procesos