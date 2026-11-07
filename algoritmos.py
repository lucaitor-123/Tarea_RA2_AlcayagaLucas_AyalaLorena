import math
import sys

# Para evitar límites de recursión en arreglos grandes
sys.setrecursionlimit(2000000)


# 1. Selección por ordenamiento completo
def seleccion_ordenamiento(arr, k):
    """
    Ordena una copia del arreglo y obtiene la posición k-1.
    Complejidad: O(n log n)
    """
    A = arr.copy()
    n = len(A)
    A.sort()
    
    # Estimación de comparaciones para sort() en Python (TimSort)
    comparaciones = int(n * math.log2(n)) if n > 1 else 0
    
    return A[k - 1], comparaciones



# 2. QUICKSELECT 

def quickselect(arr, k):
    """
    Algoritmo de Quickselect con partición de Hoare.
    Complejidad: O(n) esperado, O(n^2) peor caso
    """
    A = arr.copy()
    comparaciones = [0]
    
    def particion(low, high):
        pivote = A[low]
        i = low - 1
        j = high + 1
        while True:
            i += 1
            comparaciones[0] += 1
            while A[i] < pivote:
                i += 1
                comparaciones[0] += 1
                
            j -= 1
            comparaciones[0] += 1
            while A[j] > pivote:
                j -= 1
                comparaciones[0] += 1
                
            if i >= j:
                return j
            A[i], A[j] = A[j], A[i]

    def select(low, high, k_idx):
        if low == high:
            return A[low]
        
        pivote_idx = particion(low, high)
        
        if k_idx <= pivote_idx:
            return select(low, pivote_idx, k_idx)
        else:
            return select(pivote_idx + 1, high, k_idx)

    res = select(0, len(A) - 1, k - 1)
    return res, comparaciones[0]



# 3. Mediana de medianas
def bfprt(arr, k):
    """
    Algoritmo Mediana de Medianas (BFPRT) agrupando de a 5 elementos.
    Complejidad: O(n) garantizado en peor caso
    """
    A = arr.copy()
    comparaciones = [0]

    def select(sub_arr, k_idx):
        n = len(sub_arr)
        if n <= 5:
            sub_arr.sort()
            comparaciones[0] += int(n * math.log2(n)) if n > 1 else 0
            return sub_arr[k_idx]

        # 1. Dividir en grupos de 5 y obtener medianas
        grupos = [sub_arr[i:i + 5] for i in range(0, n, 5)]
        medianas = []
        for grupo in grupos:
            grupo.sort()
            m_len = len(grupo)
            comparaciones[0] += int(m_len * math.log2(m_len)) if m_len > 1 else 0
            medianas.append(grupo[m_len // 2])

        # 2. Encontrar la mediana de las medianas de forma recursiva
        pivote = select(medianas, len(medianas) // 2)

        # 3. Particionar el arreglo en base al pivote obtenido
        menores = []
        iguales = []
        mayores = []
        
        for elem in sub_arr:
            comparaciones[0] += 1
            if elem < pivote:
                menores.append(elem)
            elif elem == pivote:
                iguales.append(elem)
            else:
                mayores.append(elem)

        # 4. Decidir en qué subarreglo continuar
        if k_idx < len(menores):
            return select(menores, k_idx)
        elif k_idx < len(menores) + len(iguales):
            return pivote
        else:
            return select(mayores, k_idx - len(menores) - len(iguales))

    res = select(A, k - 1)
    return res, comparaciones[0]