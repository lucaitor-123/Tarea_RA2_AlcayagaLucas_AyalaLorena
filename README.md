# Tarea Práctica N° 1 – Evaluación del Rendimiento de Algoritmos de Selección

**Asignatura:** Diseño y Análisis de Algoritmos · **Institución:** Universidad Católica del Norte  
**Profesor:** Claudio Meneses V. · **Ayudante:** Gustavo Miles  
**Integrantes:** Lucas Alcayaga y Lorena Ayala

## Objetivo
Evaluar empíricamente el k-ésimo elemento más pequeño (k empieza en 1), contrastando:

| Algoritmo | Complejidad de referencia | Implementación |
|---|---|---|
| TimSort, ordenamiento completo | O(n log n) peor caso | `sorted()` con comparador instrumentado |
| Quickselect (Hoare) | O(n) esperado; O(n²) peor caso | Partición de Hoare **iterativa** y pivote aleatorio de semilla fija |
| BFPRT (mediana de medianas) | O(n) peor caso | Grupos de 5, inserción y partición ternaria |

Los contadores indican **comparaciones efectuadas entre valores**. En TimSort se cuentan llamadas reales al comparador; BFPRT cuenta las comparaciones de ordenación de cada grupo y las comparaciones de partición (puede usar dos por valor); Quickselect cuenta cada evaluación de las condiciones de partición. No son comparaciones de exactamente el mismo tipo en todas las implementaciones, pero todas se observan durante la ejecución y no se estiman con fórmulas.

**Importante:** instrumentar comparaciones agrega sobrecarga al tiempo de ejecución. TimSort utiliza un comparador Python para contar llamadas, de modo que el tiempo observado no equivale al tiempo de `list.sort()` sin instrumentación. Los tiempos comparan estas implementaciones instrumentadas, no bibliotecas de producción sin instrumentar.

## Requisitos
Python 3.9+ y `numpy`, `pandas`, `matplotlib`, `seaborn`:

```powershell
python -m pip install numpy pandas matplotlib seaborn
```

## Ejecutar en VS Code
Abrir la carpeta que contiene `algoritmos.py`. Después ejecutar:

```powershell
python experimento.py --rapido
python experimento.py
python graficar.py
python experimento.py --peor-caso
```

- `--rapido`: validación preliminar reducida (2 tamaños × 4 distribuciones × 3 valores k × 3 algoritmos × 2 repeticiones). Produce **`prueba_rapida.csv`**, que **no sirve** como resultados definitivos.
- Sin argumentos: protocolo completo: 5 tamaños (10³, 10⁴, 10⁵, 5·10⁵, 10⁶), 4 distribuciones (aleatorio, ascendente, descendente, 10 % únicos aprox.), 3 posiciones k (1, n/2, n), 10 repeticiones = **1.800 mediciones/180 combinaciones**. Puede tardar bastante en equipos modestos.
- `graficar.py`: calcula promedios, desviaciones estándar, total de repeticiones y produce 24 gráficos (tiempos y comparaciones para cada distribución y valor k). Rechaza archivos previos no validados.
- `--peor-caso`: ensayo **complementario y separado** (`demostracion_pivote_inicial.csv`) que usa siempre el primer elemento como pivote, con tamaños limitados hasta 5.000 y 3 repeticiones. Permite examinar el peor caso cuadrático de Quickselect en arreglos ordenados sin aplicar la variante lenta a los tamaños mayores. No mezclar sus medidas con el protocolo principal.

La opción principal con pivote aleatorio no tiene por qué mostrar un deterioro notable en entradas ordenadas: sus particiones esperadas son equilibradas; se explica en el informe y se contrasta con la prueba complementaria.

## Rigurosidad del protocolo
- En cada repetición se crea un arreglo con **semilla explícita**, distinto para datos aleatorios y repetidos entre repeticiones, y compartido por los algoritmos y valores de k de la misma combinación.
- Para distribuciones totalmente ordenadas el arreglo es necesariamente idéntico en cada repetición; se replica la medición temporal, no una muestra aleatoria distinta.
- Se calcula `sorted(datos)[k-1]` **fuera del cronómetro**. Se comprueba cada resultado y se detiene el experimento si alguno es incorrecto.
- Las copias de entrada y el conteo están incluidos en el tiempo; la creación de datos, la referencia y la escritura del CSV se excluyen.
- En el CSV se guardan `semilla_datos`, `validado`, el número de repetición y la estrategia de pivote.
- Para reproducir el experimento debe documentarse además el equipo utilizado (CPU, RAM, sistema operativo y versión de Python) en el informe; al finalizar el script imprime datos básicos del entorno.

## Archivos
- `algoritmos.py`: implementaciones con contadores reales.
- `experimento.py`: protocolo validado y ensayo opcional del peor caso.
- `graficar.py`: estadística y gráficos.
- `datos_experimentales_AlcayagaLucas_AyalaLorena.csv`: **se genera al ejecutar el protocolo completo**, no se incluye una versión antigua como si fuera válida.
- `resumen_estadistico_AlcayagaLucas_AyalaLorena.csv`: se genera con `graficar.py`.
- `resultados_originales/`: archivos CSV y PNG obtenidos con el código **anterior**; son **históricos y no válidos para comparar** con las mediciones corregidas. Deben reemplazarse al completar las nuevas pruebas.

## Informe pendiente
La rúbrica exige entregar además un PDF con portada, marco teórico, pseudocódigo de cada algoritmo, análisis de complejidades, metodología, hardware/software, tablas, gráficos, discusión por n/distribución/k, conclusiones y referencias. El informe **no se incluye** en este ZIP corregido.
