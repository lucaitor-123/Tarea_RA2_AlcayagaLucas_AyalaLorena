# Tarea Práctica N° 1: Evaluación del Rendimiento de Algoritmos de Selección
**Asignatura:** Diseño y Análisis de Algoritmos  
**Institución:** Universidad Católica del Norte   
**Facultad:** Facultad de Ingeniería y Ciencias Geológicas  
**Departamento:** Departamento de Ingeniería de Sistemas y Computación  
**Profesor:** Claudio Meneses V.  
**Ayudante:** Gustavo Miles  
**Integrantes:** Lucas Alcayaga & Lorena Ayala  



##  Descripción del Proyecto
Este proyecto evalúa empíricamente el rendimiento de distintos algoritmos diseñados para resolver el Problema de Selección, el cual consiste en determinar el $k$-ésimo elemento más pequeño dentro de un conjunto de $n$ elementos no ordenados.

Se implementaron y contrastaron tres algoritmos principales:
1. **Selección por Ordenamiento Completo:** Algoritmo base utilizando TimSort ($O(n \log n)$).
2. **Quickselect :** Algoritmo de división y conquista ($O(n)$ caso promedio, $O(n^2)$ peor caso).
3. **Mediana de Medianas :** Algoritmo con pivote óptimo mediante grupos de 5 ($O(n)$ garantizado en peor caso).



##  Requisitos del Entorno y Software
* **Lenguaje de Programación:** Python 3.9 o superior.
* **Bibliotecas Requeridas:**
  * `numpy`: Generación sintética y eficiente de distribuciones de datos.
  * `pandas`: Procesamiento, estructuración y exportación de datos a CSV.
  * `matplotlib`: Renderizado de gráficos de rendimiento.
  * `seaborn`: Estilización visual de curvas comparativas.

### Instalación de dependencias
Ejecute el siguiente comando en la terminal de VS Code:
```bash
pip install numpy pandas matplotlib seaborn
```



##  Estructura del Repositorio
* `algoritmos.py`: Implementación modular de los tres algoritmos con contadores de comparaciones integrados.
* `experimento.py`: Protocolo experimental que automatiza las corridas ($n$, distribuciones, $k$, repeticiones) y exporta los datos crudos.
* `graficar.py`: Script de procesamiento estadístico (promedios, desviación estándar) y generación de gráficos comparativos.
* `datos_experimentales_AlcayagaLucas_AyalaLorena.csv`: Registros crudos de todas las iteraciones ejecutadas.
* `resumen_estadistico_AlcayagaLucas_AyalaLorena.csv`: Resumen de promedios y desviaciones estándar agrupados.
* `README.md`: Documentación formal de uso e instalación.



##  Protocolo Experimental
El estudio considera las siguientes variables controladas:
* **Tamaños de entrada ($n$):** $10^3$, $10^4$, $10^5$, $5 \times 10^5$, $10^6$.
* **Distribuciones de datos:** Aleatorio (Uniforme), Ordenado Ascendente, Ordenado Descendente, y Con Repetidos (10% de valores únicos).
* **Valores de $k$:** $k=1$ (Mínimo), $k=\lfloor n/2 \rfloor$ (Mediana), $k=n$ (Máximo).
* **Repeticiones:** 10 ejecuciones independientes por combinación para asegurar rigurosidad estadística.



##  Instrucciones de Ejecución

1. **Ejecución del Experimento:**
   Para correr la suite de pruebas y generar el archivo de datos crudos:
   ```bash
   python experimento.py
   ```

2. **Procesamiento de Gráficos y Tablas:**
   Una vez concluido el experimento, genere las métricas visuales para el informe con:
   ```bash
   python graficar.py
   ```



## Entregables del Proyecto
1. **Código fuente:** Carpeta del proyecto documentada con `README.md`.
2. **Datos crudos:** Archivo `.csv` con las mediciones individuales de tiempo ($ms$) y comparaciones.
3. **Informe PDF:** Documento escrito (`Informe_RA2_AlcayagaLucas_AyalaLorena.pdf`) con marco teórico, pseudocódigos, análisis empírico y conclusiones.