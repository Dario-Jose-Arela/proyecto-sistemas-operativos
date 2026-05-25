def calcular_metricas(procesos):

    resultados = []

    total_espera = 0

    total_retorno = 0

    for p in procesos:

        retorno = p.fin - p.llegada

        espera = retorno - p.ejecucion

        resultados.append({

            "nombre": p.nombre,

            "llegada": p.llegada,

            "ejecucion": p.ejecucion,

            "fin": p.fin,

            "retorno": retorno,

            "espera": espera
        })

        total_espera += espera

        total_retorno += retorno

    promedio_espera = (
        total_espera / len(procesos)
    )

    promedio_retorno = (
        total_retorno / len(procesos)
    )

    return (
        resultados,
        promedio_espera,
        promedio_retorno
    )