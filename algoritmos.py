"""Algoritmos de selección. k es 1-indexado; comparaciones = comparaciones reales entre valores."""
from functools import cmp_to_key
import random


def _validar(arr, k):
    if not 1 <= k <= len(arr):
        raise ValueError(f"k={k} fuera de rango para n={len(arr)}")


def seleccion_ordenamiento(arr, k):
    """Ordenamiento completo TimSort O(n log n) peor caso; comparaciones observadas."""
    _validar(arr, k)
    comparaciones = 0

    def comparar(a, b):
        nonlocal comparaciones
        comparaciones += 1
        return (a > b) - (a < b)

    ordenados = sorted(arr, key=cmp_to_key(comparar))
    return ordenados[k - 1], comparaciones


def quickselect(arr, k, estrategia_pivote="aleatorio", semilla=42):
    """Quickselect iterativo con partición de Hoare.

    'aleatorio' (predeterminado): O(n) esperado para entradas arbitrarias.
    'primero': permite examinar el peor caso O(n²) en entradas ordenadas pequeñas.
    No se modifica el arreglo del llamador.
    """
    _validar(arr, k)
    if estrategia_pivote not in ("aleatorio", "primero"):
        raise ValueError("estrategia_pivote debe ser 'aleatorio' o 'primero'")
    A = arr.copy()
    rng = random.Random(semilla)
    comparaciones = 0
    low, high, objetivo = 0, len(A) - 1, k - 1

    while low < high:
        if estrategia_pivote == "aleatorio":
            posicion = rng.randrange(low, high + 1)
            A[low], A[posicion] = A[posicion], A[low]
        pivote = A[low]
        i, j = low - 1, high + 1
        while True:
            i += 1
            comparaciones += 1
            while A[i] < pivote:
                i += 1
                comparaciones += 1
            j -= 1
            comparaciones += 1
            while A[j] > pivote:
                j -= 1
                comparaciones += 1
            if i >= j:
                corte = j
                break
            A[i], A[j] = A[j], A[i]

        if objetivo <= corte:
            high = corte
        else:
            low = corte + 1

    return A[low], comparaciones


def bfprt(arr, k):
    """Selección mediana de medianas en grupos de 5, O(n) en peor caso.

    Cuenta todas las comparaciones de valores, tanto en inserción como en la
    partición de tres vías; no usa estimaciones n log n.
    """
    _validar(arr, k)
    comparaciones = 0

    def ordenar_grupo(grupo):
        nonlocal comparaciones
        grupo = list(grupo)
        for i in range(1, len(grupo)):
            x = grupo[i]
            j = i - 1
            while j >= 0:
                comparaciones += 1
                if grupo[j] <= x:
                    break
                grupo[j + 1] = grupo[j]
                j -= 1
            grupo[j + 1] = x
        return grupo

    def seleccionar(valores, indice):
        nonlocal comparaciones
        n = len(valores)
        if n <= 5:
            return ordenar_grupo(valores)[indice]

        medianas = []
        for pos in range(0, n, 5):
            grupo = ordenar_grupo(valores[pos:pos + 5])
            medianas.append(grupo[len(grupo) // 2])
        pivote = seleccionar(medianas, len(medianas) // 2)

        menores, mayores = [], []
        iguales = 0
        for valor in valores:
            comparaciones += 1
            if valor < pivote:
                menores.append(valor)
            else:
                comparaciones += 1
                if valor == pivote:
                    iguales += 1
                else:
                    mayores.append(valor)
        if indice < len(menores):
            return seleccionar(menores, indice)
        if indice < len(menores) + iguales:
            return pivote
        return seleccionar(mayores, indice - len(menores) - iguales)

    return seleccionar(arr.copy(), k - 1), comparaciones
