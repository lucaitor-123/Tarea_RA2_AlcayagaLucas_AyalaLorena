import math
import time

import numpy as np
import pandas as pd

from algoritmos import bfprt, quickselect, seleccion_ordenamiento

# datos de integrantes

INTEGRANTES = "Lucas Alcayaga & Lorena Ayala"


# Configuración del experimento

# Nota: Si 10^6 tarda demasiado en tu equipo, se puede ajustar la cota según el hardware

TAMANOS_N = [1000, 10000, 100000, 500000, 1000000]
DISTRIBUCIONES = ["Aleatorio", "Ordenado Ascendente", "Ordenado Descendente", "Con Repetidos"]
REPETICIONES = 10

def generar_datos(n, distribucion):
    """Genera arreglos según la distribución requerida."""
    rng = np.random.default_rng(42)  # Semilla fija para reproducibilidad
    
    if distribucion == "Aleatorio":
        return rng.integers(0, 10**8, size=n).tolist()
    elif distribucion == "Ordenado Ascendente":
        return list(range(n))
    elif distribucion == "Ordenado Descendente":
        return list(range(n, 0, -1))
    elif distribucion == "Con Repetidos":
        # 10% de valores únicos para asegurar alto porcentaje de duplicados
        return rng.integers(0, max(2, n // 10), size=n).tolist()
    else:
        raise ValueError(f"Distribución no válida: {distribucion}")


def obtener_ks(n):
    """Devuelve las posiciones k requeridas: k=1, k=n/2, k=n."""
    return {
        "k=1": 1,
        "k=n/2": max(1, n // 2),
        "k=n": n
    }


def ejecutar_experimentos():
    filas = []
    id_ejecucion = 1
    
    total_combinaciones = len(TAMANOS_N) * len(DISTRIBUCIONES) * 3 * 3
    print(f"Iniciando experimento ({INTEGRANTES})...")
    print(f"Total combinaciones a evaluar: {total_combinaciones}")

    algoritmos = [
        ("Selección Ordenamiento", seleccion_ordenamiento, "O(n log n)"),
        ("Quickselect", quickselect, "O(n) esperado / O(n^2) peor caso"),
        ("BFPRT (Mediana de Medianas)", bfprt, "O(n) peor caso")
    ]

    for n in TAMANOS_N:
        ks = obtener_ks(n)
        for dist in DISTRIBUCIONES:
            print(f" -> Evaluando n={n}, Distribución={dist}...")
            
            # Generamos los datos base para que los 3 algoritmos reciban EXACTAMENTE los mismos datos
            datos_base = generar_datos(n, dist)
            
            for k_nombre, k_val in ks.items():
                for nombre_algo, funcion_algo, orden_teorico in algoritmos:
                    
                    # Para evitar desbordamientos de tiempo en peor caso conocido (Quickselect en ordenados)
                    if nombre_algo == "Quickselect" and dist in ["Ordenado Ascendente", "Ordenado Descendente"] and n >= 100000:
                        print(f"    [Omitido] {nombre_algo} en {dist} (n={n}) para evitar recursion excesiva / O(n^2).")
                        continue
                        
                    for rep in range(1, REPETICIONES + 1):
                        # Calentamiento / Copia de datos
                        arr_copia = datos_base.copy()
                        
                        t0 = time.perf_counter()
                        _, comps = funcion_algo(arr_copia, k_val)
                        t1 = time.perf_counter()
                        
                        tiempo_ms = (t1 - t0) * 1000.0  # Convertir a milisegundos
                        
                        filas.append({
                            "id_ejecucion": id_ejecucion,
                            "integrantes": INTEGRANTES,
                            "algoritmo": nombre_algo,
                            "n": n,
                            "tipo_datos": dist,
                            "k_etiqueta": k_nombre,
                            "k_valor": k_val,
                            "repeticion": rep,
                            "tiempo_ms": tiempo_ms,
                            "comparaciones": comps,
                            "orden_teorico": orden_teorico
                        })
                        id_ejecucion += 1

    df = pd.DataFrame(filas)
    
    # Nombre del CSV incluyendo a ambos integrantes
    nombre_csv = "datos_experimentales_AlcayagaLucas_AyalaLorena.csv"
    df.to_csv(nombre_csv, index=False)
    print(f"\n Experimento completado con éxito. Datos guardados en: {nombre_csv}")


if __name__ == "__main__":
    ejecutar_experimentos()