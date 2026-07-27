from storage_manager import GestorAlmacenamiento


def probar_contigua():

    print("\n" + "=" * 60)
    print("PRUEBA DE ASIGNACIÓN CONTIGUA")
    print("=" * 60)

    disco = GestorAlmacenamiento(
        bloques=16,
        tam_bloque=4,
        algoritmo="Contigua"
    )

    disco.asignar("P1", 12)
    disco.asignar("P2", 20)
    disco.asignar("P3", 8)

    disco.mostrar_estado()
    disco.mostrar_archivos()
    disco.mostrar_metricas()

    print("\nLiberando P2...")

    disco.liberar("P2")

    disco.mostrar_estado()
    disco.mostrar_metricas()


def probar_enlazada():

    print("\n" + "=" * 60)
    print("PRUEBA DE ASIGNACIÓN ENLAZADA")
    print("=" * 60)

    disco = GestorAlmacenamiento(
        bloques=16,
        tam_bloque=4,
        algoritmo="Enlazada"
    )

    disco.asignar("P1", 12)
    disco.asignar("P2", 20)
    disco.asignar("P3", 8)

    disco.mostrar_estado()
    disco.mostrar_archivos()
    disco.mostrar_metricas()

    print("\nLiberando P1...")

    disco.liberar("P1")

    disco.mostrar_estado()
    disco.mostrar_metricas()


def probar_indexada():

    print("\n" + "=" * 60)
    print("PRUEBA DE ASIGNACIÓN INDEXADA")
    print("=" * 60)

    disco = GestorAlmacenamiento(
        bloques=16,
        tam_bloque=4,
        algoritmo="Indexada"
    )

    disco.asignar("P1", 12)
    disco.asignar("P2", 16)
    disco.asignar("P3", 8)

    disco.mostrar_estado()
    disco.mostrar_archivos()
    disco.mostrar_metricas()

    print("\nLiberando P2...")

    disco.liberar("P2")

    disco.mostrar_estado()
    disco.mostrar_metricas()


if __name__ == "__main__":

    probar_contigua()
    probar_enlazada()
    probar_indexada()