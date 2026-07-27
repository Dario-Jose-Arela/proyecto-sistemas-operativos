import csv

from process import Proceso


def leer_procesos(ruta):

    procesos = []

    with open(
        ruta,
        mode="r",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        lector = csv.reader(archivo)

        # Omitir encabezado
        next(lector, None)

        for numero_fila, fila in enumerate(
            lector,
            start=2
        ):

            # Ignorar filas vacías
            if not fila or all(
                not dato.strip()
                for dato in fila
            ):
                continue

            # Se necesitan como mínimo:
            # nombre, llegada, ejecución y memoria
            if len(fila) < 4:
                print(
                    f"Fila {numero_fila} ignorada: "
                    f"faltan datos."
                )
                continue

            try:
                nombre = fila[0].strip()
                llegada = fila[1].strip()
                ejecucion = fila[2].strip()
                memoria = fila[3].strip()

                # Compatibilidad con archivos antiguos.
                # Si no existe la quinta columna,
                # el proceso utilizará 0 KB de disco.
                if len(fila) >= 5 and fila[4].strip():
                    almacenamiento = fila[4].strip()
                else:
                    almacenamiento = 0

                # Validaciones básicas
                if not nombre:
                    raise ValueError(
                        "el nombre está vacío"
                    )

                llegada_num = int(llegada)
                ejecucion_num = int(ejecucion)
                memoria_num = int(memoria)
                almacenamiento_num = int(
                    almacenamiento
                )

                if llegada_num < 0:
                    raise ValueError(
                        "la llegada no puede ser negativa"
                    )

                if ejecucion_num <= 0:
                    raise ValueError(
                        "la ejecución debe ser mayor que 0"
                    )

                if memoria_num <= 0:
                    raise ValueError(
                        "la memoria debe ser mayor que 0"
                    )

                if almacenamiento_num < 0:
                    raise ValueError(
                        "el almacenamiento no puede ser negativo"
                    )

                proceso = Proceso(
                    nombre,
                    llegada_num,
                    ejecucion_num,
                    memoria_num,
                    almacenamiento_num
                )

                procesos.append(proceso)

            except ValueError as error:

                print(
                    f"Fila {numero_fila} ignorada: "
                    f"{error}"
                )

    return procesos