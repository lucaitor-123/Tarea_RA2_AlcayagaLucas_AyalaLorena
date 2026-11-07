import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuración de estilo

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11})

NOMBRE_CSV = "datos_experimentales_AlcayagaLucas_AyalaLorena.csv"

def cargar_y_procesar_datos():
    try:
        df = pd.read_csv(NOMBRE_CSV)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{NOMBRE_CSV}'. Ejecuta primero 'experimento.py'.")
        return None, None

    # Agrupar por algoritmo, n, tipo de datos y k para calcular promedio y desviación estándar
    resumen = df.groupby(["algoritmo", "n", "tipo_datos", "k_etiqueta"]).agg(
        tiempo_prom_ms=("tiempo_ms", "mean"),
        tiempo_std_ms=("tiempo_ms", "std"),
        comparaciones_prom=("comparaciones", "mean"),
        comparaciones_std=("comparaciones", "std"),
        orden_teorico=("orden_teorico", "first")
    ).reset_index()

    return df, resumen


def generar_graficos(resumen):
    if resumen is None:
        return

    distribuciones = resumen["tipo_datos"].unique()
   
    print("Generando gráficos para el informe PDF...")

    # 1. Gráficos de Tiempo vs. Tamaño (n) por cada Distribución (con k=n/2)
    for dist in distribuciones:
        _, ax = plt.subplots(figsize=(8, 5))
        sub = resumen[(resumen["tipo_datos"] == dist) & (resumen["k_etiqueta"] == "k=n/2")]
        
        sns.lineplot(
            data=sub,
            x="n",
            y="tiempo_prom_ms",
            hue="algoritmo",
            marker="o",
            ax=ax,
            linewidth=2
        )

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"Tiempo de Ejecución vs. Tamaño $n$ ({dist}, $k=n/2$)", fontsize=12, fontweight='bold')
        ax.set_xlabel("Tamaño de entrada $n$ (Escala Logarítmica)")
        ax.set_ylabel("Tiempo Promedio (ms) (Escala Logarítmica)")
        ax.grid(True, which="both", ls="--", alpha=0.6)
        
        plt.tight_layout()
        nombre_fig = f"grafico_tiempo_{dist.lower().replace(' ', '_')}.png"
        plt.savefig(nombre_fig, dpi=300)
        plt.close()
        print(f"  Guardado: {nombre_fig}")

    # 2. Gráfico de Comparaciones vs. Tamaño (n) en Distribución Aleatoria
    _, ax = plt.subplots(figsize=(8, 5))
    sub_comp = resumen[(resumen["tipo_datos"] == "Aleatorio") & (resumen["k_etiqueta"] == "k=n/2")]
    
    sns.lineplot(
        data=sub_comp,
        x="n",
        y="comparaciones_prom",
        hue="algoritmo",
        marker="s",
        ax=ax,
        linewidth=2
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Número de Comparaciones vs. Tamaño $n$ (Datos Aleatorios, $k=n/2$)", fontsize=12, fontweight='bold')
    ax.set_xlabel("Tamaño de entrada $n$ (Escala Logarítmica)")
    ax.set_ylabel("Comparaciones Promedio (Escala Logarítmica)")
    ax.grid(True, which="both", ls="--", alpha=0.6)

    plt.tight_layout()
    nombre_fig_comp = "grafico_comparaciones_aleatorio.png"
    plt.savefig(nombre_fig_comp, dpi=300)
    plt.close()
    print(f"  Guardado: {nombre_fig_comp}")

    print("\nTodos los gráficos fueron generados y guardados correctamente en la carpeta.")


if __name__ == "__main__":
    df, resumen = cargar_y_procesar_datos()
    if resumen is not None:
        # Guardar resumen en CSV
        resumen.to_csv("resumen_estadistico_AlcayagaLucas_AyalaLorena.csv", index=False)
        print(" Resumen estadístico (promedios y desviaciones) guardado.")
        generar_graficos(resumen)