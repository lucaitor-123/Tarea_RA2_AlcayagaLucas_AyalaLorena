"""Protocolo experimental reproducible para la tarea RA2."""
import argparse
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from algoritmos import bfprt, quickselect, seleccion_ordenamiento

INTEGRANTES = "Lucas Alcayaga & Lorena Ayala"
TAMANOS_N = [1000, 10000, 100000, 500000, 1000000]
DISTRIBUCIONES = ["Aleatorio", "Ordenado Ascendente", "Ordenado Descendente", "Con Repetidos"]
REPETICIONES = 10
ARCHIVO_DATOS = "datos_experimentales_AlcayagaLucas_AyalaLorena.csv"


def generar_datos(n, distribucion, semilla):
    rng = np.random.default_rng(semilla)
    if distribucion == "Aleatorio":
        return rng.integers(0, 10**8, size=n).tolist()
    if distribucion == "Ordenado Ascendente":
        return list(range(n))
    if distribucion == "Ordenado Descendente":
        return list(range(n, 0, -1))
    if distribucion == "Con Repetidos":
        return rng.integers(0, max(2, n // 10), size=n).tolist()
    raise ValueError(f"Distribución desconocida: {distribucion}")


def obtener_ks(n):
    return {"k=1": 1, "k=n/2": max(1, n // 2), "k=n": n}


def ejecutar_experimentos(tamanos=None, repeticiones=REPETICIONES, salida=ARCHIVO_DATOS):
    tamanos = TAMANOS_N if tamanos is None else tamanos
    algoritmos = [
        ("Selección Ordenamiento", seleccion_ordenamiento, "O(n log n)"),
        ("Quickselect", quickselect, "O(n) esperado / O(n^2) peor caso"),
        ("BFPRT (Mediana de Medianas)", bfprt, "O(n) peor caso"),
    ]
    total = len(tamanos) * len(DISTRIBUCIONES) * 3 * len(algoritmos) * repeticiones
    print(f"Iniciando: {INTEGRANTES}. Mediciones previstas: {total}", flush=True)
    encabezados = ["id_ejecucion", "integrantes", "algoritmo", "n", "tipo_datos",
                   "k_etiqueta", "k_valor", "repeticion", "semilla_datos", "tiempo_ms",
                   "comparaciones", "orden_teorico", "validado", "estrategia_pivote"]
    import csv
    destino = Path(salida)
    with destino.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=encabezados)
        escritor.writeheader()
        id_ejecucion = 1
        for n in tamanos:
            for dist in DISTRIBUCIONES:
                print(f"n={n:,} | {dist}", flush=True)
                for rep in range(1, repeticiones + 1):
                    # Una semilla distinta por repetición. Todos los algoritmos y k
                    # reciben exactamente el mismo conjunto de datos en ella.
                    semilla = 20261112 + rep * 1000003 + n
                    datos = generar_datos(n, dist, semilla)
                    datos_ordenados = sorted(datos)  # fuera de las mediciones
                    for k_nombre, k_val in obtener_ks(n).items():
                        esperado = datos_ordenados[k_val - 1]
                        for nombre, funcion, orden in algoritmos:
                            # Tiempo incluye copia interna y conteo de comparaciones,
                            # pero excluye creación de entrada y comprobación.
                            inicio = time.perf_counter()
                            obtenido, comps = funcion(datos, k_val)
                            transcurrido = (time.perf_counter() - inicio) * 1000
                            if obtenido != esperado:
                                raise AssertionError(
                                    f"ERROR {nombre} n={n} dist={dist} k={k_val} rep={rep}: "
                                    f"obtenido={obtenido} esperado={esperado}"
                                )
                            escritor.writerow({
                                "id_ejecucion": id_ejecucion, "integrantes": INTEGRANTES,
                                "algoritmo": nombre, "n": n, "tipo_datos": dist,
                                "k_etiqueta": k_nombre, "k_valor": k_val,
                                "repeticion": rep, "semilla_datos": semilla,
                                "tiempo_ms": transcurrido, "comparaciones": comps,
                                "orden_teorico": orden, "validado": True,
                                "estrategia_pivote": "aleatorio" if nombre == "Quickselect" else "no aplica"
                            })
                            id_ejecucion += 1
                archivo.flush()
    print(f"Experimento completado: {id_ejecucion-1}/{total} filas. {destino}")
    print(f"Python {platform.python_version()} | {platform.platform()} | CPU: {platform.processor()}")


def demostracion_peor_caso(salida="demostracion_pivote_inicial.csv"):
    """Experimento complementario acotado de Quickselect con primer pivote."""
    filas = []
    for n in [1000, 2000, 5000]:
        for dist in ["Ordenado Ascendente", "Ordenado Descendente"]:
            datos = generar_datos(n, dist, 42)
            for etiqueta, k in obtener_ks(n).items():
                esperado = sorted(datos)[k - 1]
                for rep in range(1, 4):
                    ini = time.perf_counter()
                    resultado, comps = quickselect(datos, k, estrategia_pivote="primero")
                    ms = (time.perf_counter() - ini) * 1000
                    if resultado != esperado:
                        raise AssertionError("Fallo de validación en demostración de peor caso")
                    filas.append({"n": n, "tipo_datos": dist, "k_etiqueta": etiqueta,
                                  "repeticion": rep, "tiempo_ms": ms, "comparaciones": comps,
                                  "estrategia_pivote": "primero"})
    pd.DataFrame(filas).to_csv(salida, index=False)
    print(f"Prueba complementaria guardada: {salida}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento de selección RA2")
    parser.add_argument("--rapido", action="store_true", help="Prueba reducida para verificar funcionamiento (no apta para informe)")
    parser.add_argument("--peor-caso", action="store_true", help="Ensayo complementario con pivote inicial")
    args = parser.parse_args()
    if args.peor_caso:
        demostracion_peor_caso()
    elif args.rapido:
        ejecutar_experimentos([1000, 10000], 2, "prueba_rapida.csv")
    else:
        ejecutar_experimentos()
